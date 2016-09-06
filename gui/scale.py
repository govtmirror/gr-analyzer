import wx


class scale_txtctrl(wx.TextCtrl):
    """Input TxtCtrl for setting scale factor."""
    def __init__(self, frame):
        wx.TextCtrl.__init__(self,
                             frame,
                             wx.ID_ANY,
                             size=(60, -1),
                             style=wx.TE_PROCESS_ENTER)

        self.frame = frame
        self.Bind(wx.EVT_KILL_FOCUS, self.update)
        self.Bind(wx.EVT_TEXT_ENTER, self.update)
        self.set_value()

    def update(self, event):
        val = self.GetValue()
        try:
            float_val = float(val)
        except ValueError:
            self.set_value()
            return

        if float_val != self.frame.tb.pending_cfg.scale:
            self.frame.tb.pending_cfg.scale = float_val
            self.frame.tb.reconfigure()

        self.set_value()

    def set_value(self):
        self.SetValue(str(self.frame.tb.pending_cfg.scale))


class ctrls(object):
    def __init__(self, frame):
        """Initialize gui controls for scale factor."""

        box = wx.StaticBox(frame, wx.ID_ANY, "Scale Factor (V)")
        self.scale_txtctrl = scale_txtctrl(frame)
        self.layout = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        self.layout.Add(self.scale_txtctrl, flag=wx.ALL, border=5)
