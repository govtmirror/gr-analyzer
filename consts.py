WIRE_FORMATS = frozenset(("sc8", "sc16"))
CPU_FORMATS = frozenset(("fc32", "sc16"))
FFT_SIZES = frozenset((2**n for n in range(5, 14))) # 32 - 8192
