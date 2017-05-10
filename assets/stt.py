#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import urllib2 
import simplejson as json 



class STTEngine:

    def __init__(self,language='en-us',apiKey='#################################'):
        """
        Initiates the Google STT engine
        """
        self.language = language
        self.apiKey = apiKey

    def transcript(self,audioName='voice.wav'):
        f = open(audioName)
        audioFile = f.read()
        f.close()
        googl_speech_url = 'https://www.google.com/speech-api/v2/recognize?output=json&lang='+self.language+'&key='+self.apiKey
        hrs = {'Content-type': 'audio/l16; rate=16000'}
        req = urllib2.Request(googl_speech_url, data=audioFile, headers=hrs)
        rawData = urllib2.urlopen(req).read().lower()
        print rawData
        textFileClean = rawData.replace("""{"result":[]}""", '')
        if textFileClean != '\n':
            data = json.loads(textFileClean)
            parsedData = data['result'][0]['alternative'][0]['transcript']
        else:
            parsedData = "" 

        os.remove(audioName)
        return parsedData

if __name__ == '__main__':
    # STT Test
    stt = STTEngine()
    os.system("rec --encoding signed-integer --bits 16 --channels 1 --rate 16000 voice.wav silence 1 0.1 5% 1 1.0 5%")
    print stt.transcript('voice.wav')

  

