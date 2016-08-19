import wx


class tune_delay_txtctrl(wx.TextCtrl):
    """Input TxtCtrl for adjusting number of disgarded samples."""
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
        """Update the samples to tune_delay set by the user."""
        try:
            newval = max(0, int(self.GetValue()))
        except ValueError:
            self.set_value()
            return

        if newval != self.frame.tb.pending_cfg.tune_delay:
            self.frame.tb.pending_cfg.tune_delay = newval
            self.frame.tb.reconfigure()

        self.set_value()

    def set_value(self):
        self.SetValue(str(self.frame.tb.pending_cfg.tune_delay))


class ctrls(object):
    def __init__(self, frame):
        """Initialize gui controls for number samples to delay initially."""
        box = wx.StaticBox(frame, wx.ID_ANY, "Tune Delay")
        self.tune_delay_txtctrl = tune_delay_txtctrl(frame)
        self.layout = wx.StaticBoxSizer(box, wx.VERTICAL)
        self.layout.Add(self.tune_delay_txtctrl, flag=wx.ALL, border=5)
