import os
import shutil
import subprocess
import logging

from django.conf import settings

log = logging.getLogger(__name__)

FFMPEG_BINARY = getattr(settings, "FFMPEG_BINARY")


def any_to_wav(src, dst):
    log.info("ffmpeg to wav: %s -> %s", src, dst)

    if not os.path.isfile(src):
        raise OSError(f"unable to access {src}")

    command = [
        FFMPEG_BINARY,
        "-y",
        "-v", "error",
        "-i", src,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-ac", "2",
        dst,
    ]

    log.debug("running: %s", " ".join(command))

    p = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if p.returncode != 0:
        log.error("ffmpeg failed: %s", p.stderr.decode("utf-8", "ignore"))
        raise RuntimeError(f"ffmpeg failed for {src}")

    if not os.path.exists(dst):
        log.warning("output not created: %s", dst)
        return None

    return dst



