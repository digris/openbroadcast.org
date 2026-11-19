# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""
fetch playlist images from the production storage into data/media/.

- with a playlist uuid: images of the playlist itself, its author (profile) and
  for every track the artist, release and label.
- without: the images of all playlists (the playlist image only).

- looks up the image paths in the local dev database (compose service `mariadb`)
- copies the files with rsync from the ssh host `obp-lw` (see README, `~/.ssh/config`)

Read-only on the remote side, only files missing locally are requested.

Example:
    $ uv run scripts/playlist-fecth-images.py 68494f1a-d139-4a4e-b154-f4bfc1a18e91
    $ uv run scripts/playlist-fecth-images.py 68494f1a-d139-4a4e-b154-f4bfc1a18e91 --dry-run
    $ uv run scripts/playlist-fecth-images.py
"""

import argparse
import subprocess
import sys
import uuid
from pathlib import Path

SSH_HOST = "obp-lw"
REMOTE_MEDIA_ROOT = "/nas/storage/prod.openbroadcast.org/media/"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOCAL_MEDIA_ROOT = PROJECT_ROOT / "data" / "media"
COMPOSE_FILE = PROJECT_ROOT / "devsupport" / "compose.yml"

# uuids are stored as 32 hex chars, image paths relative to MEDIA_ROOT
QUERY = """
SELECT p.main_image
FROM alibrary_playlist p
WHERE p.uuid = '{uuid}'
UNION
SELECT pr.image
FROM alibrary_playlist p
JOIN user_profiles pr ON pr.user_id = p.user_id
WHERE p.uuid = '{uuid}'
UNION
SELECT a.main_image
FROM ({media}) m
JOIN alibrary_artist a ON a.id = m.artist_id
UNION
SELECT r.main_image
FROM ({media}) m
JOIN alibrary_release r ON r.id = m.release_id
UNION
SELECT l.main_image
FROM ({media}) m
JOIN alibrary_release r ON r.id = m.release_id
JOIN alibrary_label l ON l.id = r.label_id;
"""

QUERY_ALL = """
SELECT DISTINCT p.main_image
FROM alibrary_playlist p
WHERE p.main_image IS NOT NULL AND p.main_image != '';
"""

QUERY_MEDIA = """
SELECT m.artist_id, m.release_id
FROM alibrary_playlist p
JOIN alibrary_playlistitemplaylist pip ON pip.playlist_id = p.id
JOIN alibrary_playlistitem pi ON pi.id = pip.item_id
JOIN django_content_type ct ON ct.id = pi.content_type_id
JOIN alibrary_media m ON m.id = pi.object_id
WHERE p.uuid = '{uuid}' AND ct.app_label = 'alibrary' AND ct.model = 'media'
"""


def get_image_paths(playlist_uuid=None):
    if playlist_uuid:
        media = QUERY_MEDIA.format(uuid=playlist_uuid.hex)
        sql = QUERY.format(uuid=playlist_uuid.hex, media=media)
    else:
        sql = QUERY_ALL
    output = subprocess.check_output(
        [
            "docker",
            "compose",
            "-f",
            str(COMPOSE_FILE),
            "exec",
            "-T",
            "mariadb",
            "mariadb",
            "-uobp",
            "-pobp",
            "obp",
            "--batch",
            "--skip-column-names",
            "-e",
            sql,
        ],
        text=True,
    )
    paths = [line.strip() for line in output.splitlines()]
    # skip objects without image
    return sorted({p for p in paths if p and p != "NULL"})


def rsync_files(paths, dry_run=False):
    LOCAL_MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
    command = [
        "rsync",
        "--times",
        "--verbose",
        "--human-readable",
        "--files-from=-",
        f"{SSH_HOST}:{REMOTE_MEDIA_ROOT}",
        f"{LOCAL_MEDIA_ROOT}/",
    ]
    if dry_run:
        command.insert(1, "--dry-run")
    return subprocess.run(command, input="\n".join(paths) + "\n", text=True).returncode


def parse_args():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "uuid",
        type=uuid.UUID,
        nargs="?",
        help="playlist UUID (default: all playlists)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="show what would be copied",
    )
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()

    paths = get_image_paths(args.uuid)
    if not paths:
        sys.exit(f"no images found for playlist: {args.uuid or 'all'}")

    missing = [p for p in paths if not (LOCAL_MEDIA_ROOT / p).exists()]
    print(f"images: {len(paths)} - missing locally: {len(missing)}")
    if not missing:
        sys.exit(0)

    sys.exit(rsync_files(missing, dry_run=args.dry_run))
