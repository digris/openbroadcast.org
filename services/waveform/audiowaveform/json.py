import subprocess
import tempfile
import json
import os
import logging

from .exceptions import AudioWaveformException

AUDIOWAVEFORM_BINARY = "/usr/local/bin/audiowaveform"

log = logging.getLogger("audiowaveform")


def _extract_waveform_data(path):

    if not os.path.exists(path):
        raise (f"file does not exist: {path}")

    # TODO: do we need configurable bitrate?
    bitrate = 8

    if bitrate not in [8, 16]:
        raise AudioWaveformException(f"invalid bitrate: {bitrate} (use 8 or 16)")

    out_path = tempfile.mkstemp(suffix=".json")[1]

    command = f"{AUDIOWAVEFORM_BINARY} -b {bitrate} -i {path} -o {out_path}"

    log.info(f"command: {command}")

    with subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
    ) as p:
        output, errors = p.communicate()
        exit_code = p.returncode

    if not exit_code == 0 or errors:
        os.unlink(out_path)
        raise AudioWaveformException(
            f"unable to process file (aodiowaveform). exit code {exit_code} \n{output}"
        )

    log.debug(f"command output: \n{output}")

    with open(out_path) as json_file:
        try:
            raw_data = json.load(json_file)
        except json.decoder.JSONDecodeError as e:
            raise AudioWaveformException(f"unable to process file (JSON) {e}")
        finally:
            os.unlink(out_path)

    return raw_data


def _get_peaks(data, new_size):

    ratio = len(data) / new_size
    count = 0
    maximum_item = 0
    max_array = []

    for d in data:
        if count < ratio:
            count = count + 1
            if abs(d) > maximum_item:
                maximum_item = abs(d)

        else:
            max_array.append(maximum_item)
            maximum_item = 0
            count = 1

    peaks = [int(i) for i in max_array]

    return peaks


def process_waveform_data(raw_data, num_samples=1000, num_steps=100):

    _length = raw_data.get("length")
    if not _length:
        raise AudioWaveformException(
            "data seems not to be valid - missing key 'length'"
        )

    data = raw_data.get("data", [])
    del data[2 - 1 :: 2]
    data = [abs(i) for i in data]

    data = _get_peaks(data, num_samples)

    return data


def waveform_as_json(path):

    return _extract_waveform_data(path)
