import wx
import threading

from gui.main import wxpygui_frame


class plot_interface(object):
    def __init__(self, tb):
        self.tb = tb
        self.app = wx.App()
        self.app.frame = wxpygui_frame(tb)
        self.app.frame.Show()
        self.gui = threading.Thread(target=self.app.MainLoop)

        self.redraw_plot = threading.Event()

        self.gui.daemon = True
        self.gui.start()

    def keep_alive(self):
        return self.update(None)

    def update(self, points):
        # if we don't have points to plot, just keep gui alive
        keep_alive = points is None
        redraw = self.redraw_plot.is_set() and not keep_alive
        try:
            if self.app.frame.closed:
                return False
            # thread-safe call to wx gui
            wx.CallAfter(self.app.frame.update_plot,
                         points,
                         redraw,
                         keep_alive)

            if redraw:
                self.redraw_plot.clear()
            return True
        except wx.PyDeadObjectError:
            return False

    def is_alive(self):
        try:
            if self.app.frame.closed:
                return False
            return True
        except wx.PyDeadObjectError:
            return False

    def set_gui_idle(self):
        self.tb.copy_if_gui_idle.set_enabled(True)
