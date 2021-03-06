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

import os
import time
import sys
import subprocess
import wx
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler
from ConfigParser import ConfigParser
from threading import *

rsync_loc = os.getcwd() + '/cwRsync/rsync.exe'
cygpath_loc = os.getcwd() + '/cwRsync/cygpath.exe'
chmod_loc = os.getcwd() + '/cwRsync/chmod.exe'

config = ConfigParser()
config.read('QuackBackup.cfg')

rsync_flags = config.get('RSYNC', 'rsync_flags')
dry_rsync_flags = config.get('RSYNC', 'dry_rsync_flags')

si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

class MyHandler(PatternMatchingEventHandler):
    def __init__(self, parent_frame, status_frame, src_loc, dest_loc):
        PatternMatchingEventHandler.__init__(self)
        self.parent_frame = parent_frame
        self.statusFrame = status_frame
        self.dest_loc = dest_loc
        patterns=["*"]
        self.backup_in_progress = False
        
        # First sync files that may have been modified while we were not running
        self.trigger_event(src_loc)

    def process(self, trigger_path):
        try:
            command = '{} {}'.format(cygpath_loc, trigger_path)
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si, shell=False)
            (stdoutdata, stderrdata) =  proc.communicate()
            cyg_formatted_path = os.path.dirname(stdoutdata.rstrip().replace("\n"," "))
            try:
                command = '{} {} \'{}/\' \'{}\''.format(rsync_loc, dry_rsync_flags, cyg_formatted_path, self.dest_loc)
                proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si, shell=False)
                (stdoutdata, stderrdata) =  proc.communicate()
                dry_output = stdoutdata
            except:
                dry_output = 0
                print "dry output check failed"
                pass

            if len(dry_output.split("\n")) > 5:
                self.statusFrame.Show()
            while( len(dry_output.split("\n")) > 5 ):
                try:
                    command = '{} {} \'{}/\' \'{}\''.format(rsync_loc, rsync_flags, cyg_formatted_path, self.dest_loc)
                    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si, shell=False)
                    times = 0

                    while proc.poll() is None:
                        line = proc.stdout.readline()
                        self.statusFrame.addStatus(line)
                        times += 1
                        if (not line and times >= 5):
                            break
                    proc.wait()
                except:
                    pass
                try:
                    command = '{} {} \'{}/\' \'{}\''.format(rsync_loc, dry_rsync_flags, cyg_formatted_path, self.dest_loc)
                    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si, shell=False)
                    (stdoutdata, stderrdata) =  proc.communicate()
                    dry_output = stdoutdata
                except:
                    print "dry output check failed"
                    pass
            t = Thread(target=self.statusFrame.stopOnTimeout)
            t.start()
            self.backup_in_progress = False
        except:
            pass

    def on_any_event(self, event):
        self.trigger_event(event.src_path)
        
    def trigger_event(self, trigger_path):
        if not self.backup_in_progress :
            command = '{} {}'.format(cygpath_loc, trigger_path)
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si, shell=False)
            (stdoutdata, stderrdata) =  proc.communicate()
            cyg_formatted_path = os.path.dirname(stdoutdata.rstrip().replace("\n"," "))
            try:
                command = '{} {} \'{}/\' \'{}\''.format(rsync_loc, dry_rsync_flags, cyg_formatted_path, self.dest_loc)
                proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si, shell=False)
                (stdoutdata, stderrdata) =  proc.communicate()
                dry_output = stdoutdata
            except:
                dry_output = 0
                print "dry output check failed"
                pass
            if not (len(dry_output.split("\n")) <= 5):
                self.backup_in_progress = True
                self.process(trigger_path)
    
class backup():
    def stopBackup(self):
        self.alive = False
        
    def __init__(self, status_frame):
        self.alive = True
        self.statusFrame = status_frame
        
    def run(self, parent_frame, observe_path, dest_loc):
        command = '{} {}'.format(cygpath_loc, dest_loc)
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si, shell=False)
        (stdoutdata, stderrdata) =  proc.communicate()
        self.dest_loc = os.path.dirname(stdoutdata.rstrip().replace("\n"," "))
        command = '{} {}'.format(cygpath_loc, observe_path)
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si, shell=False)
        (stdoutdata, stderrdata) =  proc.communicate()
        self.observe_path = os.path.dirname(stdoutdata.rstrip().replace("\n"," "))
        self.observer = Observer()
        self.observer.schedule(MyHandler(parent_frame, self.statusFrame, observe_path, self.dest_loc), path=observe_path, recursive=True)
        self.observer.start()

        try:
            while self.alive:
                time.sleep(1)
            self.observer.stop()
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()
        