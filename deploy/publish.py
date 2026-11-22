"""Publish one approved static homepage from the designated release branch."""
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.error import HTTPError
from urllib.request import urlopen

ORIGIN = "https://raw.githubusercontent.com/henkesmike/pensioen"
REQUEST = f"{ORIGIN}/uitrol-productie/deploy/productie.json"
PUBLIC = Path("/var/lib/pensioen-deploy/public")
MAX_HTML = 256 * 1024


def fetch(url, limit):
    with urlopen(url, timeout=15) as response:
        if response.geturl() != url:
            raise ValueError("Onverwachte doorverwijzing bij het ophalen.")
        data = response.read(limit + 1)
    if len(data) > limit:
        raise ValueError("Bestand overschrijdt de toegestane grootte.")
    return data


def publish(public=PUBLIC):
    try:
        request = json.loads(fetch(REQUEST, 4096))
    except HTTPError as error:
        if error.code == 404:
            return  # No publication has been requested yet.
        raise
    if not isinstance(request, dict) or request.keys() != {"commit", "sha256"}:
        raise ValueError("Verwacht alleen commit en sha256.")
    commit, expected = request["commit"], request["sha256"]
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Ongeldige commit.")
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
        raise ValueError("Ongeldige checksum.")
    active = public / "index.html"
    current = active.read_bytes()
    if hashlib.sha256(current).hexdigest() == expected:
        return
    candidate = fetch(f"{ORIGIN}/{commit}/index.html", MAX_HTML)
    if hashlib.sha256(candidate).hexdigest() != expected:
        raise ValueError("Checksum wijkt af. De actieve homepage blijft beschikbaar.")
    if not candidate.lstrip().lower().startswith(b"<!doctype html>"):
        raise ValueError("Verwacht een HTML-homepage.")
    with tempfile.TemporaryDirectory(dir=public) as folder:
        staged = Path(folder) / "index.html"
        staged.write_bytes(candidate)
        staged.chmod(0o644)
        previous = Path(folder) / "previous.html"
        previous.write_bytes(current)
        previous.chmod(0o644)
        os.replace(previous, public / "previous.html")
        os.replace(staged, active)
    print(f"Homepage gepubliceerd: {commit} ({expected})")


if __name__ == "__main__":
    publish()
