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

import wx
import ConfigParser
import os
from backup import backup
from StatusFrame import StatusFrame
from CustomTaskBarIcon import CustomTaskBarIcon
from threading import *
from ConfigParser import ConfigParser

class MainFrame(wx.Frame):
    def __init__(self, status_frame):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Quack Backup", (-1, -1), wx.Size(300, 150))
        self.statusFrame = status_frame
        self.icon = wx.EmptyIcon()
        self.icon.CopyFromBitmap(wx.Bitmap("quack.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(self.icon)
        
        panel = wx.Panel(self, wx.ID_ANY)
        self.tbIcon = CustomTaskBarIcon(self, status_frame)
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_srcLabel = wx.StaticText(panel, wx.ID_ANY, u"Source Directory", wx.DefaultPosition, wx.DefaultSize)
        bSizer2.Add( self.m_srcLabel, 0, wx.EXPAND|wx.ALL, 1 )
        self.m_srcDir = wx.TextCtrl(panel, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize)
        bSizer2.Add( self.m_srcDir, 0, wx.ALL, 1 )
        self.m_srcDirSelect = wx.Button(panel, wx.ID_ANY, u"...", wx.DefaultPosition, wx.DefaultSize)
        bSizer2.Add( self.m_srcDirSelect, 0, wx.ALL, 1 )
        bSizer1.Add( bSizer2, 0, wx.ALL, 1)
        
        self.m_destLabel = wx.StaticText(panel, wx.ID_ANY, u"Destination Directory", wx.DefaultPosition, wx.DefaultSize)
        bSizer3.Add( self.m_destLabel, 0, wx.EXPAND|wx.ALL, 1 )
        self.m_destDir = wx.TextCtrl(panel, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize)
        bSizer3.Add( self.m_destDir, 0, wx.ALL, 1 )
        self.m_destDirSelect = wx.Button(panel, wx.ID_ANY, u"...", wx.DefaultPosition, wx.DefaultSize)
        bSizer3.Add( self.m_destDirSelect, 0, wx.ALL, 1 )
        bSizer1.Add( bSizer3, 0, wx.ALL, 1)
        
        self.m_processBackupButton = wx.Button( panel, wx.ID_ANY, u"Start Backup", wx.DefaultPosition, wx.DefaultSize)
        bSizer1.Add( self.m_processBackupButton, 0, wx.ALL, 1 )
        
        panel.SetSizer( bSizer1 )
        panel.Layout()
 
        self.Bind(wx.EVT_ICONIZE, self.onMinimize)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.m_processBackupButton.Bind( wx.EVT_BUTTON, self.processBackup )
        self.m_srcDirSelect.Bind( wx.EVT_BUTTON, self.selectSrcDir )
        self.m_destDirSelect.Bind( wx.EVT_BUTTON, self.selectDestDir )
        
        self.stop_backup_notify = wx.NotificationMessage(u"Quack Backup", u"Stopped", self)
        self.start_backup_notify = wx.NotificationMessage(u"Quack Backup", u"Running", self)
        
        self.running = False
        
        self.config_parser = ConfigParser()
        self.config_parser.read("QuackBackup.cfg")
        self.m_srcDir.SetValue(self.config_parser.get('PATHS', 'last_src'))
        self.m_destDir.SetValue(self.config_parser.get('PATHS', 'last_dest'))

        self.Show()
 
    def onClose(self, evt):
        self.tbIcon.RemoveIcon()
        self.tbIcon.Destroy()
        self.Destroy()
        self.statusFrame.Destroy()
 
    def onMinimize(self, event):
        self.Hide()
        
    def selectDir(self):
        path = None
        dialog = wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
        return path
        
    def selectSrcDir(self, event):
        path = self.selectDir()
        if path:
            self.m_srcDir.SetValue(path)
        
    def selectDestDir(self, event):
        path = self.selectDir()
        if path:
            self.m_destDir.SetValue(path)
        
    def processBackup(self, event):
        srcDir = self.m_srcDir.GetValue()+"\\"
        destDir = self.m_destDir.GetValue()+"\\"
        if destDir != "" and not os.path.exists(destDir):
            message = wx.MessageDialog(self, message="Destination does not exist, Create?", caption="Directory Missing", style=wx.YES_NO)
            if message.ShowModal() == wx.ID_YES:
                os.makedirs(destDir)

        if srcDir != "" and os.path.exists(srcDir) and destDir != "" and os.path.exists(destDir) and srcDir != destDir:
            self.config_parser.set('PATHS', 'last_src', "{}".format(self.m_srcDir.GetValue()))
            self.config_parser.set('PATHS', 'last_dest', "{}".format(self.m_destDir.GetValue()))
            with open('QuackBackup.cfg', 'wb') as configfile:
                self.config_parser.write(configfile)
            if self.running:
                self.running = False
                
                self.backup_task.stopBackup()
                self.backup_task = None
                self.m_processBackupButton.SetLabel(u"Start Backup")
                self.m_srcDir.Enable()
                self.m_srcDirSelect.Enable()
                self.m_destDir.Enable()
                self.m_destDirSelect.Enable()
            else:
                self.running = True
                
                self.backup_task = backup(self.statusFrame)
                t = Thread(target=self.backup_task.run, args=(self, srcDir, destDir))
                t.start()
                self.m_processBackupButton.SetLabel(u"Stop Backup")
                self.m_srcDir.Disable()
                self.m_srcDirSelect.Disable()
                self.m_destDir.Disable()
                self.m_destDirSelect.Disable()
                self.Hide()
        else:
            message = wx.MessageDialog(self, message="Check your Source and Destination directories.", caption="Directory Error", style=wx.OK)
            message.ShowModal()

def main():
    """"""
    app = wx.App(False)
    statusFrame = StatusFrame()
    frame = MainFrame(statusFrame)
    frame.Fit()
    frame.Show()
    app.SetTopWindow(frame)
    app.MainLoop()
 
if __name__ == "__main__":
    main()