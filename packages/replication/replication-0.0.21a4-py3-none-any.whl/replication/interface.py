# ##### BEGIN GPL LICENSE BLOCK #####
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####


import logging
import queue
import time
import threading
import sys

from .constants import (ADDED, COMMITED, FETCHED,
                        STATE_ACTIVE, STATE_INITIAL,
                        STATE_SYNCING, UP, MODIFIED,
                        RP_COMMON, RP_STRICT)
from .data import (ReplicatedCommand, RepDeleteCommand,
                   ReplicatedDatablock, RepRightCommand,
                   RepDisconnectCommand, RepUpdateClientsState,
                   RepUpdateUserMetadata, RepKickCommand)
from .graph import ReplicationGraph
from .network import (ServerNetService,
                      ServerTTL)
from .exception import NonAuthorizedOperationError
from .orchestrator import Orchestrator


class Session(object):
    def __init__(
            self,
            factory=None,
            python_path=sys.executable):
        assert(factory)

        self._item_to_push = queue.Queue()
        self._tasks = queue.Queue()
        self._net_server = None
        self._factory = factory
        self._id = None

        self._observers = []
        self._online_users = {}

        self._graph = ReplicationGraph()

        self._orchestrator = Orchestrator(
            replication_graph=self._graph,
            q_tasks=self._tasks,
            q_net_output=self._item_to_push,
            python_path=python_path,
            session=self,
            factory=self._factory
        )

        self.callbacks = {}

    def _assert_modification_rights(self, node=None):
        if self._graph[node].owner not in [self._id, RP_COMMON]:
            raise NonAuthorizedOperationError(
                "Not authorized to delete the node")

    def _check_dependencies(self, node_uuid):
        node = self._graph[node_uuid]

        assert(node)
        if not node.instance:
            return

        if node.dependencies:
            node.dependencies.clear()
        dependencies = node.resolve_deps()

        for dep in dependencies:
            if dep:
                dep_node = self.get(reference=dep)
                if not dep_node:
                    dep_node_uuid = self.add(dep, owner=node.owner)
                else:
                    dep_node_uuid = dep_node.uuid

                node.add_dependency(dep_node_uuid)

    def register(self, name):
        def func_wrapper(func):
            self.callbacks[name] = func
            return func
        return func_wrapper
    
    def call_registered(self, name=None):
        func = self.callbacks.get(name, None)
        if func is None:
            logging.info("No function registered against - " + str(name))
            return None
        return func()

    def connect(self,
                id="Default",
                address="127.0.0.1",
                port=5560,
                ipc_port=5560,
                timeout=1000,
                password=None):
        """Connect to a session

        :param id: user name
        :type id: string
        :param address: host ip address
        :type address: string
        :param port: host port
        :type port: int
        """
        self._orchestrator.connect(
            id,
            address,
            port,
            ipc_port,
            timeout=timeout,
            password=password)
        self._id = id

    def host(self,
             id="Default",
             port=5560,
             ipc_port=5569,
             timeout=1000,
             password=None):
        """Host a session

        :param id: user name
        :type id: string
        :param address: host ip address
        :type address: strings
        :param port: host port
        :type port: int
        """
        # Create a server and serve
        self._orchestrator.host(
            id=id,
            port=port,
            ipc_port=ipc_port,
            timeout=timeout,
            password=password
        )
        self._id = id

    def init(self):
        """ Init the repository data

            commit and push initial graph to the server
        """
        if len(self._graph) == 0:
            logging.error("Add some data first")
            return
        
        self._orchestrator.init_repository()

    def disconnect(self):
        """Disconnect from session
        """
        self._orchestrator.disconnect()

    def add(self, object, owner=None, dependencies=None):
        """Register a python object for replication

        :param objet: Any registered object
        :type object: Any registered object type in the given factory
        :param dependencies: Object dependencies uuid
        :type dependencies: Array of string
        """
        assert(object)

        # Retrieve corresponding implementation and init a new instance
        implementation = self._factory.get_implementation_from_object(
            object)

        if implementation:
            default_owner = RP_COMMON

            new_owner = owner if owner else default_owner
            new_node = implementation(
                owner=new_owner, instance=object, dependencies=dependencies)

            if new_node:
                dependencies = new_node.resolve_deps()

                for dependance in dependencies:
                    dep_ref = self.get(reference=dependance)
                    if dep_ref:
                        new_node.add_dependency(dep_ref.uuid)
                    else:
                        if dependance:
                            new_child_node = self.add(object=dependance)
                            if new_child_node:
                                new_node.add_dependency(new_child_node)

                logging.debug(f"Registering {object} as {new_node.uuid}")
                new_node.store(self._graph)

                return new_node.uuid
        else:
            logging.error(f"{type(object)} not supported, skipping.")
            return None

    def remove(self, uuid, remove_dependencies=True):
        """
        Unregister for replication the given object.

        :param uuid: node uuidñ
        :type uuid: string
        :param remove_dependencies: remove all dependencies
        :type remove_dependencies: bool (default: True)
        :raise NonAuthorizedOperationError:
        :raise KeyError:
        """
        self._assert_modification_rights(uuid)

        if uuid in self._graph.keys():
            nodes_to_delete = []

            if remove_dependencies:
                nodes_to_delete.extend(
                    self._graph.get_dependencies_ordered(node=uuid))

            nodes_to_delete.append(uuid)

            for node in nodes_to_delete:
                delete_command = RepDeleteCommand(
                    owner='client', data=node)
                # remove the key from our store
                delete_command.execute(self._graph)
                self._item_to_push.put(delete_command)

        else:
            raise KeyError("Cannot unregister key")

    def kick(self, user):
        """
        Kick a user from the session.
        """

        if user == self._id:
            logging.error("You can't kick ypurself")
            return

        self._item_to_push.put(
            RepKickCommand(
                owner=self._id,
                data={
                    'user':user,
                }
            )
         )
   
    def commit(self, uuid):
        """Commit the given node

        :param uuid: node uuid
        :type uuid: string
        """
        # TODO: refactoring
        assert(self.exist(uuid))

        if self._graph[uuid].state == COMMITED:
            return

        self._check_dependencies(uuid)

        for node in self._graph.get_dependencies_ordered(node=uuid):
            if self._graph[node].state in [ADDED, MODIFIED]:
                self._tasks.put(('COMMIT', node))
        self._tasks.put(('COMMIT', uuid))

    def push(self, uuid):
        """Replicate a given node to all users. Send all node in `COMMITED` by default.

        :param uuid: node key to push
        :type uuid: string
        """
        # TODO: Refactoring
        if uuid:
            self._assert_modification_rights(uuid)

            node = self._graph[uuid]

            for dep in self._graph.get_dependencies_ordered(node=uuid):
                dep_node = self._graph[dep]
                if dep_node.state in [COMMITED, ADDED]:
                    self._tasks.put(('PUSH', dep))
            self._tasks.put(('PUSH', uuid))

    def push_all(self):
        for node in self.list():
            self.push(node)

    def apply(self, uuid=None, force=False):
        """Apply incoming modifications to local object(s) instance

        :param uuid: node key to push
        :type uuid: string
        """
        assert(self._graph[uuid].state in [FETCHED, UP])

        deps = self._graph.get_dependencies_ordered(node=uuid)

        for dep in deps:
            node = self.get(uuid=dep)

            # Check dependencies states, abort if needed
            if node and node.state == FETCHED:
                if force:
                    self.apply(uuid=node.uuid, force=force)
                else:
                    return

        self.get(uuid=uuid).apply()

    def apply_all(self):
        nodes = self._graph.get_nodes_in_state(state=FETCHED)

        for n in nodes:
            self.apply(n)

    def change_owner(self, uuid, new_owner, recursive=True):
        """Change a node owner

        :param uuid: node key
        :type uuid: string
        :param new_owner: new owner id
        :type new_owner: string
        """
        assert(uuid and new_owner)

        # and self._graph[uuid].owner != self._id
        if uuid in self._graph.keys() and self._graph[uuid].owner in [RP_COMMON, self._id]:
            if recursive:
                for node in self._graph.get_dependencies_ordered(node=uuid):
                    self.change_owner(
                        uuid=node, new_owner=new_owner, recursive=recursive)

            # Setup the right override command
            right_command = RepRightCommand(
                owner=self._id,
                data={
                    'uuid': uuid,
                    'owner': new_owner}
            )

            # Apply localy
            right_command.execute(self._graph)

            # Dispatch on clients
            self._item_to_push.put(right_command)

    def get(self, uuid=None, reference=None):
        """Get a node ReplicatedDatablock instance

        :param uuid: node uuid
        :type uuid: string
        :return: ReplicatedDatablock
        """
        target = None

        if uuid:
            target = self._graph.get(uuid)
        if reference:
            for k, v in self._graph.items():
                if reference == v.instance:
                    target = v
                    break

        return target

    def update_user_metadata(self, dikt):
        """Update user metadata

        Update local client informations to others (ex: localisation)

        :param json:
        :type dict:
        """
        assert(dikt)

        state_update_request = RepUpdateUserMetadata(
            owner=self._id,
            data=dikt
        )

        self._item_to_push.put(state_update_request)

    # TODO: remove
    def exist(self, uuid=None, reference=None):
        """Check for a node existence

        :param uuid: node uuid
        :type uuid: string
        :return: bool
        """
        if uuid:
            return uuid in self._graph.keys()
        if reference:
            for k, v in self._graph.items():
                if reference == v.instance:
                    return True

        return False

    # TODO: remove
    def list(self, filter=None, filter_owner=None):
        """List all graph nodes keys
        :param filter: node type
        :type filter: ReplicatedDatablock class (or child class)
        """
        base_list = self._graph.list(filter_type=filter)
        if filter_owner:
            return [key for key in base_list
                    if self._graph[key].owner == filter_owner]
        else:
            return base_list

    @property
    def state(self):
        """Get active session state
        0: STATE_INITIAL
        1: STATE_SYNCING
        2: STATE_ACTIVE

        :return: session state
        """
        return self._orchestrator.state

    @property
    def services_state(self):
        return self._orchestrator.services_state

    @property
    def online_users(self):
        return self._orchestrator.online_users

