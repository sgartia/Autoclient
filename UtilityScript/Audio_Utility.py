"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""

import pyaudio
import wave
import sys
import time
from audiosocket import *


print("--- Local file playback example ---")
aw = AudioWriter()
aw.open()

# PCM 16bit, little endian, signed, 44.1kHz, stereo, left interleaved
with open('sample.raw', 'rb') as stream:
  aw.play(stream)

aw.close()


print("--- Playback from TCP port :44100 ---")
print("To feed an audio stream with netcat, execute:")
print("  nc -v localhost 44100 < sample.raw")

aw = AudioWriter()
aw.open()

while True:      
  stream = SocketStream(host='')
  print("got signal from %s:%s" % stream.addr)
  aw.play(stream)
  stream.close()

aw.close()


#CHUNK = 1024
#FORMAT = pyaudio.paInt16
#CHANNELS = 2
#RATE = 44100
#RECORD_SECONDS = 10
#WAVE_OUTPUT_FILENAME = "output.wav"

#p = pyaudio.PyAudio()


#stream = p.open(format=FORMAT,
                #channels=CHANNELS,
                #rate=RATE,
                #input=True,
                #frames_per_buffer=CHUNK)

#print("* recording")

#frames = []

#for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #data = stream.read(CHUNK)
    #frames.append(data)

#print("* done recording")

#stream.stop_stream()
#stream.close()
#p.terminate()

#wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#wf.setnchannels(CHANNELS)
#wf.setsampwidth(p.get_sample_size(FORMAT))
#wf.setframerate(RATE)
#wf.writeframes(b''.join(frames))
#wf.close()
#exit()

#CHUNK = 1024
#time.sleep(30)


#wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')

#p = pyaudio.PyAudio()

#stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                #channels=wf.getnchannels(),
                #rate=wf.getframerate(),
                #output=True)

#data = wf.readframes(CHUNK)

#while data != '':
    #stream.write(data)
    #data = wf.readframes(CHUNK)

#stream.stop_stream()
#stream.close()

#p.terminate()