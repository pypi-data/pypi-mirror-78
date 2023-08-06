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
import threading
import time

import zmq

from .service import Service
from .data import ReplicatedCommand, RepDeleteCommand, ReplicatedDatablock
from .graph import ReplicationGraph
from .constants import (MODIFIED, STATE_INITIAL,
                        STATE_ACTIVE, UP, RP_COMMON, RP_STRICT)


class Observer(Service):
    def __init__(
            self,
            ipc_port=None,
            store_reference=None,
            watched_type=None,
            timeout=2,
            automatic=False,
            session_instance=None,
            context=zmq.Context.instance()):

        # Threading
        Service.__init__(
            self,
            ipc_port=ipc_port,
            name= f"{str(watched_type.__name__)}_watchdog"
        )

        self._timeout = timeout
        self._watched_type = watched_type
        self._exit_event = threading.Event()
        self._repo = store_reference
        self._automatic = automatic
        self._state = STATE_INITIAL
        self._session = session_instance
        self._local_user = self._session._id
        self._loop_interval = timeout # TODO: remove this.

        self.start()

    def main(self, socket):
        if self._watched_type.__name__ in ['BlCollection', 'BlScene']:
            keys_to_check = [k for k in self._session.list(filter=self._watched_type)
                                if self._session.get(uuid=k).owner in [RP_COMMON, self._local_user]]
        else:
            keys_to_check = self._session.list(
                filter_owner=self._local_user, filter=self._watched_type)

        for key in keys_to_check:
            node = self._repo[key]

            if node.state == UP:
                try:
                    if node.diff() and self._automatic:
                            self._session.commit(node.uuid)
                            self._session.push(node.uuid)
                except ReferenceError:
                    node.resolve()

                    if not node.is_valid():
                        self._session.remove(node.uuid)
                except Exception as e:
                    logging.debug(e)
                    continue

    def stop(self):
        pass