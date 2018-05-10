import time
import os
import shutil
import _thread
import pyaudio
import wave
import IPython.display as ipd
from threading import Thread

def countdownThread(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1


def countdown(t):
    _thread.start_new_thread(countdownThread, (t, ))


def wait(t):
    print("Wait " + str(t) + "s")
    time.sleep(t)


def createDir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

def record(audioPath, record_seconds):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = record_seconds

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print(str(RECORD_SECONDS) + "s Recording Begin.")
    countdown(RECORD_SECONDS)
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("---> Record complete.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(audioPath, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()



# class ThreadWithReturn(Thread):
#     def __init__(self, *args, **kwargs):
#         super(ThreadWithReturn, self).__init__(*args, **kwargs)
#         self._return = None

#     def run(self):
#         if self._target is not None:
#             self._return = self._target(*self._args, **self._kwargs)

#     def join(self, *args, **kwargs):
#         super(ThreadWithReturn, self).join(*args, **kwargs)

#         return self._return