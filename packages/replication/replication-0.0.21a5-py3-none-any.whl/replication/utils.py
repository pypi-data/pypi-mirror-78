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


import time
import os

try:
    import psutil
    print('psutil available')
    psutil_available=True
except ImportError:
    psutil_available=False


def current_milli_time():
    """ Retrieve current time in millisecond """
    return int(round(time.time() * 1000))

def assert_parent_process_running():
    """ 
        Check if the parent process is alive, 
        if not it kill the child
    """
    if psutil_available:
        try:
            psutil.Process(os.getppid())
        except psutil.NoSuchProcess:
            p = psutil.Process(os.getpid())
            p.kill()