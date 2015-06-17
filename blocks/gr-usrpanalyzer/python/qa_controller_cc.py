#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015 <+YOU OR YOUR COMPANY+>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy as np

from gnuradio import gr, gr_unittest, uhd
from gnuradio import blocks
import pmt
import usrpanalyzer_swig as usrpanalyzer


class qa_controller_cc(gr_unittest.TestCase):
    def setUp(self):
        self.tb = gr.top_block()
        self.tb_null = gr.top_block()
        self.usrp = uhd.usrp_source(device_addr="",
                                 stream_args=uhd.stream_args("fc32"))
        null = blocks.null_sink(gr.sizeof_gr_complex)
        self.tb_null.connect(self.usrp, null)
        self.tag_debug = blocks.tag_debug(gr.sizeof_gr_complex, "Tag debug")
        self.tag_debug.set_display(False)
        self.vsink = blocks.vector_sink_c()

    def tearDown(self):
        self.tb = None
        self.tb_null = None
        self.tab_debug = None
        self.vsink = None

    def test001(self):
        """Test simple copy, no delay"""
        tag1_dict = dict()
        tag1_dict["offset"] = 10000
        tag1_dict["key"] = pmt.intern("rx_freq")
        tag1_dict["value"] = pmt.from_double(0.0)
        tag1_dict["srcid"] = pmt.intern(self.usrp.name())
        tag1 = gr.tag_utils.python_to_tag(tag1_dict)

        nsamples = 10100
        src_data = np.array([complex(x) for x in range(nsamples)])
        src = blocks.vector_source_c(data=src_data, tags=[tag1])

        usrp_ptr = self.usrp
        cfreqs = np.array([ 0.])
        lo_offset = 0
        initial_delay = 0
        tune_delay = 0
        ncopy = 100

        ctrl = usrpanalyzer.controller_cc(usrp_ptr, cfreqs, lo_offset,
                                          initial_delay, tune_delay, ncopy,
                                          unittest=True)

        self.tb.connect((src, 0), self.tag_debug)
        self.tb.connect((src, 0), ctrl, self.vsink)
        self.tb.run()

        result = self.vsink.data()
        expected_result = np.arange(10000, 10100)

        np.testing.assert_array_equal(result, expected_result)

    def test002(self):
        """Test exit_after_complete"""
        tag1_dict = dict()
        tag1_dict["offset"] = 10000
        tag1_dict["key"] = pmt.intern("rx_freq")
        tag1_dict["value"] = pmt.from_double(0.0)
        tag1_dict["srcid"] = pmt.intern(self.usrp.name())
        tag1 = gr.tag_utils.python_to_tag(tag1_dict)

        nsamples = 10101
        src_data = np.array([complex(x) for x in range(nsamples)])
        src = blocks.vector_source_c(data=src_data, tags=[tag1])

        usrp_ptr = self.usrp
        cfreqs = np.array([ 0.])
        lo_offset = 0
        initial_delay = 0
        tune_delay = 0
        ncopy = 100

        ctrl = usrpanalyzer.controller_cc(usrp_ptr, cfreqs, lo_offset,
                                          initial_delay, tune_delay, ncopy,
                                          unittest=True)
        ctrl.set_exit_after_complete()

        self.tb.connect((src, 0), self.tag_debug)
        self.tb.connect((src, 0), ctrl, self.vsink)
        self.tb.run()

        result = self.vsink.data()
        expected_result = np.arange(10000, 10100)

        np.testing.assert_array_equal(result, expected_result)

    def test003(self):
        """Test copy at multi center freqs"""
        tag1_dict = dict()
        tag1_dict["offset"] = 10000
        tag1_dict["key"] = pmt.intern("rx_freq")
        tag1_dict["value"] = pmt.from_double(0.0)
        tag1_dict["srcid"] = pmt.intern(self.usrp.name())
        tag1 = gr.tag_utils.python_to_tag(tag1_dict)

        tag2_dict = dict()
        tag2_dict["offset"] = 20000
        tag2_dict["key"] = pmt.intern("rx_freq")
        tag2_dict["value"] = pmt.from_double(1.0)
        tag2_dict["srcid"] = pmt.intern(self.usrp.name())
        tag2 = gr.tag_utils.python_to_tag(tag2_dict)

        tag3_dict = dict()
        tag3_dict["offset"] = 30000
        tag3_dict["key"] = pmt.intern("rx_freq")
        tag3_dict["value"] = pmt.from_double(2.0)
        tag3_dict["srcid"] = pmt.intern(self.usrp.name())
        tag3 = gr.tag_utils.python_to_tag(tag3_dict)

        nsamples = 30100
        src_data = np.array([complex(x) for x in range(nsamples)])
        src = blocks.vector_source_c(data=src_data, tags=[tag1, tag2, tag3])

        usrp_ptr = self.usrp
        cfreqs = np.array([ 0.,  1.,  2.])
        lo_offset = 0
        initial_delay = 0
        tune_delay = 0
        ncopy = 100

        ctrl = usrpanalyzer.controller_cc(usrp_ptr, cfreqs, lo_offset,
                                          initial_delay, tune_delay, ncopy,
                                          unittest=True)

        self.tb.connect((src, 0), self.tag_debug)
        self.tb.connect((src, 0), ctrl, self.vsink)
        self.tb.run()

        result = self.vsink.data()
        expected_result = np.concatenate((np.arange(10000, 10100),
                                          np.arange(20000, 20100),
                                          np.arange(30000, 30100)))

        np.testing.assert_array_equal(result, expected_result)

    def test004(self):
        """Test simple copy, with delay"""
        tag1_dict = dict()
        tag1_dict["offset"] = 10000
        tag1_dict["key"] = pmt.intern("rx_freq")
        tag1_dict["value"] = pmt.from_double(0.0)
        tag1_dict["srcid"] = pmt.intern(self.usrp.name())
        tag1 = gr.tag_utils.python_to_tag(tag1_dict)

        nsamples = 10100
        src_data = np.array([complex(x) for x in range(nsamples)])
        src = blocks.vector_source_c(data=src_data, tags=[tag1])

        usrp_ptr = self.usrp
        cfreqs = np.array([ 0.])
        lo_offset = 0
        initial_delay = 50
        tune_delay = 20
        ncopy = 30

        ctrl = usrpanalyzer.controller_cc(usrp_ptr, cfreqs, lo_offset,
                                          initial_delay, tune_delay, ncopy,
                                          unittest=True)

        self.tb.connect((src, 0), self.tag_debug)
        self.tb.connect((src, 0), ctrl, self.vsink)
        self.tb.run()

        result = self.vsink.data()
        expected_result = np.arange(10070, 10100)

        np.testing.assert_array_equal(result, expected_result)

        self.assertEqual(ctrl.nitems_read(0) - ctrl.nitems_written(0), 10070)


if __name__ == '__main__':
    #import os
    #print("Blocked waiting for GDB attach (pid = {})".format(os.getpid()))
    #raw_input("Press Enter to continue...")

    gr_unittest.run(qa_controller_cc, "qa_controller_cc.xml")
