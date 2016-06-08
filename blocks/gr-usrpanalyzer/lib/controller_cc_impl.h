/* -*- c++ -*- */
/*
 * Copyright 2015 <+YOU OR YOUR COMPANY+>.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_USRPANALYZER_CONTROLLER_CC_IMPL_H
#define INCLUDED_USRPANALYZER_CONTROLLER_CC_IMPL_H

#include <deque>
#include <vector>

#include <pmt/pmt.h>
#include <gnuradio/uhd/usrp_source.h>
#include <uhd/types/tune_result.hpp>
#include <usrpanalyzer/controller_cc.h>

namespace gr {
  namespace usrpanalyzer {

    enum State
    {
      ST_INIT_TUNE,
      ST_WAIT_RX_FREQ,
      ST_TUNE_DELAY,
      ST_COPY,
      ST_EXIT
    };

    struct WorkState
    {
      State state;
      bool done;
      size_t nconsume;
      int retval;
    };

    class controller_cc_impl : public controller_cc
    {
    private:
      // used for finding tag streams
      pmt::pmt_t d_tag_key;
      std::vector<gr::tag_t> d_tags;

      // used for skipping samples
      size_t d_initial_delay;     // samples to skip after flowgraph initialization
      size_t d_tune_delay;        // samples to skip after rx_freq tag/before copy
      size_t d_total_delay;       // total samples to skip
      size_t d_nskipped;          // total samples skipped so far this segment

      // used for copying
      size_t d_ncopy;             // samples to copy per segment
      size_t d_ncopied;           // total samples copied so far this segment

      // used for general flow control
      boost::shared_ptr<gr::uhd::usrp_source> usrp_ptr;      // USRP source pointer
      ::uhd::tune_result_t d_tune_result;
      std::vector<double> d_cfreqs_orig;
      std::deque<double> d_cfreqs_iter;
      size_t d_nsegments;         // number of center frequencies in span
      size_t d_current_segment;   // incremented from 1 to nsegments
      double d_lo_offset;
      double d_current_freq;      // holds return fc
      bool d_retune;              // convenience variable for "nsegments > 1"
      bool d_exit_after_complete; // if true, exit at end of span

      bool d_unittest;            // if true, assume rx_freq's value is correct

      WorkState st;

      const pmt::pmt_t fc_msg_port = pmt::intern("fc");
      const pmt::pmt_t fc_tag_key = pmt::intern("rx_freq");

      void reset();               // helper function called at end of span
      void tune_usrp();
      void set_next_fc();

      void exit_flowgraph(WorkState& st);
      void tune_initial_fc(int& noutput_items, WorkState& st);
      void delay_for_rx_freq(int ninput_items, WorkState& st);
      void delay_for_usrp_tune(int noutput_items, WorkState& st);

      void copy_samples(int noutput_items,
                        gr_vector_const_void_star &in,
                        gr_vector_void_star &out,
                        WorkState& st);

    public:
      controller_cc_impl(boost::shared_ptr<gr::uhd::usrp_source> &usrp,
                         std::vector<double> center_freqs,
                         double lo_offset,
                         size_t initial_delay,
                         size_t tune_delay,
                         size_t ncopy,
                         bool unittest=false);

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items);

      void reset_initial_delay();
      bool get_exit_after_complete();
      void set_exit_after_complete();
      void clear_exit_after_complete();
    };

  } // namespace usrpanalyzer
} // namespace gr

#endif /* INCLUDED_USRPANALYZER_CONTROLLER_CC_IMPL_H */
