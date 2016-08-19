from copy import copy
import logging

from gnuradio import uhd


class usrp(object):
    def __init__(self, cfg):
        self.logger = logging.getLogger('gr-analyzer.usrp')

        self.stream_args = uhd.stream_args(cpu_format=cfg.cpu_format,
                                           otw_format=cfg.wire_format,
                                           args=cfg.stream_args)

        found_devices = uhd.find_devices(uhd.device_addr_t(cfg.device_addr))
        len_found_devices = len(found_devices)

        if len_found_devices is 1:
            self.device_addr = found_devices[0]
            self.logger.debug("Found device {!s}".format(self.device_addr))
        else:
            if len_found_devices > 1:
                err  = "\n\nFound more than 1 USRP:\n\n"
                err += str(found_devices)
                err += "\n\n"
                err += "Use --device-addr to select desired device.\n"
                err += "  example: --device-addr='serial=*****,addr=192.168.*.*'"
                err += "\n\n"
            else:
                err = "No devices found."
            raise RuntimeError(err)

        self.uhd = uhd.usrp_source(device_addr=self.device_addr,
                                   stream_args=self.stream_args)

        self.clock_rate = int(self.uhd.get_clock_rate())
        self.sample_rate = int(self.uhd.get_samp_rate())
        self.apply_cfg(cfg)

    def get_cfg(self):
        self.cfg_updated = False
        return self.cfg

    def apply_cfg(self, cfg):
        """Return True if cfg modified, else False"""

        self.cfg = copy(cfg)

        self.stream_args = uhd.stream_args(cpu_format=cfg.cpu_format,
                                           otw_format=cfg.wire_format,
                                           args=cfg.stream_args)
        self.uhd.set_stream_args(self.stream_args)

        if cfg.subdev_spec:
            self.uhd.set_subdev_spec(cfg.subdev_spec, 0)

        # Set the antenna
        if cfg.antenna:
            self.uhd.set_antenna(cfg.antenna, 0)

        current_rate = self.sample_rate
        if cfg.sample_rate != current_rate:
            self.set_sample_rate(cfg.sample_rate)

        current_rate = self.sample_rate
        if cfg.sample_rate != current_rate:
            # If the USRP could not match the requested sr, re-update cfg
            self.cfg.update()
            return True

        # Default to half gain
        if self.cfg.gain is None:
            g = self.uhd.get_gain_range()
            self.cfg.gain = (g.start() + g.stop()) / 2.0

        self.set_gain(self.cfg.gain)

        return False

    def set_clock_rate(self, rate):
        """Set the USRP master clock rate"""
        clock_rate = rate if rate >= 10e6 else 4*rate

        # If radio doesn't have adjustable master clock, this should be no-op.
        self.uhd.set_clock_rate(clock_rate)
        self.clock_rate = int(self.uhd.get_clock_rate())

        msg = "clock rate is {} S/s".format(self.clock_rate)
        self.logger.debug(msg)

        return self.clock_rate

    def get_clock_rate(self):
        """Get the USRP master clock rate"""
        return self.clock_rate

    def set_sample_rate(self, rate, auto_adjust_master_clock=True):
        """Set the USRP sample rate"""

        # Request new clock rate if not already a multiple of new sample rate
        if auto_adjust_master_clock and self.clock_rate % int(rate):
            self.set_clock_rate(rate)

        self.uhd.set_samp_rate(rate)
        self.sample_rate = int(self.uhd.get_samp_rate())

        msg = "sample rate is {} S/s".format(self.sample_rate)
        self.logger.debug(msg)

        return self.sample_rate

    def set_gain(self, gain):
        """Let UHD decide how to distribute gain."""
        self.uhd.set_gain(gain)

    def get_gain(self):
        """Return total gain as float."""
        return self.uhd.get_gain()
