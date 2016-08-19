import wx


class export_time_data_btn(wx.Button):
    """A toggle button to export I/Q data to a file."""
    def __init__(self, frame):
        wx.Button.__init__(self,
                           frame,
                           wx.ID_ANY,
                           label="Time",
                           style=wx.BU_EXACTFIT)

        self.Bind(wx.EVT_BUTTON, frame.export_time_data)


class export_fft_data_btn(wx.Button):
    """A toggle button to export FFT data to a file."""
    def __init__(self, frame):
        wx.Button.__init__(self,
                           frame,
                           wx.ID_ANY,
                           label="Freq",
                           style=wx.BU_EXACTFIT)

        self.Bind(wx.EVT_BUTTON, frame.export_fft_data)


class ctrls(object):
    def __init__(self, frame):
        """Initialize gui controls for exporting data to a file"""
        ctrl_label = wx.StaticBox(frame, wx.ID_ANY, "Export Data")
        self.layout = wx.StaticBoxSizer(ctrl_label, wx.VERTICAL)
        grid = wx.GridSizer(rows=1, cols=2)
        self.time_btn = export_time_data_btn(frame)
        self.fft_btn = export_fft_data_btn(frame)
        grid.Add(self.time_btn)
        grid.Add(self.fft_btn)
        self.layout.Add(grid, flag=wx.ALL, border=5)
