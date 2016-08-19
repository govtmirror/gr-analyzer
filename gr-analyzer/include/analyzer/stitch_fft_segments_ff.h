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


#ifndef INCLUDED_ANALYZER_STITCH_FFT_SEGMENTS_FF_H
#define INCLUDED_ANALYZER_STITCH_FFT_SEGMENTS_FF_H

#include <analyzer/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace analyzer {

    /*!
     * \brief Given an input vector of fft_size segments, overlap them
     * \ingroup analyzer
     *
     */
    class ANALYZER_API stitch_fft_segments_ff : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<stitch_fft_segments_ff> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of analyzer::stitch_fft_segments_ff.
       *
       * To avoid accidental use of raw pointers, analyzer::stitch_fft_segments_ff's
       * constructor is in a private implementation
       * class. analyzer::stitch_fft_segments_ff::make is the public interface for
       * creating new instances.
       */
      static sptr make(size_t fft_size, size_t n_segments, float overlap);
    };

  } // namespace analyzer
} // namespace gr

#endif /* INCLUDED_ANALYZER_STITCH_FFT_SEGMENTS_FF_H */
