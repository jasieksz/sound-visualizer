import struct

import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import threading
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg


class Visualizer():

    def __init__(self):
        self.RATE = 44100
        self.CHUNK = 1024
        self.CHANNELS = 1
        self.SMOOTHING = 0.75
        self.FORMAT = pyaudio.paInt16
        self.stream = self.init_pyaudio()
        # self.widget = None

    def init_pyaudio(self):
        p = pyaudio.PyAudio()
        return p.open(format=self.FORMAT,
                      channels=self.CHANNELS,
                      rate=self.RATE,
                      input=True,
                      frames_per_buffer=self.CHUNK)

    def power(self, fft):
        p = np.sum(fft)
        return p / (self.CHUNK * 20000)

    def visualize(self, binNumber, fft):
        data = np.zeros(binNumber)
        for i in range(binNumber):
            data[i] = np.mean(fft[520 + 5 * i: 520 + 5 * (i + 1)])
        return (np.arange(fft.shape[0]), data)

    def startWindow(self):
        app = QtGui.QApplication([])
        w = QtGui.QMainWindow()
        widget = pg.GraphicsLayoutWidget()
        w.show()
        w.resize(1200, 800)
        w.setCentralWidget(widget)
        w.setWindowTitle('Fourier')
        return widget

    def initialize_vars(self):
        x = np.linspace(0, self.CHUNK / self.RATE, self.CHUNK)
        y = (2 ** 15 - 1) * np.sin(2 * np.pi * 5000 * x)
        xf = np.fft.fftfreq(y.size, x[1] - x[0])
        return x, y, xf

    def prepareFFT(self, xRange, yRange, binNumber, lines):
        FFT = np.zeros(self.CHUNK)
        mem = np.zeros((self.CHUNK, self.CHUNK))
        vx = np.arange(xRange)
        vy = np.arange(0, yRange)
        q = np.zeros((lines, binNumber))
        return FFT, mem, vx, vy, q

    def plot(self, x, y, xf, runFlag, signalFlag=False, transformFlag=False, visualizationFlag=True):
        app = QtGui.QApplication([])
        w = QtGui.QMainWindow()
        widget = pg.GraphicsLayoutWidget()
        w.show()
        w.resize(1200, 800)
        w.setCentralWidget(widget)
        w.setWindowTitle('Fourier')

        if signalFlag:
            signal = widget.addPlot(row=0, col=0)
            signal.setRange(yRange=[-2 ** 15, 2 ** 15])
        if transformFlag:
            transform = widget.addPlot(row=1, col=0)
            transform.setRange(yRange=[0, 10000])
        if visualizationFlag:
            visualization = widget.addPlot(row=2, col=0)
            visualization.setRange(yRange=[0, 10000])

        pen = pg.mkPen(color=(0, 150, 0))

        FFT, mem, vx, vy, q = self.prepareFFT(10, 127, 40, 3) # TODO : po co 1 zmiena !?

        while runFlag[0]:
            raw = self.stream.read(self.CHUNK)
            y = self.SMOOTHING + (1 - self.SMOOTHING) * np.array(struct.unpack("%dh" % self.CHUNK, raw))
            FFT = FFT * self.SMOOTHING + (1 - self.SMOOTHING) * (np.abs(np.fft.fft(y)) * np.blackman(self.CHUNK)).clip(
                min=1)
            FFT = np.where(FFT > 11, FFT, 1)

            if signalFlag:
                signal.plot(x, y, clear=True)
            if transformFlag:
                transform.plot(xf, FFT, clear=False)

            if visualizationFlag:
                q = np.roll(q, -1, axis=0)
                q[2] = self.visualize(q.shape[1], FFT)[1]
                for i in range(q.shape[0]):
                    q[i][0] = 0
                    q[i][q.shape[1] - 1] = 0
                #q2 = np.copy(q)
                #q2 = q2 * (-1)
                visualization.plot(vx, q[0], pen=pen, clear=True)
                #visualization.plot(vx, q2[0], pen=pen, clear=True)
                for i in range(1, q.shape[0]):
                    visualization.plot(vx, q[i], pen=pen, clear=False)
                    #visualization.plot(vx, q2[i], pen=pen, clear=False)

            pg.QtGui.QApplication.processEvents()


if __name__ == "__main__":
    vs = Visualizer()
    x, y, xf = vs.initialize_vars()
    runFlag = [True]
    plotting = threading.Thread(target=vs.plot, args=(x, y, xf, runFlag, False, True, False))

    plotting.start()
    plotting.join(1000)
    runFlag[0] = False
