#!/usr/bin/env python3
"""Verify, stage and select a complete static release on a Linux filesystem."""

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import quote
from urllib.request import urlopen


def records(bundle):
    manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
    if manifest["schema_version"] != 1:
        raise ValueError("Onbekende manifestversie.")
    files = {}
    for entry in manifest["files"]:
        name = entry["path"]
        if not re.fullmatch(r"[A-Za-z0-9_-][A-Za-z0-9_.-]*(/[A-Za-z0-9_-][A-Za-z0-9_.-]*)*", name):
            raise ValueError(f"Ongeldig pad: {name!r}")
        digest, size = entry["sha256"], entry["size"]
        if name in files or not re.fullmatch(r"[0-9a-f]{64}", digest) or type(size) is not int or size < 0:
            raise ValueError(f"Ongeldige manifestregel: {name}")
        files[name] = (size, digest)
    if "index.html" not in files:
        raise ValueError("index.html ontbreekt in het manifest.")
    return files


def verify_stream(stream, size, expected, name):
    digest = hashlib.sha256()
    remaining = size
    while remaining:
        chunk = stream.read(min(remaining, 1024 * 1024))
        if not chunk:
            break
        digest.update(chunk)
        remaining -= len(chunk)
    if remaining or stream.read(1) or digest.hexdigest() != expected:
        raise ValueError(f"Bestandsgrootte of SHA-256 wijkt af: {name}")


def verify(bundle):
    files = records(bundle)
    site = bundle / "site"
    if site.is_symlink():
        raise ValueError("site moet een gewone map zijn.")
    present = set()
    for entry in site.rglob("*"):
        if entry.is_symlink() or not (entry.is_file() or entry.is_dir()):
            raise ValueError(f"Onverwacht bestandstype: {entry}")
        if entry.is_file():
            present.add(entry.relative_to(site).as_posix())
    if present != files.keys():
        raise ValueError(f"Bestandslijst wijkt af: {sorted(present ^ files.keys())}")
    for name, (size, expected) in files.items():
        with (site / name).open("rb") as stream:
            verify_stream(stream, size, expected, name)


def select(root, release, bundle):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", release):
        raise ValueError("Ongeldige release-ID.")
    releases = root / "releases"
    releases.mkdir(parents=True, exist_ok=True)
    target = releases / release
    active = root / "current"
    with (root / ".release.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if bundle is not None:
            verify(bundle)
            if target.exists():
                if (target / "manifest.json").read_bytes() != (bundle / "manifest.json").read_bytes():
                    raise ValueError("Release-ID is al gekoppeld aan een ander manifest.")
            else:
                with tempfile.TemporaryDirectory(prefix=".staging-", dir=releases) as temporary:
                    staged = Path(temporary) / "bundle"
                    shutil.copytree(bundle, staged, symlinks=True)
                    verify(staged)
                    staged.rename(target)
        verify(target)
        previous = os.readlink(active) if active.is_symlink() else None
        with tempfile.TemporaryDirectory(prefix=".switch-", dir=root) as temporary:
            link = Path(temporary) / "current"
            link.symlink_to(Path("releases") / release / "site", target_is_directory=True)
            os.replace(link, active)
    return previous


def verify_http(bundle, base_url):
    for name, (size, expected) in records(bundle).items():
        path = "" if name == "index.html" else quote(name, safe="/")
        with urlopen(base_url.rstrip("/") + "/" + path, timeout=20) as response:
            verify_stream(response, size, expected, name)
        print(f"Gecontroleerd: {name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("verify")
    check.add_argument("bundle", type=Path)
    http = commands.add_parser("verify-http")
    http.add_argument("bundle", type=Path)
    http.add_argument("base_url")
    activate = commands.add_parser("activate")
    activate.add_argument("root", type=Path)
    activate.add_argument("release")
    activate.add_argument("--bundle", type=Path, help="Leg een nieuwe release klaar voor activering.")
    args = parser.parse_args()
    if args.command == "verify":
        verify(args.bundle)
    elif args.command == "verify-http":
        verify_http(args.bundle, args.base_url)
    else:
        previous = select(args.root, args.release, args.bundle)
        print(f"Actief: {args.release}. Vorige doelmap: {previous or 'geen'}.")


if __name__ == "__main__":
    main()
