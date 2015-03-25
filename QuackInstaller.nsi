
/* Quack Backup - Quack Backup will monitor a folder and sync it with a second folder.
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
along with this program.  If not, see <http://www.gnu.org/licenses/>. */

# define name of installer
OutFile "QuackInstaller.exe"
Name "Quack"
Caption "Quack"
XPStyle "on"
 
# define installation directory
InstallDir "C:\QuackBackup\"

# For removing Start Menu shortcut in Windows 7
RequestExecutionLevel user
 
# start default section
Section "install"
 
    # set the installation directory as the destination for the following actions
    SetOutPath $INSTDIR\cwRsync
    
    # Install Files
    File /r .\cwRsync
    
    SetOutPath $INSTDIR
    
    File .\dist\*
    File .\quack.ico
    File .\QuackBackup.cfg
    File .\README.txt
    File .\LICENSE
 
    # create the uninstaller
    WriteUninstaller "$INSTDIR\uninstall.exe"
 
    # create a shortcut named "new shortcut" in the start menu programs directory
    # point the new shortcut at the program uninstaller
    # CreateShortCut "$SMPROGRAMS\new shortcut.lnk" "$INSTDIR\uninstall.exe"
    
    # create a shortcut named "new shortcut" in the start menu programs directory
    # presently, the new shortcut doesn't call anything (the second field is blank)
    createShortCut "$SMPROGRAMS\QuackBackup.lnk" "$INSTDIR\Quack.exe"
 
SectionEnd
 
# create a section to define what the uninstaller does.
# the section will always be named "Uninstall"
Section "uninstall"
    # remove the link from the start menu
    Delete "$SMPROGRAMS\QuackBackup.lnk"
     
    # now delete installed files
    rmDir /r $INSTDIR/cwRsync
    rmDir $INSTDIR/cwRsync
    
    rmDir /r $INSTDIR
    Delete $INSTDIR/uninstall.exe
    rmDir $INSTDIR
SectionEnd
