import logging
import subprocess
import os
import tempfile
from flask import current_app as ca

from .exceptions import AudioWaveformException

# FFPROBE_BINARY = "/usr/bin/ffprobe"
# FFMPEG_BINARY = "/usr/bin/ffmpeg"

FFPROBE_BINARY = "ffprobe"
FFMPEG_BINARY = "ffmpeg"

AUDIOWAVEFORM_BINARY = "/usr/local/bin/audiowaveform"

RESAMPLE_RATE = 8000


def _validate_file(path):
    ca.logger.debug("validate file: {}".format(path))
    pass


def _convert_to_wav(path):

    ca.logger.debug("convert to wav: {}".format(path))

    wav_path = tempfile.mkstemp(suffix=".wav")[1]

    command = "{binary} -y -v error -i {input} -ar {sample_rate} {output}".format(
        binary=FFMPEG_BINARY,
        input=path,
        sample_rate=RESAMPLE_RATE,
        output=wav_path,
    )

    ca.logger.info("command: {}".format(command))

    with subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
    ) as p:
        output, errors = p.communicate()
        exit_code = p.returncode

    if not exit_code == 0 or errors:
        os.unlink(wav_path)
        raise AudioWaveformException(
            "unable to process file (ffmpeg). exit code {} \n{}".format(
                exit_code, output
            )
        )

    ca.logger.debug("command output: \n{}".format(output))

    return wav_path


def _get_duration(path):

    """
    ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 /data/data/sample.mp3
    """

    ca.logger.debug("get duration for: {}".format(path))

    command = "{binary} -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {input}".format(
        binary=FFPROBE_BINARY, input=path
    )

    ca.logger.info("command: {}".format(command))

    with subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
    ) as p:
        output, errors = p.communicate()
        exit_code = p.returncode

    if not exit_code == 0 or errors:
        raise AudioWaveformException(
            "unable to process file (ffprobe). exit code {} \n{}".format(
                exit_code, output
            )
        )

    ca.logger.debug("command output: \n{}".format(output))

    return int(float(output.strip()))


def _generate_png(path, duration, width=500, height=100, fg="000000", bg="ffffff"):

    """
    audiowaveform --no-axis-labels --background-color ffffff --waveform-color ffffff00 -w 1800 -h 301 -b 8 -e 292 -i ./data/Always.mp3 -o ./data/wfa.png
    """

    ca.logger.debug("convert to wav: {}".format(path))

    png_path = tempfile.mkstemp(suffix=".png")[1]

    command = "{binary} --no-axis-labels --background-color {bg} --waveform-color {fg} -w {width} -h {height} -b 8 -e {duration} -i {input} -o {output}".format(
        binary=AUDIOWAVEFORM_BINARY,
        duration=duration,
        fg=fg,
        bg=bg,
        height=height,
        width=width,
        input=path,
        output=png_path,
    )

    ca.logger.info("command: {}".format(command))

    with subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
    ) as p:
        output, errors = p.communicate()
        exit_code = p.returncode

    if not exit_code == 0 or errors:
        raise AudioWaveformException(
            "unable to process file (ffprobe). exit code {} \n{}".format(
                exit_code, output
            )
        )

    ca.logger.debug("command output: \n{}".format(output))

    # just mocking...
    # import shutil
    # src = '/Users/ohrstrom/code/docker-images/audiowaveform/data/wfa.png'
    # shutil.copyfile(src, png_path)

    return png_path


def waveform_as_png(path, width, height, fg, bg, delete_after_processing=False):
    ca.logger.info("info bla: {}".format(path))
    ca.logger.warning("warning bla: {}".format(path))

    wav_path = _convert_to_wav(path)
    duration = _get_duration(wav_path)
    png_path = _generate_png(
        wav_path, duration, width=width, height=height, fg=fg, bg=bg
    )

    # TODO: cleanup temporary files
    if delete_after_processing:
        os.unlink(path)
    os.unlink(wav_path)

    return png_path
