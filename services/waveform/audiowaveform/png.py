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
    ca.logger.debug("validate file: %s", path)
    pass


def _convert_to_wav(path):

    ca.logger.debug("convert to wav: %s", path)

    wav_path = tempfile.mkstemp(suffix=".wav")[1]

    command = f"{FFMPEG_BINARY} -y -v error -i {path} -ar {RESAMPLE_RATE} {wav_path}"

    ca.logger.info("command: %s", command)

    with subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
    ) as p:
        output, errors = p.communicate()
        exit_code = p.returncode

    if exit_code != 0 or errors:
        os.unlink(wav_path)
        raise AudioWaveformException(
            f"unable to process file (ffmpeg). exit code {exit_code} \n{output}"
        )

    ca.logger.debug("command output: \n%s", output)

    return wav_path


def _get_duration(path):
    """
    ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 /data/data/sample.mp3
    """

    ca.logger.debug("get duration for: %s", path)

    command = f"{FFPROBE_BINARY} -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {path}"

    ca.logger.info("command: %s", command)

    with subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
    ) as p:
        output, errors = p.communicate()
        exit_code = p.returncode

    if not exit_code == 0 or errors:
        raise AudioWaveformException(
            f"unable to process file (ffprobe). exit code {exit_code} \n{output}"
        )

    ca.logger.debug("command output: \n%s", output)

    return int(float(output.strip()))


def _generate_png(path, duration, width=500, height=100, fg="000000", bg="ffffff"):
    """
    audiowaveform --no-axis-labels --background-color ffffff --waveform-color ffffff00 -w 1800 -h 301 -b 8 -e 292 -i ./data/Always.mp3 -o ./data/wfa.png
    """

    ca.logger.debug("convert to wav: %s", path)

    png_path = tempfile.mkstemp(suffix=".png")[1]

    command = f"{AUDIOWAVEFORM_BINARY} --no-axis-labels --background-color {bg} --waveform-color {fg} -w {width} -h {height} -b 8 -e {duration} -i {path} -o {png_path}"

    ca.logger.info("command: %s", command)

    with subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
    ) as p:
        output, errors = p.communicate()
        exit_code = p.returncode

    if not exit_code == 0 or errors:
        raise AudioWaveformException(
            f"unable to process file (ffprobe). exit code {exit_code} \n{output}"
        )

    ca.logger.debug("command output: \n%s", output)

    # just mocking...
    # import shutil
    # src = '/Users/ohrstrom/code/docker-images/audiowaveform/data/wfa.png'
    # shutil.copyfile(src, png_path)

    return png_path


def waveform_as_png(path, width, height, fg, bg, delete_after_processing=False):
    ca.logger.info("info bla: %s", path)
    ca.logger.warning("warning bla: %s", path)

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
