import wx


class nframes_txtctrl(wx.TextCtrl):
    """Input TxtCtrl for adjusting number of frames passed to detector."""
    def __init__(self, frame):
        wx.TextCtrl.__init__(self,
                             frame,
                             id=wx.ID_ANY,
                             size=(60, -1),
                             style=wx.TE_PROCESS_ENTER)

        self.frame = frame
        self.Bind(wx.EVT_KILL_FOCUS, self.update)
        self.Bind(wx.EVT_TEXT_ENTER, self.update)
        self.set_value()

    def update(self, event):
        """Update the number of frames set by the user."""
        try:
            newval = max(1, int(self.GetValue()))
        except ValueError:
            self.set_value()
            return

        if newval != self.frame.tb.pending_cfg.nframes:
            self.frame.tb.pending_cfg.nframes = newval
            self.frame.tb.reconfigure()

        self.set_value()

    def set_value(self):
        self.SetValue(str(self.frame.tb.pending_cfg.nframes))


class ctrls(object):
    def __init__(self, frame):
        """Initialize gui controls for number of detectected frames."""
        box = wx.StaticBox(frame, wx.ID_ANY, "No. of DFTs")
        self.nframes_txtctrl = nframes_txtctrl(frame)
        self.layout = wx.StaticBoxSizer(box, wx.VERTICAL)
        self.layout.Add(self.nframes_txtctrl, flag=wx.ALL, border=5)
