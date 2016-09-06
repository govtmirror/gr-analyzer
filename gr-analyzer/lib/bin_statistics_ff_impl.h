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

#ifndef INCLUDED_ANALYZER_BIN_STATISTICS_FF_IMPL_H
#define INCLUDED_ANALYZER_BIN_STATISTICS_FF_IMPL_H

#include <analyzer/bin_statistics_ff.h>

namespace gr {
  namespace analyzer {

    class bin_statistics_ff_impl : public bin_statistics_ff
    {
    private:
      size_t d_vlen;
      size_t d_meas_interval;
      size_t d_detector;

    public:
      bin_statistics_ff_impl(size_t vlen,
                             size_t meas_interval,
                             size_t detector);

      // Where all the action really happens
      int work(int noutput_items,
               gr_vector_const_void_star &input_items,
               gr_vector_void_star &output_items);

      enum Detector {AVG, PEAK};
    };

  } // namespace analyzer
} // namespace gr

#endif /* INCLUDED_ANALYZER_BIN_STATISTICS_FF_IMPL_H */
