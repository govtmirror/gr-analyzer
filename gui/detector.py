import wx

import consts


class detector_dropdown(wx.ComboBox):
    """Dropdown for setting the detector to PEAK of AVG."""
    def __init__(self, frame):
        self.frame = frame

        wx.ComboBox.__init__(self,
                             frame,
                             id=wx.ID_ANY,
                             choices=list(consts.DETECTORS),
                             style=wx.CB_READONLY)

        # Size the dropdown based on longest string
        _, height = self.GetSize()
        dc = wx.ClientDC(self)
        tsize = max(dc.GetTextExtent(d)[0] for d in consts.DETECTORS)
        self.SetMinSize((tsize+45, height))

        self.SetStringSelection(self.frame.tb.cfg.detector.name)
        self.Bind(wx.EVT_COMBOBOX, self.update)

    def update(self, event):
        """Set the window function selected by the user via dropdown."""
        detector = self.GetValue()
        self.frame.tb.pending_cfg.detector = consts.Detector[detector]
        self.frame.tb.reconfigure()

class ctrls(object):
    def __init__(self, frame):
        """Initialize gui controls for detector."""
        detector_box = wx.StaticBox(frame, wx.ID_ANY, "Detector")
        self.detector_dropdown = detector_dropdown(frame)
        self.layout = wx.StaticBoxSizer(detector_box, wx.VERTICAL)
        self.layout.Add(self.detector_dropdown, flag=wx.ALL, border=5)
