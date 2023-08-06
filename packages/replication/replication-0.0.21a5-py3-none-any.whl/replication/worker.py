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

from .graph import ReplicationGraph
from .service import Service

class TaskExecutor(Service):
    def __init__(
            self,
            ipc_port=None,
            tasks=None,
            graph=None,
            push_queue=None):
        
        Service.__init__(
            self,
            ipc_port=ipc_port,
            name='TaskExecutor')
        
        self._graph = graph
        self._tasks = tasks
        self._push_queue = push_queue
        
        self.start()

    def main(self, sockets):
        if not self._tasks.empty():
            task_type, task_target = self._tasks.get_nowait()

            if task_type == 'COMMIT':
                self._graph[task_target].commit()
            elif task_type == 'COMMAND':
                self._push_queue.put(task_target)
            elif task_type == 'PUSH':
                node = self._graph.get(task_target)
                node._serialize()
                self._push_queue.put(node)

    def stop(self):
        self._state = 0
        

