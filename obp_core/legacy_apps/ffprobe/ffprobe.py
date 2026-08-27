#!/usr/bin/python
"""
Python wrapper for ffprobe command line tool.
"""

import os
import platform
import subprocess
from django.conf import settings


FFPROBE_BINARY = getattr(settings, "FFPROBE_BINARY")


class FFProbe:
    """
    FFProbe wraps the ffprobe command and pulls the data into an object form::
        metadata = FFProbe('multimedia-file.mov')
    """

    def __init__(self, video_file):
        self.video_file = video_file

        try:
            with open(os.devnull, "w") as tempf:
                subprocess.check_call(
                    [FFPROBE_BINARY, "-h"],
                    stdout=tempf,
                    stderr=tempf,
                )
        except Exception as exc:
            raise OSError("ffprobe not found.") from exc

        if not os.path.isfile(video_file):
            raise OSError("No such media file " + video_file)

        cmd = [FFPROBE_BINARY, "-show_streams", video_file]

        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=False,
        )

        self.format = None
        self.created = None
        self.duration = None
        self.start = None
        self.bitrate = None
        self.streams = []
        self.video = []
        self.audio = []

        datalines = []

        for line in p.stdout:
            line = line.strip()
            if line == "[STREAM]":
                datalines = []
            elif line == "[/STREAM]":
                self.streams.append(FFStream(datalines))
                datalines = []
            else:
                datalines.append(line)

        p.stdout.close()
        p.stderr.close()
        p.wait()

        for stream in self.streams:
            if stream.isAudio():
                self.audio.append(stream)
            if stream.isVideo():
                self.video.append(stream)


class FFStream:
    """
    An object representation of an individual stream in a multimedia file.
    """

    def __init__(self, datalines):
        for line in datalines:
            if "=" not in line:
                continue
            key, val = line.strip().split("=", 1)
            setattr(self, key, val)

    def isAudio(self):
        return getattr(self, "codec_type", None) == "audio"

    def isVideo(self):
        return getattr(self, "codec_type", None) == "video"

    def isSubtitle(self):
        return getattr(self, "codec_type", None) == "subtitle"

    def frameSize(self):
        size = None
        if self.isVideo():
            width = getattr(self, "width", None)
            height = getattr(self, "height", None)
            if width and height:
                try:
                    size = (int(width), int(height))
                except Exception:
                    size = (0, 0)
        return size

    def pixelFormat(self):
        if self.isVideo():
            return getattr(self, "pix_fmt", None)
        return None

    def frames(self):
        f = 0
        if self.isVideo() or self.isAudio():
            nb_frames = getattr(self, "nb_frames", None)
            if nb_frames:
                try:
                    f = int(nb_frames)
                except Exception:
                    print("None integer frame count")
        return f

    def durationSeconds(self):
        f = 0.0
        if self.isVideo() or self.isAudio():
            duration = getattr(self, "duration", None)
            if duration:
                try:
                    f = float(duration)
                except Exception:
                    print("None numeric duration")
        return f

    def language(self):
        return getattr(self, "TAG:language", None)

    def codec(self):
        return getattr(self, "codec_name", None)

    def codecDescription(self):
        return getattr(self, "codec_long_name", None)

    def codecTag(self):
        return getattr(self, "codec_tag_string", None)

    def bitrate(self):
        b = 0
        bit_rate = getattr(self, "bit_rate", None)
        if bit_rate:
            try:
                b = int(bit_rate)
            except Exception:
                pass
        return b


if __name__ == "__main__":
    print("Module ffprobe")