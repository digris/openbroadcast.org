#-*- coding: utf-8 -*-
import subprocess

__ALL__ = 'duration_audiotools', 'duration_ffmpeg'

FFPROBE_BINARY = 'ffprobe'

def duration_audiotools(src):
    raise NotImplementedError


def duration_ffmpeg(src):

        try:
            p = subprocess.Popen([
                FFPROBE_BINARY, src, "-show_format"
            ], stdout=subprocess.PIPE)
            stdout = p.communicate()

            dur = stdout[0].split('duration=')[1]
            dur = dur.split("\n")[0]
            return float(dur) * 1000

        except Exception, e:
            print e