import struct

import pyaudio
import wave
import threading
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time
import audioop

CHUNK = 1024
FORMAT = pyaudio.paInt16
Y_MAX = 2 ** 15
CHANNELS = 1
RATE = 44100
LAST_SECONDS = 1
SMOOTHING = 0.6
FPS = 30
SAMPLES = RATE//CHUNK
SAMPLE_DELTA = RATE//CHUNK


def mean_bytes(data):
    parsed = np.array(struct.unpack("%dh" % (CHUNK * CHANNELS), data))
    mean = parsed[::CHANNELS]
    for i in range(1, CHANNELS):
        mean += parsed[i::CHANNELS]
    return mean // CHANNELS


def do_fft(data):
    parsed = np.array(struct.unpack("%dh" % CHUNK, data))
    return np.abs(np.fft.fft(parsed)) * np.blackman(CHUNK)



def streaming_thread(stream, line1, line2, keep_running):
    while keep_running[0]:
        y = np.array(struct.unpack("%dh" % CHUNK, stream.read(CHUNK)))
        yf = 20 * np.log10(1 + np.abs(np.blackman(CHUNK) * np.fft.fft(y)))
        line1.set_ydata(y)
        line2.set_ydata(yf)

def th1(stream, xs, ys, keep_running):
    xd = True
    while keep_running[0]:
        # ys[...] = np.roll(ys, -CHUNK)
        # n = len(ys)
        # data = stream.read(CHUNK)
        # ys[n - 1 - CHUNK: n - 1] = mean_bytes(data)
        # if xd:
        #     do_fft(data)
        #     xd = False
        # new_shit = np.zeros(SAMPLES)
        # for i in range(SAMPLES):
        #     data = stream.read(CHUNK)
        #     m = audioop.max(data, 2)
        #     new_shit[i] = m

        # print(".")
        # new_y = do_fft(stream.read(CHUNK))
        # ys[...] = SMOOTHING * new_y + (1 - SMOOTHING) * ys
        y = np.sin(50.0 * 2.0 * np.pi * xs) + 0.5 * np.sin(80.0 * 2.0 * np.pi * xs)
        ys[...] = np.abs(np.fft.fft(y))


def update_line(num, xs, ys, line):
    line.set_data((xs, ys))
    return line,


if __name__ == "__main__":
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    samples_count = int(LAST_SECONDS * RATE)
    res = np.zeros(samples_count)

    # fig1 = plt.figure()

    # ys = np.zeros(CHUNK)
    # T = dt * N
    # N = CHUNK
    # dt = 1/RATE
    # df = 1/T = 1/(CHUNK/RATE) = RATE/CHUNK
    # dw = 2pi df
    # ny = df * N/2 = RATE/CHUNK * CHUNK/2 = RATE/2
    # f = np.fft.fftfreq(CHUNK) * RATE

    keep_running = [True]

    # t = threading.Thread(target=th1, args=(stream, xs, ys, keep_running))
    # t.start()

    # l, = plt.plot([], [], 'r-')
    # plt.xlim(0, RATE/2)
    # plt.ylim(0, 500)
    # plt.xlabel('x')
    # plt.title('test')
    # line_ani = animation.FuncAnimation(fig1, update_line, 25, fargs=(xf, ys, l),
    #

    x = np.linspace(0, CHUNK / RATE, CHUNK)
    y = np.full(CHUNK, 22767)
    y[1] = -22767
    yf = 20*np.log10(1 + np.abs(np.fft.fft(y)))
    xf = np.fft.fftfreq(y.size, x[1] - x[0])

    plt.ion()
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    line1, = ax1.plot(x, y, 'r-')
    line2, = ax2.plot(xf, yf, 'b-')

    t = threading.Thread(target=streaming_thread, args=(stream, line1, line2, keep_running))
    t.start()

    while keep_running[0]:
        fig.canvas.draw()

        plt.pause(0.001)

    # plt.subplot(211)
    # plt.plot(x, y)
    # plt.subplot(212)
    # plt.plot(xf, yf)
    # plt.show()
    keep_running[0] = False

    stream.stop_stream()
    stream.close()
    p.terminate()

# # n = len(res)
# # k = np.arange(n)
# # T = n / Fs
# # frq = k/T
# # frq = frq[range(n//2)]
# #
# # Y = np.fft.fft(res)/n
# # Y = Y[range(n//2)]
#
# x = np.linspace(0.0, listen, samples_count)
# plt.plasma()
# plt.plot(x, res)
# plt.show()
#
# xf = np.linspace(0.0, Fs/2, samples_count//2)
# yf = 2.0 / samples_count * np.abs(np.fft.fft(res)[:samples_count//2])
#
