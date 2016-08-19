import wx


class center_freq_txtctrl(wx.TextCtrl):
    """Input TxtCtrl for adjusting the center frequency."""
    def __init__(self, frame):
        wx.TextCtrl.__init__(self,
                             frame,
                             id=wx.ID_ANY,
                             size=(60, -1),
                             style=wx.TE_PROCESS_ENTER)

        self.frame = frame
        self.Bind(wx.EVT_TEXT_ENTER, self.update)
        self.Bind(wx.EVT_KILL_FOCUS, self.update)
        self.set_value()

    def update(self, event):
        """Set the min freq set by the user."""
        try:
            float_val = float(self.GetValue()) * 1e6
        except ValueError:
            self.set_value()
            return

        if float_val != self.frame.tb.pending_cfg.center_freq:
            self.frame.tb.pending_cfg.center_freq = float_val
            self.frame.tb.pending_cfg.update()
            self.frame.tb.reconfigure(redraw_plot=True)

        self.set_value()

    def set_value(self):
        self.SetValue(str(self.frame.tb.pending_cfg.center_freq / 1e6))


class ctrls(object):
    def __init__(self, frame):
        """Initialize gui controls for adjusting frequency range."""
        box = wx.StaticBox(frame, wx.ID_ANY, "Frequency (MHz)")
        self.center_freq_txtctrl = center_freq_txtctrl(frame)
        self.layout = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        self.layout.Add(self.center_freq_txtctrl, flag=wx.ALL, border=5)
