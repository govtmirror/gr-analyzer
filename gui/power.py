import wx


class min_power_txtctrl(wx.TextCtrl):
    """Input TxtCtrl for adjusting the minimum power."""
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
        """Set the min power set by the user."""
        try:
            newval = float(self.GetValue())
        except ValueError:
            self.set_value()
            return

        if newval != self.frame.min_power:
            self.frame.min_power = newval
            self.frame.format_axis()

        self.set_value()

    def set_value(self):
        self.SetValue(str(int(self.frame.min_power)))


class max_power_txtctrl(wx.TextCtrl):
    """Input TxtCtrl for adjusting the maximum power."""
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
        """Set the max power set by the user."""
        try:
            newval = float(self.GetValue())
        except ValueError:
            self.set_value()
            return

        if newval != self.frame.max_power:
            self.frame.max_power = newval
            self.frame.format_axis()

        self.set_value()

    def set_value(self):
        self.SetValue(str(int(self.frame.max_power)))


class ctrls(object):
    def __init__(self, frame):
        """Initialize gui controls for adjusting power range."""
        box = wx.StaticBox(frame, wx.ID_ANY, "Power Range (dBm)")
        self.layout = wx.StaticBoxSizer(box, wx.VERTICAL)
        low_txt = wx.StaticText(frame, wx.ID_ANY, "low: ")
        high_txt = wx.StaticText(frame, wx.ID_ANY, "high: ")
        self.max_power_txtctrl = max_power_txtctrl(frame)
        self.min_power_txtctrl = min_power_txtctrl(frame)
        grid = wx.FlexGridSizer(rows=2, cols=2)
        grid.Add(high_txt, flag=wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.max_power_txtctrl, flag=wx.BOTTOM, border=5)
        grid.Add(low_txt, flag=wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.min_power_txtctrl, flag=wx.ALIGN_RIGHT)
        self.layout.Add(grid, flag=wx.ALL|wx.EXPAND, border=5)
