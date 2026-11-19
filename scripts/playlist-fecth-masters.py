# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""
fetch the master files of a playlist from the production storage into data/media/.

- looks up the master paths in the local dev database (compose service `mariadb`)
- copies the files with rsync from the ssh host `obp-lw` (see README, `~/.ssh/config`)

Read-only on the remote side, only files missing locally are requested.

The production dump marks the derived assets (encoded versions, waveforms) as
"done", but their files are not available locally. Those records are reset, so
the app re-creates them from the fetched masters (on export, in the editor, ...).

Example:
    $ uv run scripts/playlist-fecth-masters.py 68494f1a-d139-4a4e-b154-f4bfc1a18e91
    $ uv run scripts/playlist-fecth-masters.py 68494f1a-d139-4a4e-b154-f4bfc1a18e91 --dry-run
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

# uuids are stored as 32 hex chars, master paths relative to MEDIA_ROOT
QUERY = """
SELECT m.master, m.id
FROM alibrary_playlist p
JOIN alibrary_playlistitemplaylist pip ON pip.playlist_id = p.id
JOIN alibrary_playlistitem pi ON pi.id = pip.item_id
JOIN django_content_type ct ON ct.id = pi.content_type_id
JOIN alibrary_media m ON m.id = pi.object_id
WHERE p.uuid = '{uuid}' AND ct.app_label = 'alibrary' AND ct.model = 'media'
ORDER BY pip.position
"""

# derived assets of the playlist's media. see media_asset.models
QUERY_ASSETS = """
SELECT 'format', f.id, f.media_uuid, CONCAT(f.quality, '.', f.encoding)
FROM media_asset_format f
JOIN ({media}) m ON m.id = f.media_id
WHERE f.status = 1
UNION ALL
SELECT 'waveform', w.id, w.media_uuid, CONCAT(w.type, '.png')
FROM media_asset_waveform w
JOIN ({media}) m ON m.id = w.media_id
WHERE w.status = 1;
"""
ASSET_STATUS_INIT = 0


def run_sql(sql):
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
    return [line.split("\t") for line in output.splitlines()]


def get_master_paths(playlist_uuid):
    paths = [row[0].strip() for row in run_sql(QUERY.format(uuid=playlist_uuid.hex))]
    # unique, keep order. skip media without master
    return list(dict.fromkeys(p for p in paths if p and p != "NULL"))


def reset_missing_assets(playlist_uuid, dry_run=False):
    """
    set format / waveform records without a local file back to "initial".
    """
    rows = run_sql(QUERY_ASSETS.format(media=QUERY.format(uuid=playlist_uuid.hex)))
    for table in ("format", "waveform"):
        ids = [
            asset_id
            for kind, asset_id, media_uuid, filename in rows
            if kind == table and not asset_path(kind, media_uuid, filename).exists()
        ]
        print(f"{table}s to reset: {len(ids)}")
        if ids and not dry_run:
            run_sql(
                f"UPDATE media_asset_{table} SET status = {ASSET_STATUS_INIT} "
                f"WHERE id IN ({', '.join(ids)});"
            )


def asset_path(kind, media_uuid, filename):
    # see media_asset.models: <kind>/aa/bb/cc/dd/eeee/ffff/gggg/hhhhhhhhhhhh/<filename>
    u = uuid.UUID(media_uuid)
    parts = str(u).split("-")
    head = parts[0]
    directory = [head[0:2], head[2:4], head[4:6], head[6:8], *parts[1:]]
    return LOCAL_MEDIA_ROOT.joinpath("media_asset", kind, *directory, filename)


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
    p.add_argument("uuid", type=uuid.UUID, help="playlist UUID")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="show what would be copied",
    )
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()

    paths = get_master_paths(args.uuid)
    if not paths:
        sys.exit(f"no masters found for playlist: {args.uuid}")

    missing = [p for p in paths if not (LOCAL_MEDIA_ROOT / p).exists()]
    print(f"masters: {len(paths)} - missing locally: {len(missing)}")
    if missing:
        returncode = rsync_files(missing, dry_run=args.dry_run)
        if returncode:
            sys.exit(returncode)

    reset_missing_assets(args.uuid, dry_run=args.dry_run)
