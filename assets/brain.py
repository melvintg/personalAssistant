#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from modules import tracker, alarm, wolfram, music, photo, jokes
from modules import calendarAPI
from modules import dropboxAPI
import tts

class Brain:
    def __init__(self, path):
        self.path = path

        self.tracker = None



        self.tracker = tracker.Tracker(path + "/modules/faces.xml", path + "/modules/eyes.xml")
        self.tracker.start()

        self.tts = tts.TTSEngine()

        self.alarm = alarm.Alarm()
        self.calendar = calendarAPI.CalendarAPI(path + "/", True)
        self.reminder = calendarAPI.CalendarAPI(path + "/", False)
        self.dropbox = dropboxAPI.Dropbox(path)
        self.music = music.Music(path + "/music/")
        self.joke = jokes.Jokes(path + "/modules/")
        self.webCam = photo.Photo(path)
        self.wolfram = wolfram.Wolfram()

        self.isWebCam = False

    def think(self, text):
        if "calendar" in text:
            response = "Processing Calendar Order"
            self.tts.say(response)
            print response
            response = self.calendar.think(text)
            
        elif ("remind" in text) | ("reminders" in text):
            response = "Processing Reminder Order"
            self.tts.say(response)
            response = self.reminder.think(text)

        elif ("timer" in text) | ("alarm" in text):
            response = self.alarm.think(text)

        elif ("time" in text):
            response = datetime.now().strftime("It's %I:%M%p")

        elif ("day" in text) | ("date" in text):
            response = datetime.now().strftime("%A %d of %B")

        elif ("download music" in text):
            response = "Downloading music from dropbox"
            self.tts.say(response)
            response = self.dropbox.downloadMusic()

        elif ("music" in text):
            if ("play" in text):
                response = self.music.play()
            else:
                response = self.music.stop()

        elif ("upload" in text):
            response = "Uploading photos to dropbox"
            self.tts.say(response)
            response = self.dropbox.uploadIMG()

        elif ("photo" in text):
            if self.isWebCam:
                response = self.webCam.takePhoto()
            else:
                response = "WebCam not active"

        elif ("wake" in text) | ("up" in text):
            self.tracker.resume()
            self.isWebCam = True
            response = "I'm waking up sir"

        elif ("sleep" in text) | ("stop" in text):
            self.tracker.pause()
            self.isWebCam = False
            response = "I'm going to sleep now"


        elif ("joke" in text):
            response = self.joke.think()

        else:
            response = self.wolfram.think(text)

        return response

if __name__ == '__main__':
    # Brain Test for debuging propose
    brain = Brain(os.getcwd())
    tts = tts.TTSEngine()
    for query in iter(lambda: raw_input('>>> '), ''):
        if "exit" in query:
            break
        response = brain.think(query)
        print response
        tts.say(response)

