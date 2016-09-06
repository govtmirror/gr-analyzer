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


#ifndef INCLUDED_ANALYZER_BIN_STATISTICS_FF_H
#define INCLUDED_ANALYZER_BIN_STATISTICS_FF_H

#include <cstdlib> /* size_t */

#include <analyzer/api.h>
#include <gnuradio/sync_decimator.h>

namespace gr {
  namespace analyzer {

    /*!
     * \brief Perform a peak or avg detection on incoming DFT frames
     * \ingroup analyzer
     *
     */
    class ANALYZER_API bin_statistics_ff : virtual public gr::sync_decimator
    {
     public:
      typedef boost::shared_ptr<bin_statistics_ff> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of analyzer::bin_statistics_ff.
       *
       * To avoid accidental use of raw pointers, analyzer::bin_statistics_ff's
       * constructor is in a private implementation
       * class. analyzer::bin_statistics_ff::make is the public interface for
       * creating new instances.
       */
      static sptr make(size_t vlen, size_t meas_period, size_t detector);
    };

  } // namespace analyzer
} // namespace gr

#endif /* INCLUDED_ANALYZER_BIN_STATISTICS_FF_H */
