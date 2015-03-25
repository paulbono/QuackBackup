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
class CustomTaskBarIcon(wx.TaskBarIcon):
    def __init__(self, frame, status_frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
 
        self.icon = wx.EmptyIcon()
        self.icon.CopyFromBitmap(wx.Bitmap("quack.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(self.icon)
 
        self.SetIcon(self.icon, "Restore")
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftClick)

    def OnTaskBarActivate(self, evt):
        pass

    def OnTaskBarClose(self, evt):
        self.frame.Close()
        self.status_frame.Close()

    def OnTaskBarLeftClick(self, evt):
        self.frame.Show()
        self.frame.Restore()
