
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
    File .\cwRsync\cwrsync.cmd
    File .\cwRsync\cygcrypto-1.0.0.dll
    File .\cwRsync\cyggcc_s-1.dll
    File .\cwRsync\cygiconv-2.dll
    File .\cwRsync\cygssp-0.dll
    File .\cwRsync\cygwin1.dll
    File .\cwRsync\cygz.dll
    File .\cwRsync\README.cwrsync.txt
    File .\cwRsync\README.rsync.txt
    File .\cwRsync\rsync.exe
    File .\cwRsync\rsync.html
    File .\cwRsync\rsyncd.conf.html
    File .\cwRsync\ssh.exe
    File .\cwRsync\ssh-keygen.exe
    File .\cwRsync\puttygen.exe
    File .\cwRsync\plink.exe
    File .\cwRsync\chmod.exe
    File .\cwRsync\cygpath.exe
    
    SetOutPath $INSTDIR
    
    File .\dist\_ctypes.pyd
    File .\dist\_hashlib.pyd
    File .\dist\bz2.pyd
    File .\dist\python27.dll
    File .\dist\Quack.exe
    File .\dist\select.pyd
    File .\dist\unicodedata.pyd
    File .\dist\w9xpopen.exe
    File .\dist\wx._controls_.pyd
    File .\dist\wx._core_.pyd
    File .\dist\wx._gdi_.pyd
    File .\dist\wx._misc_.pyd
    File .\dist\wx._windows_.pyd
    File .\dist\wxbase30u_net_vc90.dll
    File .\dist\wxbase30u_vc90.dll
    File .\dist\wxmsw30u_adv_vc90.dll
    File .\dist\wxmsw30u_core_vc90.dll
    File .\dist\wxmsw30u_html_vc90.dll
    File .\quack.ico
    File .\QuackBackup.cfg
 
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
     
    # now delete installed file
    Delete $INSTDIR\cwRsync\cwrsync.cmd
    Delete $INSTDIR\cwRsync\cygcrypto-1.0.0.dll
    Delete $INSTDIR\cwRsync\cyggcc_s-1.dll
    Delete $INSTDIR\cwRsync\cygiconv-2.dll
    Delete $INSTDIR\cwRsync\cygssp-0.dll
    Delete $INSTDIR\cwRsync\cygwin1.dll
    Delete $INSTDIR\cwRsync\cygz.dll
    Delete $INSTDIR\cwRsync\README.cwrsync.txt
    Delete $INSTDIR\cwRsync\README.rsync.txt
    Delete $INSTDIR\cwRsync\rsync.exe
    Delete $INSTDIR\cwRsync\rsync.html
    Delete $INSTDIR\cwRsync\rsyncd.conf.html
    Delete $INSTDIR\cwRsync\ssh.exe
    Delete $INSTDIR\cwRsync\ssh-keygen.exe
    Delete $INSTDIR\cwRsync\puttygen.exe
    Delete $INSTDIR\cwRsync\plink.exe
    Delete $INSTDIR\cwRsync\chmod.exe
    Delete $INSTDIR\cwRsync\cygpath.exe
    
    rmDir $INSTDIR\cwRsync
    
    Delete $INSTDIR\_ctypes.pyd
    Delete $INSTDIR\_hashlib.pyd
    Delete $INSTDIR\bz2.pyd
    Delete $INSTDIR\python27.dll
    Delete $INSTDIR\Quack.exe
    Delete $INSTDIR\select.pyd
    Delete $INSTDIR\unicodedata.pyd
    Delete $INSTDIR\w9xpopen.exe
    Delete $INSTDIR\wx._controls_.pyd
    Delete $INSTDIR\wx._core_.pyd
    Delete $INSTDIR\wx._gdi_.pyd
    Delete $INSTDIR\wx._misc_.pyd
    Delete $INSTDIR\wx._windows_.pyd
    Delete $INSTDIR\wxbase30u_net_vc90.dll
    Delete $INSTDIR\wxbase30u_vc90.dll
    Delete $INSTDIR\wxmsw30u_adv_vc90.dll
    Delete $INSTDIR\wxmsw30u_core_vc90.dll
    Delete $INSTDIR\wxmsw30u_html_vc90.dll
    Delete $INSTDIR\quack.ico
    Delete $INSTDIR\QuackBackup.cfg
    Delete $INSTDIR\quack.exe.log
    
    Delete $INSTDIR\uninstall.exe
    rmDir $INSTDIR
SectionEnd
