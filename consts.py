from enum import IntEnum

WIRE_FORMATS = ("sc8", "sc16")
CPU_FORMATS = ("fc32", "sc16")
FFT_SIZES = [2**n for n in range(5, 14)] # 32 - 8192

class Detector(IntEnum):
    AVG = 0
    PEAK = 1

DETECTORS = [d.name for d in Detector.__members__.values()]
