REM Quack Backup - Quack Backup will monitor a folder and sync it with a second folder.
REM Copyright (C) 2015  Paul Bono

REM This program is free software: you can redistribute it and/or modify
REM it under the terms of the GNU General Public License as published by
REM the Free Software Foundation, either version 3 of the License, or
REM (at your option) any later version.

REM This program is distributed in the hope that it will be useful,
REM but WITHOUT ANY WARRANTY; without even the implied warranty of
REM MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
REM GNU General Public License for more details.

REM You should have received a copy of the GNU General Public License
REM along with this program.  If not, see <http://www.gnu.org/licenses/>.

echo BUILDING EXE
setup.py
echo BUILDING INSTALLER
"C:\Program Files (x86)\NSIS\makensis.exe" QuackInstaller.nsi
echo INSTALLIING
QuackInstaller.exe /S
echo DONE