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
from backup import backup
from threading import *
from ConfigParser import ConfigParser

########################################################################
class CustomTaskBarIcon(wx.TaskBarIcon):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, frame):
        """Constructor"""
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
 
        self.icon = wx.EmptyIcon()
        self.icon.CopyFromBitmap(wx.Bitmap("quack.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(self.icon)
 
        self.SetIcon(self.icon, "Restore")
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftClick)

    #----------------------------------------------------------------------
    def OnTaskBarActivate(self, evt):
        """"""
        pass

    #----------------------------------------------------------------------
    def OnTaskBarClose(self, evt):
        """
        Destroy the taskbar icon and frame from the taskbar icon itself
        """
        self.frame.Close()

    #----------------------------------------------------------------------
    def OnTaskBarLeftClick(self, evt):
        """
        Create the right-click menu
        """
        self.frame.Show()
        self.frame.Restore()

########################################################################
class MainFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, id):
        """Constructor"""
        wx.Frame.__init__(self, None, id, "Quack Backup", (-1, -1), wx.Size(300, 150))
        self.icon = wx.EmptyIcon()
        self.icon.CopyFromBitmap(wx.Bitmap("quack.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(self.icon)
        
        panel = wx.Panel(self, -1)
        self.tbIcon = CustomTaskBarIcon(self)
        
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
        
        #self.m_cousin_trust = wx.StaticText(panel, wx.ID_ANY, u"Cousin Trust", wx.DefaultPosition, wx.DefaultSize)
        #bSizer1.Add( self.m_cousin_trust, 0, wx.EXPAND|wx.ALL, 1 )
        
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
 
    #----------------------------------------------------------------------
    def onClose(self, evt):
        """
        Destroy the taskbar icon and the frame
        """
        self.tbIcon.RemoveIcon()
        self.tbIcon.Destroy()
        self.Destroy()
 
    #----------------------------------------------------------------------
    def onMinimize(self, event):
        """
        When minimizing, hide the frame so it "minimizes to tray"
        """
        self.Hide()
        
    def selectDir(self):
        path = None
        dialog = wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
        dialog.Destroy()
        return path
        
    def selectSrcDir(self, event):
        path = self.selectDir()
        if path:
            self.m_srcDir.SetValue(path)
            self.config_parser.set('PATHS', 'last_src', "{}".format(path))
            with open('QuackBackup.cfg', 'wb') as configfile:
                self.config_parser.write(configfile)
                configfile.close()
        
    def selectDestDir(self, event):
        path = self.selectDir()
        if path:
            self.m_destDir.SetValue(path)
            self.config_parser.set('PATHS', 'last_dest', "{}".format(path))
            with open('QuackBackup.cfg', 'wb') as configfile:
                self.config_parser.write(configfile)
                configfile.close()
        
    def processBackup(self, event):
        srcDir = self.m_srcDir.GetValue()+"\\"
        destDir = self.m_destDir.GetValue()+"\\"
        if srcDir != "" and destDir != "":
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
                
                self.backup_task = backup()
                t = Thread(target=self.backup_task.run, args=(self, srcDir, destDir))
                t.start()
                self.m_processBackupButton.SetLabel(u"Stop Backup")
                self.m_srcDir.Disable()
                self.m_srcDirSelect.Disable()
                self.m_destDir.Disable()
                self.m_destDirSelect.Disable()
                self.Hide()
 
#----------------------------------------------------------------------
def main():
    """"""
    app = wx.App(False)
    frame = MainFrame(1)
    app.MainLoop()
 
if __name__ == "__main__":
    main()