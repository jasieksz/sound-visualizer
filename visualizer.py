import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

import struct
import pyaudio
import random
from scipy.fftpack import fft

import sys
import time
from argparse import ArgumentParser


class AudioStream(object):
    def __init__(self, audio_format, visId, signalFlag, spectrumFlag, time):
        self.signalFlag = signalFlag
        self.spectrumFlag = spectrumFlag
        
        self.visualizationId = visId
        self.traces = dict()
        self.app = QtGui.QApplication(sys.argv)
        self.win = pg.GraphicsWindow(title='Spectrum Analyzer')
        self.win.setWindowTitle('Spectrum Analyzer')
        self.win.setGeometry(5, 115, 1910, 1070)

        self.init_pg()
        self.init_pyaudio(audio_format, time)

        # waveform and spectrum x points
        self.x, self.fx = self.getXandFX()
        self.y, self.fy = self.getYandFY()
        self.vis2x, self.vis2y = self.getVis2Params()

        self.max_intensity = 0
        self.max_sig = 0


    def init_pg(self):
        pg.setConfigOptions(antialias=True)
        if self.signalFlag:
            self.waveform = self.win.addPlot(
                title='WAVEFORM', row=1, col=1)
        if self.spectrumFlag:
            self.spectrum = self.win.addPlot(
                title='SPECTRUM', row=2, col=1)
        self.visualization = self.win.addPlot(title='VISUALIZATION', row=3, col=1)


    def init_pyaudio(self, audio_format, time):
        # pyaudio stuff
        self.FORMAT = audio_format
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.SMOOTHING = 0.75
        self.time = time

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK,
        )

    def getVis2Params(self):
        return np.arange(0, self.CHUNK), np.arange(0, self.CHUNK)

    def getXandFX(self):
        x = np.linspace(0, self.CHUNK / self.RATE, self.CHUNK)
        freq = np.fft.fftfreq(self.CHUNK, x[1] - x[0])
        return x, freq

    def getYandFY(self):
        y = np.zeros(self.CHUNK)
        fy = np.zeros(self.CHUNK)
        return y, fy

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def set_plotdata(self, name, data_x, data_y, pen):
        if name in self.traces:
            if self.visualizationId == 1 and name == 'visualization1':
                self.traces[name].setPen(pen)
                self.traces[name].setData(data_x, data_y)
            elif self.visualizationId == 2 and name == 'visualization2':
                self.traces[name].setPen(pen)
                self.traces[name].setData(data_x, data_y)
            elif self.visualizationId == 3 and name == 'visualization3':
                #
                # ADD YOUR CODE HERE
                #
                pass
            else:
                self.traces[name].setData(data_x, data_y)
        else:
            if self.signalFlag and name == 'waveform':
                self.traces[name] = self.waveform.plot(pen='c', width=3)
                self.waveform.setYRange(-2 ** 15, 2 ** 15, padding=0)
                self.waveform.setXRange(0, max(self.x), padding=0.005)
            if self.spectrumFlag and name == 'spectrum':
                pen = pg.mkPen(color=(0, 150, 0))
                self.spectrum.setYRange(0, 10000, padding=0)
                self.traces[name] = self.spectrum.plot(pen=pen, width=3)
            if self.visualizationId == 1 and name == 'visualization1':
                self.traces[name] = self.visualization.plot(pen='c')

            if self.visualizationId == 2 and name == 'visualization2':
                self.traces[name] = self.visualization.plot(pen='c')
                self.visualization.setYRange(0, self.CHUNK)
                self.visualization.setXRange(0, self.CHUNK)

            if self.visualizationId == 3 and name == 'visualization3':
                #
                # ADD YOUR CODE HERE
                #
                pass

    def update(self):
        self.update_spectrum()
        self.update_transform()

        if self.spectrumFlag:
            self.set_plotdata(name='spectrum', data_x=self.fx, data_y=self.fy, pen='c')

        if self.visualizationId == 1:
            v1x, v1y, pen1 = self.visualize_1(self.fx, self.fy)
            self.set_plotdata("visualization1", v1x, v1y, pen1)
        elif self.visualizationId == 2:
            v2x, v2y, pen2 = self.visualize_2(self.vis2x, self.vis2y)
            self.set_plotdata("visualization2", v2x, v2y, pen2)
        elif self.visualizationId == 3:
            pass
            #
            # ADD YOUR CODE HERE
            #

    def update_spectrum(self):
        wf_data = self.stream.read(self.CHUNK)
        wf_data = struct.unpack("%dh" % self.CHUNK, wf_data)
        self.y = self.y * self.SMOOTHING
        self.y += np.array(wf_data) * (1 - self.SMOOTHING)
        if self.signalFlag:
            self.set_plotdata(name='waveform', data_x=self.x, data_y=self.y, pen='m')

    def update_transform(self):
        transformed = (np.abs(np.fft.fft(self.y)) * np.blackman(self.CHUNK)).clip(min=1)
        self.fy = self.fy * self.SMOOTHING
        self.fy += (1 - self.SMOOTHING) * transformed
        self.fy = np.where(self.fy > 11, self.fy, 1)

    def visualize_1(self, x, y):
        vx = np.arange(100)
        vy = np.zeros(100)
        for i in range(100):
            vy[i] = np.mean(y[i * y.shape[0] // 100: (i + 1) * y.shape[0] // 100])

        intensity = np.mean(self.fy)
        self.max_intensity = max(intensity, self.max_intensity)
        r = int(255 * intensity / self.max_intensity)

        self.max_intensity *= 0.999
        return vx, vy, pg.mkPen(color=(r, 30, 255 - r))

    def visualize_2(self, vx, vy):
        new_max_sig = np.max(self.y)
        if new_max_sig > self.max_sig:
            self.max_sig = new_max_sig
            beginning = np.argmax(self.fy[self.CHUNK // 4:self.CHUNK // 2])
            beginning = 4 * beginning
            rise = self.CHUNK - vy[beginning]
            vy[beginning] = self.CHUNK
            val = rise
            for i in range(beginning + 1, self.CHUNK):
                vy[i] = min(self.CHUNK * 2, vy[i] + val)
                val *= 0.9
            val = rise
            for i in range(beginning - 1, 0, -1):
                vy[i] = min(self.CHUNK * 2, vy[i] + val)
                val *= 0.9
        for i in range(self.CHUNK):
            vy[i] *= 0.95

        intensity = np.mean(self.fy)
        self.max_intensity = max(intensity, self.max_intensity)
        r = int(255 * intensity / self.max_intensity)

        self.max_intensity *= 0.999
        self.max_sig *= 0.9
        return vx, vy, pg.mkPen(color=(r, 30, 255 - r))

    def visualize_3(self, vx, vy):
        #
        # ADD YOUR CODE HERE
        #
        return vx, vy, pg.mkPen(color=(0, 0, 0))


    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        if self.time < 0:
            timer.start()
        else:
            timer.start(self.time)
        self.start()



if __name__ == '__main__':
    argparser = ArgumentParser(description='Visualize audio')
    argparser.add_argument('-vis', type=int, help='Pick visualization', default=1, choices=[1,2,3]) # Add your own
    argparser.add_argument('-time', type=int, help='How long the visualization plays [seconds], -1=infinitely', default=(-1))
    argparser.add_argument('--signal', type=bool, help='Show signal plot', default=False)
    argparser.add_argument('--spectrum', type=bool, help='Show spectrum plot', default=False)
    argparser.add_argument('-format', type=str, help='Audio device format, one of Int16, Int32, Float32', default='Int16', choices=['Int16', 'Int32', 'Float32'])

    args = argparser.parse_args()
    formats = {
        'Int16': pyaudio.paInt16, 
        'Int32': pyaudio.paInt32, 
        'Float32': pyaudio.paFloat32
    }
    audio_format = formats[args.format]

    audio_app = AudioStream(audio_format, args.vis, args.signal, args.spectrum, args.time)
    audio_app.animation()
