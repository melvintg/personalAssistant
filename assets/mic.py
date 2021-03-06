import pyaudio
import struct
import math
import wave 
import urllib2 
import os
import tempfile


class Microphone:

    def __init__(self,language='en-us',apiKey='#################################'):
        """
        Initiates the Google STT engine
        """
        self.language = language
        self.apiKey = apiKey

    def rms(self,frame):
        count = len(frame)/2
        format = "%dh"%(count)
        shorts = struct.unpack( format, frame )
        sum_squares = 0.0
        for sample in shorts:
            n = sample * (1.0/32768.0)
            sum_squares += n*n
        rms = math.pow(sum_squares/count,0.5);
        return rms * 1000

    def passiveListen(self,persona):

        CHUNK = 1024; RATE = 16000; THRESHOLD = 100; LISTEN_TIME = 5

        didDetect = False
        
        # prepare recording stream
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

        # stores the audio data
        all =[]

        # starts passive listening for disturbances 
        for i in range(0, RATE / CHUNK * LISTEN_TIME):
            input = stream.read(CHUNK)
            rms_value = self.rms(input)
            if (rms_value > THRESHOLD):
                didDetect = True
                print "Listening...\n"
                break

        if not didDetect:
            stream.stop_stream()
            stream.close()
            return False

        # append all the chunks
        all.append(input)
        for i in range(0, 10):
            data = stream.read(CHUNK)
            all.append(data)

        # save the audio data   
        data = ''.join(all)
        stream.stop_stream()
        stream.close()

        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            tmpfile = f.name
            wf = wave.open(tmpfile, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(RATE)
            wf.writeframes(data)
            wf.close()
            # check if persona was said
            fp = open(tmpfile)
            audioFile = fp.read()
            fp.close()
            os.remove(tmpfile)

        googl_speech_url = 'https://www.google.com/speech-api/v2/recognize?output=json&lang='+self.language+'&key='+self.apiKey
        hrs = {'Content-type': 'audio/l16; rate=16000'}
        req = urllib2.Request(googl_speech_url, data=audioFile, headers=hrs)
        rawData = urllib2.urlopen(req).read().lower()
        print rawData

        if persona in rawData:
            os.system ('mpg123 assets/beep.mp3')
            return True

        return False
