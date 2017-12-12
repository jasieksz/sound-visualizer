import numpy as np
import matplotlib.pyplot as plt

RATE = 44100
CHUNK = 1024

x = np.linspace(0, CHUNK/RATE, CHUNK)
y =  10 * np.sin(2 * np.pi * 5000 * x) + 5 * np.sin(2 * np.pi * 10000 * x)

FFT = np.abs(np.fft.fft(y))
freqs = np.fft.fftfreq(y.size, x[1] - x[0])

plt.subplot(211)
plt.plot(x, y)
plt.subplot(212)
plt.plot(freqs,20*np.log10(FFT))
plt.show()
