import struct

import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import threading
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

RATE = 44100
CHUNK = 1024
CHANNELS = 1
SMOOTHING = 0.75
FORMAT = pyaudio.paInt16

def init_pyaudio():
    p = pyaudio.PyAudio()
    return p.open(format=FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  frames_per_buffer=CHUNK)

def power(fft):
    p = np.sum(fft)
    return p / (CHUNK * 20000)

def visualize(data, fft):
    vy = np.zeros(10)
    for i in range(10):
        vy[i] = np.mean(fft[520+ 5 * i : 520 + 5 * (i+1)])
    return (np.arange(10), vy)


def plotting_thread(x, y, xf, keep_running):
    app = QtGui.QApplication([])

    w = QtGui.QMainWindow()
    cw = pg.GraphicsLayoutWidget()

    w.show()
    w.resize(1200, 800)
    w.setCentralWidget(cw)
    w.setWindowTitle('Fourier')

    #signal = cw.addPlot(row=0, col=0)
    #transform = cw.addPlot(row=1, col=0)
    visualization = cw.addPlot(row=2, col=0)
    visualization.showAxis(axis='left', show=False)
    visualization.showAxis(axis='bottom', show=False)
    # visualization.setLogMode(y=True)
    #visualization.SetRange(yRange=[0,10])

    #signal.setRange(yRange=[-2**15, 2**15])
    #transform.setRange(yRange=[0, 6])

    stream = init_pyaudio()

    FFT = np.zeros(CHUNK)
    mem = np.zeros((CHUNK, CHUNK))

    vx = np.arange(10)
    vy = np.arange(0, 127)
    pen = pg.mkPen(color=(0, 150, 0))
    q = np.zeros((3, 10))
    while keep_running[0]:
        raw = stream.read(CHUNK)
        y = y * SMOOTHING + (1-SMOOTHING) * np.array(struct.unpack("%dh" % CHUNK, raw))
        FFT = FFT * SMOOTHING + (1-SMOOTHING ) * (np.abs(np.fft.fft(y)) * np.blackman(CHUNK)).clip(min=1)
        FFT = np.where(FFT > 11, FFT, 1)

        visualization.plot(vx, q[0], pen=pen, clear=True)

        pg.QtGui.QApplication.processEvents()


def initialize_vars():
    x = np.linspace(0, CHUNK / RATE, CHUNK)
    y = (2**15-1) * np.sin(2 * np.pi * 5000 * x)

    xf = np.fft.fftfreq(y.size, x[1] - x[0])
    return (x, y, xf)


if __name__ == "__main__":
    (x, y, xf) = initialize_vars()
    keep_running = [True]

    plotting = threading.Thread(target=plotting_thread, args=(x, y, xf, keep_running))

    plotting.start()

    plotting.join(1000)
    keep_running[0] = False
