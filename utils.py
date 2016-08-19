import numpy as np


def find_nearest(array, value):
    """Find the index of the closest matching value in a NumPyarray."""
    #http://stackoverflow.com/a/2566508
    return np.abs(array - value).argmin()


def _chunks(l, n):
    """Yield successive n-sized chunks from l"""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


#def save_time_data_to_file(self, pathname):
#    """Save I/Q time data to file"""
#
#    data = self.iq_vsink.data()
#    if not data:
#        return False
#
#    self.iq_vsink.reset() # empty the sink
#
#    chunk_size = self.cfg.fft_size * self.cfg.n_averages
#    total_samples = chunk_size * self.cfg.nsteps
#    assert(len(data) == total_samples)
#    data_chunks = self._chunks(data, chunk_size)
#
#    # Translate the data to a structed array that savemat understands
#    #
#    # [ (712499200L, [
#    #     (0.005035535432398319-0.002960284473374486j),
#    #     (0.004394649062305689-0.003509615547955036j),
#    #     ...
#    #   ])
#    #   ...
#    # ]
#    matlab_format_data = np.zeros(self.cfg.nsteps, dtype=[
#        ('center_frequency', np.float64),
#        ('samples', np.complex64, (chunk_size,))
#    ])
#
#    for i, freq in enumerate(self.cfg.center_freqs):
#        samples = next(data_chunks)
#        matlab_format_data[i] = (freq, samples)
#
#    sio.savemat(pathname,
#                {'time_data': matlab_format_data},
#                appendmat=False)
#
#    self.logger.info("Exported I/Q time data to {}".format(pathname))
#
#    return True
#
#
#def save_fft_data_to_file(self, pathname):
#    """Save complex FFT data to file"""
#
#    data = self.fft_vsink.data()
#    if not data:
#        return False
#
#    self.fft_vsink.reset() # empty the sink
#
#    data_chunks = self._chunks(data, self.cfg.fft_size)
#
#    # Translate the data to a structed array that savemat understands
#    #
#    # [ (712499200L, [
#    #     (0.005035535432398319-0.002960284473374486j),
#    #     (0.004394649062305689-0.003509615547955036j),
#    #     ...
#    #   ])
#    #   ...
#    # ]
#    matlab_format_data = np.zeros(len(self.cfg.bin_freqs), dtype=[
#        ('bin_frequency', np.float64),
#        ('samples', np.complex64, (self.cfg.n_averages,))
#    ])
#
#    for step, freq in enumerate(self.cfg.center_freqs):
#        x_points = calc_x_points(freq, self.cfg)
#        n_points = len(x_points)
#        n_averages_count = 0
#        while n_averages_count < self.cfg.n_averages:
#            samples = next(data_chunks)[self.cfg.bin_start:self.cfg.bin_stop]
#            for bin_idx in xrange(n_points):
#                abs_idx = step*n_points + bin_idx
#                if n_averages_count == 0:
#                    bin_freq = x_points[bin_idx]
#                    matlab_format_data[abs_idx]['bin_frequency'] = bin_freq
#                matlab_format_data[abs_idx]['samples'][n_averages_count] = samples[bin_idx]
#
#            n_averages_count += 1
#
#    sio.savemat(pathname,
#                {'fft_data': matlab_format_data},
#                appendmat=False)
#
#    self.logger.info("Exported complex FFT data to {}".format(pathname))
#
#    return True
