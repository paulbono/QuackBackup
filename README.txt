Quack Backup - Quack Backup will monitor a folder and sync it with a second folder.
Copyright (C) 2015  Paul Bono

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

v0.5b
Quack Backup will monitor a folder and sync it with a second folder.

FAQ:
Is it portable?
    Yeah just extract the installer to its own subdir or after installing you can copy the dir at C:\QuackBackup
Why install it?
    I put a nice shortcut in your start menu

Todo:
Notifications
Something breaks when deleting all files & folders
Fix when folder doesn't exist or is the same

Known issues:
AVG (maybe others) detects cwRsync as a power user tool/vulnerability
Python crashes when copying lots of files into directory extremely fast (maybe not an issue, seems abusive)
Syncing a folder to itself will upset the program so much that you'll need to close it and reopen it if you want it to continue syncing a folder.

Credit to other tools:
GPL v3
cwRsync
cygwin
rSync
putty
py2exe
python watchdog
wxPython
Nullsoft Scriptable Install System (NSIS)