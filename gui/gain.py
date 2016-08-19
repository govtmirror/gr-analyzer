import wx


class gain_txtctrl(wx.TextCtrl):
    """Input TxtCtrl for setting gain."""
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

        if float_val != self.frame.tb.usrp.get_gain():
            self.frame.tb.usrp.set_gain(float_val)

        self.set_value()

    def set_value(self):
        actual_val = self.frame.tb.usrp.get_gain()
        self.SetValue(str(actual_val))


class ctrls(object):
    def __init__(self, frame):
        """Initialize gui controls for gain."""

        box = wx.StaticBox(frame, wx.ID_ANY, "Gain (dB)")
        self.gain_txtctrl = gain_txtctrl(frame)
        self.layout = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        self.layout.Add(self.gain_txtctrl, flag=wx.ALL, border=5)
