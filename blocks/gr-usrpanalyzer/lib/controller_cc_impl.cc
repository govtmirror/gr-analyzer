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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <algorithm> /* min */
#include <cstring>   /* memcpy */
#include <cassert>   /* assert */
#include <deque>
#include <vector>

#include <gnuradio/io_signature.h>
#include <gnuradio/uhd/usrp_source.h>
#include <pmt/pmt.h>
#include <uhd/types/tune_request.hpp>
//#include <uhd/types/device_addr.hpp>
#include "controller_cc_impl.h"

namespace gr {
  namespace usrpanalyzer {

    controller_cc::sptr
    controller_cc::make(boost::shared_ptr<gr::uhd::usrp_source> &usrp,
                        std::vector<double> center_freqs,
                        double lo_offset,
                        size_t initial_delay,
                        size_t tune_delay,
                        size_t ncopy,
                        bool unittest)
    {
      return gnuradio::get_initial_sptr
        (new controller_cc_impl(usrp,
                                center_freqs,
                                lo_offset,
                                initial_delay,
                                tune_delay,
                                ncopy,
                                unittest));
    }

    /*
     * The private constructor
     */
    controller_cc_impl::controller_cc_impl(boost::shared_ptr<gr::uhd::usrp_source> &usrp,
                                           std::vector<double> center_freqs,
                                           double lo_offset,
                                           size_t initial_delay,
                                           size_t tune_delay,
                                           size_t ncopy,
                                           bool unittest)
      : gr::block("controller_cc",
                  gr::io_signature::make(1, 1, sizeof(gr_complex)),
                  gr::io_signature::make(1, 1, sizeof(gr_complex))),
        usrp_ptr(usrp), d_lo_offset(lo_offset), d_ncopy(ncopy)
    {
      d_initial_delay = initial_delay;
      d_tune_delay = tune_delay;
      d_total_delay = initial_delay + tune_delay;
      d_cfreqs_orig = center_freqs;
      d_cfreqs_iter = std::deque<double>(center_freqs.begin(),
                                         center_freqs.end());
      d_nsegments = center_freqs.size();
      d_current_segment = 1;
      d_nskipped = 0;
      d_ncopied = 0;

      st.state = ST_INIT_TUNE;

      d_retune = d_nsegments > 1;
      d_exit_after_complete = false;

      set_tag_propagation_policy(TPP_DONT);
      d_unittest = unittest;

      message_port_register_out(fc_msg_port);
    }

    void
    controller_cc_impl::forecast(int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = noutput_items;
    }

    int
    controller_cc_impl::general_work(int noutput_items,
                                     gr_vector_int& ninput_items,
                                     gr_vector_const_void_star& input_items,
                                     gr_vector_void_star& output_items)
    {
      st.done = false;

      while (!st.done)
      {
        switch (st.state)
        {
        case ST_INIT_TUNE:
          tune_initial_fc(noutput_items, st);
          break;
        case ST_WAIT_RX_FREQ:
          delay_for_rx_freq(ninput_items[0], st);
          break;
        case ST_TUNE_DELAY:
          delay_for_usrp_tune(noutput_items, st);
          break;
        case ST_COPY:
          copy_samples(noutput_items, input_items, output_items, st);
          break;
        case ST_EXIT:
          exit_flowgraph(st);
          break;
        }
      }

      this->consume(0, st.nconsume);
      return st.retval;
    }

    void
    controller_cc_impl::exit_flowgraph(WorkState& st)
    /* If done copying and d_exit_after_complete was set, then WORK_DONE */
    {
      reset();  // leave the block in a sane state
      st.nconsume = 0;
      st.done = true;
      st.state = ST_INIT_TUNE;
      st.retval = WORK_DONE;
    }

    void
    controller_cc_impl::tune_initial_fc(int& noutput_items, WorkState& st)
    {
      set_next_fc();
      tune_usrp();
      st.nconsume = noutput_items;
      st.done = true;
      st.state = ST_WAIT_RX_FREQ;
      st.retval = 0;
    }

    void
    controller_cc_impl::delay_for_rx_freq(int ninput_items, WorkState& st)
    /* Drop samples until receiving a sample tagged with "rx_freq" */
    {
      size_t range_start = this->nitems_read(0);
      size_t range_stop = range_start + ninput_items;
      size_t rel_offset;

      d_tags.clear();
      // populate tags vector with any tag on chan 0 matching tag_key
      this->get_tags_in_range(d_tags, 0, range_start, range_stop, fc_tag_key);

      // Find first tag matching target freq
      bool got_target_freq = false;
      while (!d_tags.empty() && !got_target_freq)
      {
        // For some reason rx_freq's value is not part of tune_result_t
        double trfreq = d_tune_result.actual_rf_freq - d_tune_result.actual_dsp_freq;
        if (pmt::to_double(d_tags[0].value) == trfreq || d_unittest)
        {
          rel_offset = d_tags[0].offset - range_start;
          got_target_freq = true;
        }

        // Potentially expensive, but d_tags.size() is rarely > 1
        d_tags.erase(d_tags.begin());
      }

      if (got_target_freq)
      {
        //assert(usrp_ptr->get_sensor("lo_locked").to_bool());
        st.state = ST_TUNE_DELAY;

        if (rel_offset != 0)
        {
          st.nconsume = rel_offset;
          st.retval = 0;
          st.done = true;
        }
        else
        {
          st.done = false;
        }
      }
      else
      {
        // didn't get correct tag in this batch
        st.nconsume = ninput_items;
        st.retval = 0;
        st.done = true;
      }
    }

    void
    controller_cc_impl::delay_for_usrp_tune(int noutput_items, WorkState& st)
    {
      size_t skips_left = d_total_delay - d_nskipped;
      if (skips_left > 0)
      {
        size_t nskip_this_time = std::min((size_t)noutput_items, skips_left);
        d_nskipped += nskip_this_time;

        st.nconsume = nskip_this_time;
        st.retval = 0;
        st.done = true;
      }
      else
      {
        st.done = false;
        st.state = ST_COPY;
      }
    }

    void
    controller_cc_impl::copy_samples(int noutput_items,
                                     gr_vector_const_void_star &in,
                                     gr_vector_void_star &out,
                                     WorkState& st)
    {
      // copy samples
      size_t ncopy_this_time = std::min((size_t)noutput_items, d_ncopy - d_ncopied);

      memcpy(out[0],
             in[0],
             noutput_items * this->input_signature()->sizeof_stream_item(0));

      d_ncopied += ncopy_this_time;

      bool done_copying = d_ncopied == d_ncopy;
      bool last_segment = d_current_segment == d_nsegments;

      // retune and advance to next segment or set exit_flowgraph
      if (done_copying)
      {
        d_ncopied = 0;

        if (last_segment)
        {
          d_current_segment = 1;
        }

        if (last_segment && d_exit_after_complete)
        {
          st.state = ST_EXIT;
        }
        else if (d_retune)
        {
          set_next_fc();
          tune_usrp();
          d_nskipped = 0;
          ++d_current_segment;
          d_total_delay = d_tune_delay; // don't redo initial sample delay
          st.state = ST_WAIT_RX_FREQ;
        }
      }

      st.nconsume = ncopy_this_time;
      st.retval = ncopy_this_time;
      st.done = true;
    }

    void
    controller_cc_impl::reset()
    {
      d_current_segment = 1;
      d_nskipped = 0;
      d_ncopied = 0;
      d_total_delay = d_initial_delay + d_tune_delay;
      if (d_retune)
      {
        d_cfreqs_iter = std::deque<double>(d_cfreqs_orig.begin(), d_cfreqs_orig.end());
      }
    }

    void
    controller_cc_impl::tune_usrp()
    {
      ::uhd::tune_request_t tune_req(d_current_freq, d_lo_offset);
      //tune_req.args = ::uhd::device_addr_t("mode_n=integer"); // use integer N tuning
      d_tune_result = usrp_ptr->set_center_freq(tune_req);

      this->message_port_pub(fc_msg_port, pmt::from_double(d_current_freq));
    }

    void
    controller_cc_impl::set_next_fc()
    {
      d_current_freq = d_cfreqs_iter.front();
      d_cfreqs_iter.pop_front();
      d_cfreqs_iter.push_back(d_current_freq);
    }

    bool
    controller_cc_impl::get_exit_after_complete()
    {
      return d_exit_after_complete;
    }

    void
    controller_cc_impl::set_exit_after_complete()
    {
      d_exit_after_complete = true;
    }

    void
    controller_cc_impl::clear_exit_after_complete()
    {
      d_exit_after_complete = false;
    }

  } /* namespace usrpanalyzer */
} /* namespace gr */
