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

import argparse
import sys
import os
from pathlib import Path
import logging
import cmd

# TODO: remove
replication_lib = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(str(replication_lib.parent))

from replication.network import ServerNetService
from replication.constants import CONNECTION_TIMEOUT

class ServerShell(cmd.Cmd):
    intro = 'Welcome the replication server shell.\n   Type help or ? to list commands.\n'
    prompt = '>> '
    file = None

    def __init__(
            self,
            port=5555,
            timeout=CONNECTION_TIMEOUT,
            password='None',
            attached=False):

        cmd.Cmd.__init__(self)
        self._net = ServerNetService()

        self._net.listen(
            port=port,
            password=password,
            attached=attached,
            timeout=timeout)
  
    def do_users(self, args):
        """ Print online users """
        print(f"{len(self._net.clients)} user online")
        for cli_id, cli_data in self._net.clients.items():
            role = 'admin' if cli_data['admin'] else ''
            print(f"{cli_data['id']}({role}) - {cli_data['latency']} ms")

    def do_kick(self, args):
        """ Kick the target user """
        self._net.kick(args)

    def do_exit(self, args):
        """ Exit the server """
        self._net.stop()
        return -1

    def do_EOF(self, args):
            print('*** EOF')
            return True

def cli():
    logging.basicConfig(format="%(message)s", level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=5560,
                        help="port to listen")
    parser.add_argument('-t', '--timeout', default=CONNECTION_TIMEOUT,
                        help="connection timeout in millisecond")
    parser.add_argument('-pwd', '--password', default='admin',
                        help="session admin password")

    parser.add_argument('--attached', 
                        help="server attached to a blender instance",
                        action='store_true')

    args = parser.parse_args()

    shell = ServerShell(
            port=int(args.port),
            timeout=int(args.timeout),
            password=str(args.password),
            attached=bool(args.attached)
        )
    try: 
        shell.cmdloop()
    except KeyboardInterrupt:
        shell.do_exit(None)

if __name__ == '__main__':
    cli()
