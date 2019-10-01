# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import audiotools
from ffprobe import FFProbe


def encoding_for_path(path):
    basename, ext = os.path.splitext(path)
    return ext[1:].lower()


def filesize_for_path(path):
    if os.path.isfile(path):
        return os.path.getsize(path)


def bitrate_for_path(path):
    if os.path.isfile(path):
        pass


def samplerate_for_path(path):
    if os.path.isfile(path):
        audiofile = audiotools.open(path)
        return audiofile.sample_rate()


def duration_for_path(path):
    if os.path.isfile(path):
        audiofile = audiotools.open(path)
        return audiofile.seconds_length()


class FileInfoProcessor(object):
    def __init__(self, path):
        if not os.path.isfile(path):
            raise IOError("unable to read file at: %s" % path)
        self.path = path
        self.audio_stream = None

        self.ffprobe()

    def ffprobe(self):
        meta = FFProbe(self.path)
        for stream in meta.streams:
            if stream.isAudio():
                self.audio_stream = stream
                break

    @property
    def filesize(self):
        return os.path.getsize(self.path)

    @property
    def encoding(self):

        basename, ext = os.path.splitext(self.path)
        return ext[1:].lower()

        # if self.audio_stream:
        #     return self.audio_stream.codec_name
        #     #return self.audio_stream.codecTag()

    @property
    def bitrate(self):
        if self.audio_stream:
            try:
                bitrate = self.audio_stream.bitrate()
                if bitrate:
                    return int(bitrate / 1000)
            except:
                pass

    @property
    def duration(self):
        if self.audio_stream:
            return self.audio_stream.durationSeconds()

    @property
    def samplerate(self):
        if self.audio_stream:
            try:
                return int(self.audio_stream.sample_rate)
            except:
                pass
