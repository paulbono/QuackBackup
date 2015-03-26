# Quack Backup - Quack Backup will monitor a folder and sync it with a second folder.
# Copyright (C) 2015  Paul Bono

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
from threading import *

class timer(Thread):
    def __init__(self, timeout):
        Thread.__init__(self)
        self.timeout = timeout
        self.expired = False
        self.running = False

    def start(self):
        self.running = True
        self.expired = False
        self.startTime = time.time()
        time.clock()    
        elapsed = 0
        while elapsed < self.timeout:
            elapsed = time.time() - self.startTime
            time.sleep(1)
        self.expired = True
        self.running = False

    def restart(self):
        self.startTime=time.time()
        if not self.running:
            self.t = Thread(target=self.start)
            self.t.start()
        
    def isExpired(self):
        self.t.join()
        return self.expired