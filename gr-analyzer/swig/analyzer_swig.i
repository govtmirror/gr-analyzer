/* -*- c++ -*- */

#define ANALYZER_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "analyzer_swig_doc.i"

%{
#include "analyzer/bin_statistics_ff.h"
#include "analyzer/stitch_fft_segments_ff.h"
#include "analyzer/usrp_controller_cc.h"
#include "analyzer/skiphead_reset.h"
%}

%include "analyzer/bin_statistics_ff.h"
GR_SWIG_BLOCK_MAGIC2(analyzer, bin_statistics_ff);
%include "analyzer/stitch_fft_segments_ff.h"
GR_SWIG_BLOCK_MAGIC2(analyzer, stitch_fft_segments_ff);
%include "analyzer/usrp_controller_cc.h"
GR_SWIG_BLOCK_MAGIC2(analyzer, usrp_controller_cc);
%include "analyzer/skiphead_reset.h"
GR_SWIG_BLOCK_MAGIC2(analyzer, skiphead_reset);
