/* -*- c++ -*- */
/*
 * Copyright 2014 <+YOU OR YOUR COMPANY+>.
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

#include <algorithm>  /* min, copy */
#include <cstddef>    /* size_t */

#include <gnuradio/io_signature.h>
#include "skiphead_reset_impl.h"

namespace gr {
  namespace analyzer {

    skiphead_reset::sptr
    skiphead_reset::make(size_t itemsize, uint64_t nitems_to_skip)
    {
      return gnuradio::get_initial_sptr
        (new skiphead_reset_impl(itemsize, nitems_to_skip));
    }

    /*
     * The private constructor
     */
    skiphead_reset_impl::skiphead_reset_impl(size_t itemsize, uint64_t nitems_to_skip)
      : gr::block("skiphead_reset",
                  gr::io_signature::make(1, 1, itemsize),
                  gr::io_signature::make(1, 1, itemsize)),
        d_nitems_to_skip(nitems_to_skip), d_nitems_skipped(0), d_done_skipping(false)
    {}

    void
    skiphead_reset_impl::forecast(int noutput_items,
                                  gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = noutput_items;
    }

    int
    skiphead_reset_impl::general_work(int noutput_items,
                                      gr_vector_int &ninput_items,
                                      gr_vector_const_void_star &input_items,
                                      gr_vector_void_star &output_items)
    {
      // skip d_nitems_to_skip samples
      if (!d_done_skipping)
      {
        size_t skips_left = d_nitems_to_skip - d_nitems_skipped;
        if (skips_left > 0)
        {
          size_t nskip_this_time = std::min((size_t)noutput_items, skips_left);
          this->consume(0, nskip_this_time);
          d_nitems_skipped += nskip_this_time;
          return 0;
        }

        d_done_skipping = true;
      }

      memcpy(output_items[0],
             input_items[0],
             noutput_items * this->input_signature()->sizeof_stream_item(0));
      this->consume(0, noutput_items);
      return noutput_items;
    }

    void
    skiphead_reset_impl::set_nitems_to_skip(uint64_t nitems_to_skip)
    {
      d_nitems_to_skip = nitems_to_skip;
      reset();
    }

    uint64_t
    skiphead_reset_impl::nitems_to_skip() const
    {
      return d_nitems_to_skip;
    }

    uint64_t
    skiphead_reset_impl::nitems_skipped() const
    {
      return d_nitems_skipped;
    }

    void
    skiphead_reset_impl::reset()
    {
      d_nitems_skipped = 0;
      d_done_skipping = false;
    }

  } /* namespace analyzer */
} /* namespace gr */
