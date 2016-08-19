import wx


class averaging_txtctrl(wx.TextCtrl):
    """Input TxtCtrl for adjusting number of passes for averaging."""
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
        """Update the number of averages set by the user."""
        try:
            newval = max(1, int(self.GetValue()))
        except ValueError:
            self.set_value()
            return

        if newval != self.frame.tb.pending_cfg.n_averages:
            self.frame.tb.pending_cfg.n_averages = newval
            self.frame.tb.reconfigure()

        self.set_value()

    def set_value(self):
        self.SetValue(str(self.frame.tb.pending_cfg.n_averages))


class ctrls(object):
    def __init__(self, frame):
        """Initialize gui controls for number of passes for averaging."""
        box = wx.StaticBox(frame, wx.ID_ANY, "# of DFT Avgs")
        self.averaging_txtctrl = averaging_txtctrl(frame)
        self.layout = wx.StaticBoxSizer(box, wx.VERTICAL)
        self.layout.Add(self.averaging_txtctrl, flag=wx.ALL, border=5)
