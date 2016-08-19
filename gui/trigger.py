import wx


class continuous_run_btn(wx.Button):
    """A button to run the flowgraph continuously."""
    def __init__(self, frame):
        wx.Button.__init__(self, frame, wx.ID_ANY, label="Continuous")

        self.Bind(wx.EVT_BUTTON, frame.set_continuous_run)


class single_run_btn(wx.Button):
    """A button to run the flowgraph once and pause."""
    def __init__(self, frame):
        wx.Button.__init__(self, frame, wx.ID_ANY, label="Single")

        self.Bind(wx.EVT_BUTTON, frame.set_single_run)


class ctrls(object):
    def __init__(self, frame):
        """Initialize gui controls for triggering the flowgraph"""
        ctrl_label = wx.StaticBox(frame, wx.ID_ANY, "Trigger")
        self.layout = wx.StaticBoxSizer(ctrl_label, wx.VERTICAL)
        grid = wx.GridSizer(rows=2, cols=1)
        self.single_run_btn = single_run_btn(frame)
        self.continuous_run_btn = continuous_run_btn(frame)
        grid.Add(self.single_run_btn)
        grid.Add(self.continuous_run_btn)
        self.layout.Add(grid, flag=wx.ALL, border=5)
