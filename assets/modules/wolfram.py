#!/usr/bin/python
# -*- coding: utf-8 -*-

import wolframalpha

class Wolfram:

    def __init__(self):
        self.wolframID = '##############'
    def think(self, text):
        client = wolframalpha.Client(self.wolframID)
        res = client.query(text)
        if len(res.pods) > 0:
            pod = res.pods[1]
            return pod.text       
        else:
            return "I have no answer for that"
