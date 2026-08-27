#!/usr/bin/env python3
"""
download obp master files for debugging.
ssh needs to be configured.

Example:
    $ ./download_master.py 74ada867-5419-475c-9a8e-9a3042db4b9e .
"""
import argparse
import os
import subprocess


HOST = "37.48.80.2"
BASE_PATH = "/nas/storage/prod.openbroadcast.org/media/private/"


class DownloaderException(Exception):
    pass


def get_remote_path(uuid):
    path = os.path.join(BASE_PATH, *uuid.split("-"))
    try:
        output = subprocess.check_output(
            [
                "ssh",
                HOST,
                "find",
                path,
                "-type",
                "f",
            ],
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError:
        raise DownloaderException("unable to get remote path")

    lines = output.splitlines()

    try:
        assert len(lines) == 1
    except AssertionError:
        raise DownloaderException("unable to get remote path")

    return lines[0].decode()


def rsync_file(remote_path, local_path):
    try:
        subprocess.check_output(
            [
                "rsync",
                f"{HOST}:{remote_path}",
                local_path,
            ],
            stderr=subprocess.STDOUT,
        )
        return local_path
    except subprocess.CalledProcessError as e:
        raise DownloaderException("unable to download file")


def download_file(uuid, path):

    if not os.path.isdir(path):
        raise IOError(f"path is not a directory: {path}")

    remote_path = get_remote_path(uuid=uuid)
    filename, ext = os.path.splitext(os.path.basename(remote_path))
    local_path = os.path.join(path, f"{uuid}{ext}")

    print(f"remote: {remote_path}")
    print(f"local:  {local_path}")
    return rsync_file(remote_path=remote_path, local_path=local_path)


def parse_args():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "uuid",
        help="media UUID",
    )
    p.add_argument(
        "dst",
        help="destination (path or file)",
    )

    return p.parse_args()


if __name__ == "__main__":

    args = parse_args()
    uuid = args.uuid
    path = os.path.abspath(args.dst)

    try:
        out_path = download_file(uuid=uuid, path=path)
        print(f"downloaded file to: {out_path}")
    except DownloaderException as e:
        print(f"error downloading: {e}")
