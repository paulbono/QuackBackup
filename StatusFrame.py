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
import time
import re
import win32gui
from timer import timer

class StatusFrame(wx.Frame):
    def __init__(self, parent_frame=None):
        self.w=win32gui
        dw, dh =  wx.GetClientDisplayRect().GetBottomRight()
        w, h = (400, 150)
        x = dw - w
        y = dh - h
        statusFrameStyle = wx.DEFAULT_FRAME_STYLE^(wx.CLOSE_BOX|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX)| wx.STAY_ON_TOP|wx.FRAME_NO_TASKBAR|wx.FRAME_TOOL_WINDOW|wx.FRAME_SHAPED
        wx.Frame.__init__(self, parent_frame, wx.ID_ANY, "Backup Status", (x, y), wx.Size(w, h), style = statusFrameStyle )
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.bSizer1 = wx.BoxSizer( wx.VERTICAL )
        self.m_StatusOutput = wx.TextCtrl(self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE)
        self.bSizer1.Add( self.m_StatusOutput, 1, wx.ALL|wx.EXPAND, 5 )
        self.panel.SetSizer( self.bSizer1 )
        self.panel.Layout()
        self.timer = timer(3)

    def addStatus(self, message):
        if message.rstrip() != "":
            self.m_StatusOutput.AppendText(message)
            self.m_StatusOutput.Refresh()
            if re.match('total size is .* speedup is .*', message):
                self.timer.restart()
            elif message == './':
                self.timer.cancel()
            
    def stopOnTimeout(self):
        while not self.timer.isExpired():
            pass
        while "Backup Status" == self.w.GetWindowText(self.w.GetForegroundWindow()):
            pass
        self.m_StatusOutput.SetValue(wx.EmptyString)
        self.HideWithEffect(wx.SHOW_EFFECT_BLEND, 1000)