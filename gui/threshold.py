import wx


class threshold_txtctrl(wx.TextCtrl):
    """Input TxtCtrl for setting a threshold power level."""
    def __init__(self, frame):
        wx.TextCtrl.__init__(self,
                             frame,
                             id=wx.ID_ANY,
                             size=(60, -1),
                             style=wx.TE_PROCESS_ENTER)

        self.Bind(wx.EVT_KILL_FOCUS, frame.threshold.set_level)
        self.Bind(wx.EVT_TEXT_ENTER, frame.threshold.set_level)
        if frame.threshold.level:
            self.SetValue(str(frame.threshold.level))


class threshold(object):
    """A horizontal line to indicate user-defined overload threshold."""
    def __init__(self, frame, level):
        self.frame = frame
        self.line = None
        self.level = level # default level in dBm or None

    def plot(self):
        # plot the new threshold and add it to our blitted background
        f_min = self.frame.tb.cfg.min_freq
        f_max = self.frame.tb.cfg.max_freq
        xs = [f_min - 1e7, f_max + 1e7]
        ys = [self.level] * 2
        self.line, = self.frame.subplot.plot(xs, ys,
                                             color='red',
                                             # play nice with blitting:
                                             animated=True,
                                             # draw above grid lines:
                                             zorder=90)

    def unplot(self):
        self.line.remove()
        self.line = None
        self.level = None

    def set_level(self, event):
        """Set the level to a user input value."""
        evt_obj = event.GetEventObject()

        txtctrl_value = evt_obj.GetValue()

        try:
            # will raise ValueError if not a number
            new_level = float(txtctrl_value)
            if not self.level or new_level != self.level:
                self.level = new_level
                self.plot()
        except ValueError:
            if txtctrl_value == "" and self.level is not None:
                # Let the user remove the threshold line
                self.unplot()

        evt_obj.SetValue(str(self.level) if self.level else "")


class ctrls(object):
    def __init__(self, frame):
        """Initialize gui controls for threshold."""
        ctrl_box = wx.StaticBox(frame, wx.ID_ANY, "Threshold (dBm)")
        self.layout = wx.StaticBoxSizer(ctrl_box, wx.VERTICAL)
        grid = wx.FlexGridSizer(rows=1, cols=2)
        txt = wx.StaticText(frame, wx.ID_ANY, "Overload: ")
        grid.Add(txt, flag=wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        grid.Add(threshold_txtctrl(frame), flag=wx.ALIGN_RIGHT)
        self.layout.Add(grid, flag=wx.ALL, border=5)
