import wx


class windowfn_dropdown(wx.ComboBox):
    """Dropdown for selecting available windowing functions."""
    def __init__(self, frame):
        self.frame = frame

        window_strs = self.frame.tb.cfg.windows.keys()
        wx.ComboBox.__init__(self,
                             frame,
                             id=wx.ID_ANY,
                             choices=sorted(window_strs),
                             style=wx.CB_READONLY)

        # Size the dropdown based on longest string
        _, height = self.GetSize()
        dc = wx.ClientDC(self)
        tsize = max(dc.GetTextExtent(s)[0] for s in window_strs)
        self.SetMinSize((tsize+50, height))

        self.SetStringSelection(self.frame.tb.cfg.window)
        self.Bind(wx.EVT_COMBOBOX, self.update)

    def update(self, event):
        """Set the window function selected by the user via dropdown."""
        self.frame.tb.pending_cfg.set_window(self.GetValue())
        self.frame.tb.reconfigure()


class ctrls(object):
    def __init__(self, frame):
        """Initialize gui controls for window function."""
        windowfn_box = wx.StaticBox(frame, wx.ID_ANY, "Window")
        self.windowfn_dropdown = windowfn_dropdown(frame)
        self.layout = wx.StaticBoxSizer(windowfn_box, wx.VERTICAL)
        self.layout.Add(self.windowfn_dropdown, flag=wx.ALL, border=5)
