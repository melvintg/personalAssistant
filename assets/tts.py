
import os
import tempfile
import subprocess


class TTSEngine():
    def __init__(self, pitch=40, speed=140):
        self.pitch = pitch
        self.speed = speed

    def say(self, phrase):
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            tmpfile = f.name
            cmd = ['espeak', '-p', str(self.pitch), '-s', str(self.speed), '-w', tmpfile, phrase]
            subprocess.call(cmd, stdout=f, stderr=f)
            self.play(tmpfile)
            os.remove(tmpfile)

    def play(self, tmpfile):
        cmd = ['aplay', tmpfile]
        with tempfile.TemporaryFile() as f:
            subprocess.call(cmd, stdout=f, stderr=f)

if __name__ == '__main__':
    engine = TTSEngine()
    engine.say("This is a debuging test")
