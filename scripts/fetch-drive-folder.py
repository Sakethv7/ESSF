#!/usr/bin/env python3
"""Enumerate and download a public Google Drive folder into a staging directory.

The folder listing comes from Drive's `embeddedfolderview` endpoint, which is
server-rendered and returns every entry in one request — unlike the normal
folder page, which renders its listing client-side.

Usage:
  python3 scripts/fetch-drive-folder.py <folder_url_or_id> <staging_dir> [--enumerate-only]

Example:
  python3 scripts/fetch-drive-folder.py 12PCLhyLQlAps8Hng_GHlSaXdQEFglHeq ~/tmp/bharat-raw
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx

EMBED_URL = "https://drive.google.com/embeddedfolderview?id={folder_id}#list"
DOWNLOAD_URL = "https://drive.google.com/uc?export=download&id={file_id}"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"

ENTRY_RE = re.compile(
    r'id="entry-([0-9A-Za-z_-]+)".*?flip-entry-title">([^<]+)<', re.DOTALL
)
FOLDER_ID_RE = re.compile(r"folders/([0-9A-Za-z_-]+)")


def parse_folder_id(value: str) -> str:
    match = FOLDER_ID_RE.search(value)
    return match.group(1) if match else value


def enumerate_folder(folder_id: str) -> list[dict]:
    """Return [{drive_id, name}] for every entry in the folder, in listing order."""
    url = EMBED_URL.format(folder_id=folder_id)
    response = httpx.get(url, headers={"User-Agent": USER_AGENT}, follow_redirects=True, timeout=60)
    response.raise_for_status()

    # Split per entry so a missing title can't pair with the next entry's id.
    chunks = response.text.split('class="flip-entry"')[1:]
    entries = []
    for chunk in chunks:
        match = ENTRY_RE.search('id="entry-' + chunk.split('id="entry-', 1)[-1])
        if match:
            entries.append({"drive_id": match.group(1), "name": match.group(2).strip()})
    return entries


def download(entries: list[dict], staging: Path) -> tuple[int, list[str]]:
    """Download each entry, skipping files already present. Returns (ok_count, failures)."""
    failures = []
    ok = 0
    for i, entry in enumerate(entries, 1):
        dest = staging / entry["name"]
        if dest.exists() and dest.stat().st_size > 0:
            ok += 1
            print(f"[{i}/{len(entries)}] skip {entry['name']} ({dest.stat().st_size / 1e6:.1f} MB)")
            continue

        url = DOWNLOAD_URL.format(file_id=entry["drive_id"])
        try:
            with httpx.stream(
                "GET", url, headers={"User-Agent": USER_AGENT}, follow_redirects=True, timeout=120
            ) as response:
                response.raise_for_status()
                content_type = response.headers.get("content-type", "")
                if "text/html" in content_type:
                    failures.append(f"{entry['name']}: got HTML (sign-in or scan interstitial)")
                    print(f"[{i}/{len(entries)}] FAIL {entry['name']} — HTML response")
                    continue
                with dest.open("wb") as fh:
                    for block in response.iter_bytes(chunk_size=1 << 16):
                        fh.write(block)
        except httpx.HTTPError as exc:
            dest.unlink(missing_ok=True)
            failures.append(f"{entry['name']}: {exc}")
            print(f"[{i}/{len(entries)}] FAIL {entry['name']} — {exc}")
            continue

        ok += 1
        print(f"[{i}/{len(entries)}] ok   {entry['name']} ({dest.stat().st_size / 1e6:.1f} MB)")

    return ok, failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder")
    parser.add_argument("staging_dir")
    parser.add_argument("--manifest", default=None)
    parser.add_argument("--enumerate-only", action="store_true")
    args = parser.parse_args()

    folder_id = parse_folder_id(args.folder)
    staging = Path(args.staging_dir).expanduser()
    staging.mkdir(parents=True, exist_ok=True)
    manifest_path = Path(args.manifest).expanduser() if args.manifest else staging / "manifest.json"

    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        entries = manifest["files"]
        print(f"Reusing manifest: {len(entries)} entries from {manifest_path}")
    else:
        entries = enumerate_folder(folder_id)
        if not entries:
            print("Enumeration found 0 entries — folder may be private or the page shape changed.")
            return 1
        manifest = {
            "source_folder": folder_id,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "count": len(entries),
            "files": entries,
        }
        manifest_path.write_text(json.dumps(manifest, indent=2))
        print(f"Enumerated {len(entries)} entries → {manifest_path}")

    if args.enumerate_only:
        return 0

    ok, failures = download(entries, staging)
    print(f"\n{ok}/{len(entries)} present in {staging}")
    if failures:
        print(f"{len(failures)} failed:", file=sys.stderr)
        for line in failures:
            print(f"  {line}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
