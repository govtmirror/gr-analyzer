import numpy as np

from gnuradio import gr
import pmt


class plotter_f(gr.sync_block):
    def __init__(self, tb, plot_vec_len):
        gr.sync_block.__init__(
            self,
            name="plotter_f",
            in_sig=[(np.float32, plot_vec_len)],
            out_sig=None
        )

        self.tb = tb
        self.max_bin = tb.cfg.max_plotted_bin # crop plotted data to span
        self.plot_iface = tb.plot_iface
        self.plot_iface.redraw_plot.set()

        self.signal = pmt.from_bool(False)
        self.port_name = pmt.intern("gui_busy_notifier")
        self.message_port_register_out(self.port_name)

    def work(self, input_items, output_items):
        in0 = input_items[0]
        ninput_items = len(in0)

        gui_alive = self.plot_iface.update(in0[0][:self.max_bin])
        if not gui_alive:
            return -1

        if self.tb.continuous_run.is_set():
            # only protect the gui thread in continuous mode
            self.message_port_pub(self.port_name, self.signal)

        return ninput_items
