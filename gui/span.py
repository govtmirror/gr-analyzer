import wx


class span_txtctrl(wx.TextCtrl):
    """Input TxtCtrl for adjusting the span."""
    def __init__(self, frame):
        wx.TextCtrl.__init__(self,
                             frame,
                             id=wx.ID_ANY,
                             size=(60, -1),
                             style=wx.TE_PROCESS_ENTER)

        self.frame = frame
        self.Bind(wx.EVT_KILL_FOCUS, self.update)
        self.Bind(wx.EVT_TEXT_ENTER, self.update)
        self.format_str = "{:.1f}"
        self.set_value()

    def update(self, event):
        """Set the span set by the user."""
        evt_obj = event.GetEventObject()
        txtctrl_value = evt_obj.GetValue()

        try:
            float_val = float(txtctrl_value) * 1e6
            assert(float_val > 0)
        except (ValueError, AssertionError):
            self.set_default(None)
            return

        if float_val != self.frame.tb.pending_cfg.span:
            self.frame.tb.pending_cfg.requested_span = float_val
            self.frame.tb.reconfigure(redraw_plot=True)
            self.frame.tb.pending_cfg.update()
            self.set_value()

    def set_default(self, event):
        """Set a default span"""
        self.frame.tb.pending_cfg.requested_span = None
        self.frame.tb.pending_cfg.update()
        self.frame.tb.reconfigure(redraw_plot=True)
        self.set_value()

    def set_value(self):
        value = self.frame.tb.pending_cfg.span / 1e6
        self.SetValue(self.format_str.format(value))


class span_reset_btn(wx.Button):
    """A button to export I/Q data to a file."""
    def __init__(self, frame, span_txtctrl):
        wx.Button.__init__(self,
                           frame,
                           wx.ID_ANY,
                           label="Reset",
                           style=wx.BU_EXACTFIT)

        self.Bind(wx.EVT_BUTTON, span_txtctrl.set_default)


class ctrls(object):
    def __init__(self, frame):
        """Initialize gui controls for adjusting span."""
        box = wx.StaticBox(frame, wx.ID_ANY, "Span (MHz)")
        self.layout = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.span_txt = span_txtctrl(frame)
        self.span_btn = span_reset_btn(frame, self.span_txt)
        hbox.Add(self.span_txt)
        hbox.Add(self.span_btn)
        self.layout.Add(hbox, flag=wx.ALL, border=5)
