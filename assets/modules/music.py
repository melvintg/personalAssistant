#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess, os

class Music:
    def __init__(self, path):
        self.player =  None
        self.path = path

    def play(self):
        # The os.setsid() is passed in the argument preexec_fn so
        # it's run after the fork() and before  exec() to run the shell.
        #pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
        #os.killpg(pro.pid, signal.SIGTERM)  # Send the signal to all the process groups

        self.player = subprocess.Popen("exec " + "mpg123 *.mp3", cwd = self.path, stdout=subprocess.PIPE, shell= True)
        return "Playing music"

    def stop(self):
        if self.player != None:
            self.player.kill()
        return "."

if __name__ == '__main__':
    # Music Test
    path = os.getcwd()
    music = Music("/".join(path.split("/")[0:-1]) + "/music/")
    music.play()
    