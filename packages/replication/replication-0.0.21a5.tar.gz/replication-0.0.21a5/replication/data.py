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
from deepdiff import DeepDiff, Delta
import json
import marshal
import io
import time
from enum import Enum
from uuid import uuid4
import sys
import zmq
import math
import pickle
import traceback

from .constants import (
    ADDED, COMMITED,
    FETCHED, UP, ERROR, MODIFIED, DIFF_BINARY, DIFF_JSON)
from .exception import NetworkFrameError


CHUNK_SIZE = 2500000000


class ReplicatedDataFactory(object):
    """
    Manage the data types implementations.

    """

    def __init__(self):
        self.supported_types = []

    def register_type(
            self,
            source_type,
            implementation,
            timer=0,
            automatic=False):
        """
        Register a new replicated datatype implementation
        """
        self.supported_types.append(
            (source_type, implementation, timer, automatic))

    def match_type_by_instance(self, data):
        """
        Find corresponding type to the given datablock
        """
        for stypes, implementation, time, auto in self.supported_types:
            if isinstance(data, stypes):
                return implementation
        logging.error(f"{data} not supported for replication")

    def match_type_by_name(self, type_name):
        for stypes, implementation, time, auto in self.supported_types:
            if type_name == implementation.__name__:
                return implementation
        logging.error(f"{type_name} not supported for replication")

    def get_implementation_from_object(self, data):
        return self.match_type_by_instance(data)

    def get_implementation_from_net(self, type_name):
        """
        Re_construct a new replicated value from serialized data
        """
        return self.match_type_by_name(type_name)


class ReplicatedDatablock(object):
    """
    Datablock definition that handle object replication logic.
    PUSH: send the object over the wire
    STORE: register the object on the given replication graph
    LOAD: apply loaded changes by reference on the local copy
    DUMP: get local changes

    """
    uuid = None     # uuid used as key      (string)
    instance = None  # dcc data ref          (DCC type)
    data = None   # raw data              (json)
    str_type = None  # data type name        (string)
    dependencies = [None]   # dependencies array    (string)
    owner = None    # Data owner            (string)
    state = None    # Data state            (RepState)
    buffer = None  # Serialized buffer
    diff_method = DIFF_JSON

    def __init__(
            self,
            owner=None,
            instance=None,
            str_type=None,
            uuid=None,
            data=None,
            bytes=None,
            sender=None,
            dependencies=[]):

        self.uuid = uuid if uuid else str(uuid4())
        self.owner = owner
        self.str_type = type(self).__name__
        self.buffer = None

        if instance:
            self.state = ADDED
            self.instance = instance
        elif data:
            self.data = data
            self.state = COMMITED
        elif bytes:
            # Server side
            if type(self) == ReplicatedDatablock:
                self.state = UP
                self.str_type = str_type
                self.data = bytes  # Storing data as raw bytes on server side

            # Client side
            else:
                try:
                    self.data = self._deserialize(bytes)
                    self.state = FETCHED
                except ValueError as e:
                    logging.error(f"Failed to load {self.str_type} :\n Incompatible data received, maybe an unsuported addon...")
                    self.state = ERROR
        self.dependencies = dependencies
        self.sender = sender

    def commit(self):
        # TMP for investigation
        # assert(self.instance and
        #        self.state in [MODIFIED, ADDED, UP])
        if self.state not in [MODIFIED, ADDED, UP]:
            return

        try:
            self.data = self._dump(instance=self.instance)
            self.state = COMMITED
        except ReferenceError:
            logging.error("Lost reference, trying to resolve the datablocks.")
            self.resolve()
        except Exception:
            logging.error(f"{self.str_type} commit error:  failed: \n {traceback.format_exc()}")
            self.state = ERROR

    def push(self, socket, identity=None):
        """
        Here send data over the wire:
            - _serialize the data
            - send them as a multipart frame thought the given socket
        """

        if self.state in [COMMITED, UP]:
            data = self.data if type(self.data) == bytes else self.buffer

            assert(data)

            owner = self.owner.encode()
            key = self.uuid.encode()
            rep_type = self.str_type.encode()
            dependencies = pickle.dumps(self.dependencies)

            # Determine chunk numbers
            ck_number = math.ceil(sys.getsizeof(data)/CHUNK_SIZE)

            # Server to specific Client case
            if identity:
                socket.send(identity, zmq.SNDMORE)

            # First step : send nodes metadata
            socket.send_multipart(
                [socket.IDENTITY, key, owner, rep_type, pickle.dumps(ck_number), dependencies])

            # Second step: stream data chunks
            stream = io.BytesIO(data)

            for i in range(ck_number):
                chunk = stream.read(CHUNK_SIZE)
                if identity:
                    socket.send(identity, zmq.SNDMORE)
                socket.send_multipart([chunk])

            stream.close()
            # self.buffer = None
            self.state = UP
        else:
            logging.error(f"Attempting to push uncomited node {self.str_type}")

    @classmethod
    def fetch(cls, socket, factory=None):
        """
        Here we reeceive data from the wire:
            - read data from the socket
            - reconstruct an instance
        """

        frame = socket.recv_multipart(0)
        
        # identity, uuid, owner, str_type, ck_number, dependencies
        # Load node metadata
        if len(frame) != 6:
            logging.error("Incomplete frame received")
            raise NetworkFrameError("Error fetching data")

        identity = frame[0]
        uuid = frame[1].decode()
        owner = frame[2].decode()
        str_type = frame[3].decode()
        ck_number = pickle.loads(frame[4])     
        dependencies = pickle.loads(frame[5])
        dependencies = dependencies if dependencies else None

        # Rebuild data from chunks
        data = bytes()
        for i in range(ck_number):
            chunk_frame = socket.recv_multipart()
            data += chunk_frame[0]

        # Server side replication
        if factory is None:
            return ReplicatedDatablock(
                owner=owner,
                uuid=uuid,
                dependencies=dependencies,
                sender=identity,
                str_type=str_type,
                bytes=data)

        # Client side replication
        else:
            implementation = factory.get_implementation_from_net(str_type)

            return implementation(
                owner=owner,
                uuid=uuid,
                dependencies=dependencies,
                bytes=data)

    def apply(self):
        """Apply stored data into the DCC
        """
        # UP in case we want to reset our instance data
        assert(self.state in [FETCHED, UP])
        logging.debug(f"Applying {self.uuid} - {self.str_type}")

        if self.instance is None:
            self.resolve()

        try:
            self._load(data=self.data, target=self.instance)
            self.state = UP
        except Exception as e:
            logging.error(f"Load {self.uuid} failed: \n {traceback.format_exc()}")

    def is_valid(self):
        raise NotImplementedError

    def _construct(self, data=None):
        """Construct a new instance of the target object,
        assign our instance to this instance
        """
        raise NotImplementedError

    def resolve(self):
        pass

    def store(self, dict):
        """
        Store the node into the given dict
        """
        if self.uuid is not None:
            if self.uuid in dict:
                dict[self.uuid].data = self.data
                dict[self.uuid].state = self.state
                dict[self.uuid].dependencies = self.dependencies
            else:
                dict[self.uuid] = self

            return self.uuid

    def _deserialize(self, data):
        """
        BUFFER -> JSON
        """
        return marshal.loads(data)

    def _serialize(self):
        """
        JSON -> BUFFER
        """
        self.buffer = marshal.dumps(self.data)

    def _dump(self, instance=None):
        """
        DCC -> JSON
        """
        assert(instance)

        return json.dumps(instance)

    def _load(self, data=None, target=None):
        """
        JSON -> DCC
        """
        raise NotImplementedError

    def diff(self):
        """Compare stored data to the actual one.

        return True if the versions doesn't match
        """
        new_version = self._dump(instance=self.instance)
        if self.diff_method == DIFF_JSON:
            diff = DeepDiff(self.data, new_version, cache_size=5000)
        elif self.diff_method == DIFF_BINARY:
            diff = self.buffer != marshal.dumps(new_version)

        if diff:
            logging.debug(f"Found a diff on {self.uuid} ({self.str_type}): \n {diff}")
            self.state = MODIFIED
            return True
        return False

    def resolve_deps(self):
        """Return a list of dependencies
        """
        return []

    def add_dependency(self, dependency):
        if not self.dependencies:
            self.dependencies = []
        if dependency not in self.dependencies:
            self.dependencies.append(dependency)

    def __repr__(self):
        return f"\n {self.uuid} - owner: {self.owner} - type: {self.str_type}"


class ReplicatedCommandFactory(object):
    """
    Manage the data types implementations.

    """

    def __init__(self):
        self.supported_types = []

        self.register_type(RepDeleteCommand, RepDeleteCommand)
        self.register_type(RepRightCommand, RepRightCommand)
        self.register_type(RepConfigCommand, RepConfigCommand)
        self.register_type(RepSnapshotCommand, RepSnapshotCommand)
        self.register_type(RepServerSnapshotCommand, RepServerSnapshotCommand)
        self.register_type(RepAuthCommand, RepAuthCommand)
        self.register_type(RepDisconnectCommand, RepDisconnectCommand)
        self.register_type(RepKickCommand, RepKickCommand)
        self.register_type(RepUpdateClientsState, RepUpdateClientsState)
        self.register_type(RepUpdateUserMetadata, RepUpdateUserMetadata)

    def register_type(
            self,
            source_type,
            implementation):
        """
        Register a new replicated datatype implementation
        """
        self.supported_types.append(
            (source_type, implementation))

    def match_type_by_name(self, type_name):
        for stypes, implementation in self.supported_types:
            if type_name == implementation.__name__:
                return implementation
        logging.error(f"{type_name} not supported for replication")

    def get_implementation_from_object(self, data):
        return self.match_type_by_instance(data)

    def get_implementation_from_net(self, type_name):
        """
        Re_construct a new replicated value from serialized data
        """
        return self.match_type_by_name(type_name)


class ReplicatedCommand():
    def __init__(
            self,
            owner=None,
            data=None):
        assert(owner)

        self.owner = owner
        self.data = data
        self.str_type = type(self).__name__

    def push(self, socket):
        """
        Here send data over the wire:
            - _serialize the data
            - send them as a multipart frame thought the given socket
        """
        data = pickle.dumps(self.data)
        owner = self.owner.encode()
        type = self.str_type.encode()

        socket.send_multipart([owner, type, data])

    @classmethod
    def fetch(cls, socket, factory=None):
        """
        Here we reeceive data from the wire:
            - read data from the socket
            - reconstruct an instance
        """

        owner, str_type, data = socket.recv_multipart(0)

        str_type = str_type.decode()
        owner = owner.decode()
        data = pickle.loads(data)

        implementation = factory.get_implementation_from_net(str_type)

        instance = implementation(owner=owner, data=data)
        return instance

    @classmethod
    def server_fetch(cls, socket, factory=None):
        """
        Here we reeceive data from the wire:
            - read data from the socket
            - reconstruct an instance
        """
        instance = None
        frame = socket.recv_multipart(0)

        if len(frame) != 4:
            logging.error(f"Malformed command frame received (len: {len(frame)}/4) ")
        else:
            str_type = frame[2].decode()
            owner = frame[1].decode()
            data = pickle.loads(frame[3])

            implementation = factory.get_implementation_from_net(str_type)

            instance = implementation(owner=owner, data=data)
            instance.sender = frame[0]

        return instance

    def execute(self, graph):
        raise NotImplementedError


class RepDeleteCommand(ReplicatedCommand):
    def execute(self, graph):
        assert(self.data)

        if graph and self.data in graph.keys():
            # Clean all reference to this node
            for key, value in graph.items():
                if value.dependencies and self.data in value.dependencies:
                    value.dependencies.remove(self.data)
            # Remove the node itself
            del graph[self.data]


class RepRightCommand(ReplicatedCommand):
    def execute(self, graph):
        assert(self.data)

        if graph and self.data['uuid'] in graph.keys():
            graph[self.data['uuid']].owner = self.data['owner']


class RepConfigCommand(ReplicatedCommand):
    pass


class RepSnapshotCommand(ReplicatedCommand):
    pass


class RepServerSnapshotCommand(ReplicatedCommand):
    pass


class RepAuthCommand(ReplicatedCommand):
    pass


class RepDisconnectCommand(ReplicatedCommand):
    pass


class RepKickCommand(ReplicatedCommand):
    pass


class RepUpdateClientsState(ReplicatedCommand):
    pass


class RepUpdateUserMetadata(ReplicatedCommand):
    pass
