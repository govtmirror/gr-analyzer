#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import math
import time
import threading
import logging
from copy import copy

from gnuradio import gr
from gnuradio import blocks
from gnuradio import fft

from analyzer import (usrp_controller_cc,
                      bin_statistics_ff,
                      stitch_fft_segments_ff,
                      plotter_f)

from cli_parser import init_parser
from configuration import configuration
import gui
from usrp import usrp


class top_block(gr.top_block):
    def __init__(self, cfg):
        gr.top_block.__init__(self)

        self.logger = logging.getLogger("gr-analyzer.top_block")

        # Use 2 copies of the configuration:
        # cgf - settings that matches the current state of the flowgraph
        # pending_cfg - requested config changes that will be applied during
        #               the next run of configure
        self.cfg = cfg
        self.pending_cfg = copy(self.cfg)

        if cfg.realtime:
            # Attempt to enable realtime scheduling
            r = gr.enable_realtime_scheduling()
            if r != gr.RT_OK:
                self.logger.warning("failed to enable realtime scheduling")

        try:
            self.usrp = usrp(cfg)
        except RuntimeError as err:
            print("Error initializing USRP." + str(err), file=sys.stderr)
            sys.exit(0)

        # The main loop blocks at the end of the loop until either continuous
        # or single run mode is set.
        self.continuous_run = threading.Event()
        self.single_run = threading.Event()

        self.plot_iface = gui.plot_interface(self)

        self.rebuild_flowgraph = False
        self.configure(initial=True)

    def set_single_run(self):
        self.clear_continuous_run()
        if self.cfg.continuous_run:
            self.rebuild_flowgraph = True
            self.cfg.continuous_run = False
            self.pending_cfg.continuous_run = False
        self.single_run.set()

    def clear_single_run(self):
        self.single_run.clear()

    def set_continuous_run(self):
        self.clear_single_run()
        if not self.cfg.continuous_run:
            self.clear_exit_after_complete()
            self.rebuild_flowgraph = True
            self.pending_cfg.continuous_run = True
        self.continuous_run.set()

    def clear_continuous_run(self):
        self.set_exit_after_complete()
        self.continuous_run.clear()

    def set_exit_after_complete(self):
        self.ctrl.set_exit_after_complete()

    def clear_exit_after_complete(self):
        self.ctrl.clear_exit_after_complete()

    def reconfigure(self, redraw_plot=False):
        msg = "tb.reconfigure called - redraw_plot: {}"
        self.logger.debug(msg.format(redraw_plot))
        self.rebuild_flowgraph = True
        self.set_exit_after_complete()  # exit flowgraph to apply new config
        if redraw_plot:
            self.plot_iface.redraw_plot.set()

    def configure(self, initial=False):
        """Configure or reconfigure the flowgraph"""

        self.lock()

        if self.usrp.apply_cfg(self.pending_cfg):
            self.pending_cfg = copy(self.usrp.get_cfg())

        # Apply any pending configuration changes
        cfg = self.cfg = copy(self.pending_cfg)

        if not initial:
            self.disconnect_all()
            self.msg_disconnect(self.plot, "gui_busy_notifier",
                                self.copy_if_gui_idle, "en")

        self.ctrl = usrp_controller_cc(self.usrp.uhd,
                                       cfg.center_freqs,
                                       cfg.lo_offset,
                                       cfg.skip_initial,
                                       cfg.tune_delay,
                                       cfg.fft_size * cfg.nframes)

        if cfg.continuous_run:
            self.set_continuous_run()
        else:
            self.set_single_run()

        self.scaleV = blocks.multiply_const_cc(cfg.scale)

        timedata_vlen = 1
        self.timedata_sink = blocks.vector_sink_c(timedata_vlen)

        stream_to_fft_vec = blocks.stream_to_vector(gr.sizeof_gr_complex,
                                                    cfg.fft_size)

        forward = True
        shift = True
        self.fft = fft.fft_vcc(cfg.fft_size,
                               forward,
                               cfg.window_coefficients,
                               shift)

        freqdata_vlen = cfg.fft_size
        self.freqdata_sink = blocks.vector_sink_c(freqdata_vlen)

        c2mag_sq = blocks.complex_to_mag_squared(cfg.fft_size)

        stats = bin_statistics_ff(cfg.fft_size, cfg.nframes, cfg.detector)

        power = sum(tap * tap for tap in cfg.window_coefficients)

        # Divide magnitude-square by a constant to obtain power
        # in Watts. Assumes unit of USRP source is volts.
        impedance = 50.0  # ohms
        Vsq2W_dB = -10.0 * math.log10(cfg.fft_size * power * impedance)
        # Convert from Watts to dBm.
        W2dBm = blocks.nlog10_ff(10.0, cfg.fft_size, 30 + Vsq2W_dB)

        stitch = stitch_fft_segments_ff(cfg.fft_size,
                                        cfg.n_segments,
                                        cfg.overlap)

        fft_vec_to_stream = blocks.vector_to_stream(gr.sizeof_float,
                                                    cfg.fft_size)
        n_valid_bins = cfg.fft_size - (cfg.fft_size * (cfg.overlap / 2) * 2)
        # FIXME: think about whether to cast to int vs round vs...
        stitch_vec_len = int(cfg.n_segments * cfg.fft_size)
        stream_to_stitch_vec = blocks.stream_to_vector(gr.sizeof_float,
                                                       stitch_vec_len)

        plot_vec_len = int(cfg.n_segments * n_valid_bins)

        # Only copy sample to plot if enabled to avoid overwhelming gui thread
        self.copy_if_gui_idle = blocks.copy(gr.sizeof_float * plot_vec_len)

        self.plot = plotter_f(self, plot_vec_len)

        # Create the flowgraph:
        #
        # USRP   - hardware source output stream of 32bit complex floats
        # ctrl   - copy N samples then call retune callback and loop
        # scaleV - scale voltage by scalar to get calibrated output
        # fft    - compute forward FFT, complex in complex out
        # mag^2  - convert vectors from complex to real by taking mag squared
        # stats  - linear average or peak detect vectors if nframes > 1
        # W2dBm  - convert volt to dBm
        # stitch - overlap FFT segments by a certain number of bins
        # copy   - copy if gui thread is idle, else drop
        # plot   - plot data
        #
        # USRP > ctrl > fft > mag^2 > stats > W2dBm > stitch > copy > plot

        self.connect(self.usrp.uhd, self.ctrl, self.scaleV)
        if self.single_run.is_set():
            self.logger.debug("Connected timedata_sink")
            self.connect((self.scaleV, 0), self.timedata_sink)
        else:
            self.logger.debug("Disconnected timedata_sink")
        self.connect((self.scaleV, 0), stream_to_fft_vec, self.fft)
        if self.single_run.is_set():
            self.logger.debug("Connected freqdata_sink")
            self.connect((self.fft, 0), self.freqdata_sink)
        else:
            self.logger.debug("Disconnected freqdata_sink")
        self.connect((self.fft, 0), c2mag_sq, stats, W2dBm, fft_vec_to_stream)
        self.connect(fft_vec_to_stream, stream_to_stitch_vec, stitch)
        self.connect(stitch, self.copy_if_gui_idle, self.plot)

        self.msg_connect(self.plot, "gui_busy_notifier",
                         self.copy_if_gui_idle, "en")

        self.unlock()

    def set_sample_rate(self, rate):
        new_rate = self.usrp.set_sample_rate(rate)

        # Pass the actual samp rate back to cfgs so they have it before
        # calling cfg.update()
        requested_rate = self.cfg.sample_rate
        self.pending_cfg.sample_rate = self.cfg.sample_rate = new_rate

        # If the rate was adjusted, recalculate freqs and reconfigure flowgraph
        if requested_rate != self.sample_rate:
            self.pending_cfg.update()
            self.reconfigure(redraw_plot=True)

    def save_time_data_to_file(self, data):
        print("NOOP")

    def save_freq_data_to_file(self, data):
        print("NOOP")


def main(tb):
    """Run the main loop of the program"""

    logger = logging.getLogger('gr-analyzer.main')
    gui_alive = True

    while True:
        # Execute flow graph and wait for it to stop
        tb.run()
        tb.clear_single_run()

        if tb.continuous_run.is_set() and not tb.plot_iface.is_alive():
            # GUI was destroyed while in continuous mode
            return

        while not (tb.single_run.is_set() or tb.continuous_run.is_set()):
            # keep certain gui elements alive
            gui_alive = tb.plot_iface.keep_alive()
            if not gui_alive:
                # GUI was destroyed while in single mode
                return
            # check run mode again in 1/4 second
            time.sleep(.25)

        tb.timedata_sink.reset()
        tb.freqdata_sink.reset()

        if tb.rebuild_flowgraph:
            logger.info("rebuild flowgraph")
            tb.configure()
            tb.rebuild_flowgraph = False


if __name__ == '__main__':
    parser = init_parser()
    args = parser.parse_args()
    cfg = configuration(args)

    if cfg.debug:
        print("pid = {}".format(os.getpid()))
        raw_input("Press Enter to continue...")

    tb = top_block(cfg)
    try:
        main(tb)
        logging.getLogger('gr-analyzer').info("Exiting.")
    except KeyboardInterrupt:
        tb.stop()
        tb.wait()
