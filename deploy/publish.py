"""Publish checksum-verified static files from a designated GitHub commit."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import tempfile
from datetime import datetime, timezone
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import urlopen
from uuid import uuid4

ORIGIN = "https://raw.githubusercontent.com/henkesmike/pensioen"
REQUEST = f"{ORIGIN}/uitrol-productie/deploy/productie.json"
BASE = Path("/var/lib/pensioen-deploy")
PUBLIC = BASE / "public"
WEBROOT = Path("/var/www/pensioen")
ACTIVE = PUBLIC / "index.html"
HISTORY = BASE / "history"
MAX_REQUEST = 16 * 1024
MAX_FILE = 10 * 1024 * 1024
MAX_TOTAL = 40 * 1024 * 1024
MAX_FILES = 20
ALLOWED_SUFFIXES = {
    ".html", ".css", ".js", ".json", ".svg", ".png", ".webp", ".jpg",
    ".jpeg", ".gif", ".mp3", ".ogg", ".wav", ".mp4", ".webm", ".woff2",
    ".ico", ".txt",
}
RESERVED_ROOTS = {
    ".github", "deploy", "docs", "node_modules", "poc", "test", "tests",
}


def fetch(url, limit):
    with urlopen(url, timeout=15) as response:
        if response.geturl() != url:
            raise ValueError("Onverwachte doorverwijzing bij het ophalen.")
        data = response.read(limit + 1)
    if len(data) > limit:
        raise ValueError("Bestand overschrijdt de toegestane grootte.")
    return data


def safe_path(value):
    if not isinstance(value, str) or not value or len(value) > 240:
        raise ValueError("Ongeldig bestandspad.")
    if "\\" in value or value.startswith("/") or value.endswith("/"):
        raise ValueError("Gebruik een relatief POSIX-bestandspad.")
    parts = value.split("/")
    if any(part in ("", ".", "..") or part.startswith(".") for part in parts):
        raise ValueError("Puntbestanden en onveilige paden zijn niet toegestaan.")
    if parts[0].lower() in RESERVED_ROOTS:
        raise ValueError("Dit pad is geen publiceerbare website-inhoud.")
    path = PurePosixPath(value)
    if path.suffix.lower() not in ALLOWED_SUFFIXES:
        raise ValueError("Dit bestandstype is niet toegestaan.")
    return path


def parse_request(raw):
    request = json.loads(raw)
    if not isinstance(request, dict):
        raise ValueError("Ongeldige deploymentopdracht.")
    if request.keys() == {"commit", "sha256"}:
        records = [{"path": "index.html", "sha256": request["sha256"]}]
    elif request.keys() == {"commit", "files"}:
        records = request["files"]
    else:
        raise ValueError("Verwacht commit en sha256, of commit en files.")
    commit = request.get("commit")
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Ongeldige volledige GitHub-commit.")
    if not isinstance(records, list) or not records or len(records) > MAX_FILES:
        raise ValueError("De opdracht moet 1 tot 20 bestanden bevatten.")
    seen = set()
    parsed = []
    total = 0
    for item in records:
        if not isinstance(item, dict) or item.keys() != {"path", "sha256"}:
            raise ValueError("Elk bestand bevat alleen path en sha256.")
        path = safe_path(item["path"])
        key = path.as_posix()
        if key in seen:
            raise ValueError("Een bestandspad staat meer dan één keer in de opdracht.")
        seen.add(key)
        expected = item["sha256"]
        if expected is not None and (
            not isinstance(expected, str)
            or not re.fullmatch(r"[0-9a-f]{64}", expected)
        ):
            raise ValueError("Ongeldige SHA-256; gebruik null om een bestand te verwijderen.")
        parsed.append((key, path, expected))
    for path in seen:
        for other in seen:
            if path != other and other.startswith(path + "/"):
                raise ValueError("Een bestandspad kan niet ook een map zijn.")
    return commit, parsed


def destination(path, create_parents, created_dirs):
    if path == "index.html":
        target = ACTIVE
        root = PUBLIC
        parts = []
    else:
        target = WEBROOT.joinpath(*PurePosixPath(path).parts)
        root = WEBROOT
        parts = list(PurePosixPath(path).parts[:-1])
    if root.is_symlink():
        raise ValueError("De publicatiemap mag geen symbolische koppeling zijn.")
    current = root
    for part in parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("Symbolische koppelingen in doelpaden zijn niet toegestaan.")
        if current.exists():
            if not current.is_dir():
                raise ValueError("Een bovenliggende doelmap is geen map.")
        elif create_parents:
            current.mkdir(mode=0o755)
            created_dirs.append(current)
    if target.is_symlink():
        raise ValueError("Een bestaand doelbestand mag geen symbolische koppeling zijn.")
    if target.exists() and not target.is_file():
        raise ValueError("Het doel is geen regulier bestand.")
    return target


def write_atomic(target, data):
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".pensioen-stage-", dir=target.parent)
    stage = Path(name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        stage.chmod(0o644)
        os.replace(stage, target)
    finally:
        stage.unlink(missing_ok=True)


def publish(public=PUBLIC, webroot=WEBROOT, request_url=REQUEST):
    global WEBROOT, ACTIVE, PUBLIC
    WEBROOT = webroot
    PUBLIC = public
    ACTIVE = PUBLIC / "index.html"
    try:
        raw_request = fetch(request_url, MAX_REQUEST)
    except HTTPError as error:
        if error.code == 404:
            return
        raise

    commit, records = parse_request(raw_request)
    staged = []
    created_dirs = []
    previous = {}
    operations = []
    try:
        for relative, path, expected in records:
            target = destination(relative, create_parents=expected is not None, created_dirs=created_dirs)
            old = target.read_bytes() if target.is_file() else None
            previous[relative] = old
            if expected is None:
                operations.append((relative, target, None, old))
                continue
            url = f"{ORIGIN}/{commit}/{quote(relative, safe='/')}"
            data = fetch(url, MAX_FILE)
            if hashlib.sha256(data).hexdigest() != expected:
                raise ValueError(f"Checksum wijkt af voor {relative}.")
            if path.suffix.lower() == ".html" and not data.lstrip().lower().startswith(b"<!doctype html>"):
                raise ValueError(f"Verwacht een HTML-document met doctype: {relative}.")
            if len(data) > MAX_TOTAL:
                raise ValueError("De deployment overschrijdt de totale bestandsgrootte.")
            staged.append((relative, target, data, old))
        if sum(len(data) for _, _, data, _ in staged) > MAX_TOTAL:
            raise ValueError("De deployment overschrijdt de totale bestandsgrootte.")

        changes = [
            operation for operation in operations
            if (operation[2] is None and operation[3] is not None)
            or (operation[2] is not None and hashlib.sha256(operation[2]).digest()
                != hashlib.sha256(operation[3]).digest() if operation[3] is not None
                else operation[2] is not None)
        ]
        if not changes:
            print(f"Bestanden staan al op de gevraagde versie: {commit}")
            return

        deployment_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8]
        history_dir = HISTORY / deployment_id
        history_dir.mkdir(parents=True, exist_ok=False)
        previous_manifest = {"commit": commit, "files": []}
        for relative, _, data, old in changes:
            previous_manifest["files"].append({
                "path": relative,
                "sha256": hashlib.sha256(data).hexdigest() if data is not None else None,
            })
            if old is not None:
                backup = history_dir / "previous" / PurePosixPath(relative)
                backup.parent.mkdir(parents=True, exist_ok=True)
                backup.write_bytes(old)
                backup.chmod(0o600)
        (history_dir / "previous.json").write_text(
            json.dumps(previous_manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        applied = []
        try:
            for relative, target, data, old in changes:
                if data is None:
                    target.unlink(missing_ok=True)
                else:
                    write_atomic(target, data)
                applied.append((target, old))
        except Exception:
            for target, old in reversed(applied):
                if old is None:
                    target.unlink(missing_ok=True)
                else:
                    write_atomic(target, old)
            raise

        current_manifest = {
            "commit": commit,
            "deployment_id": deployment_id,
            "files": [
                {"path": relative, "sha256": hashlib.sha256(data).hexdigest() if data is not None else None}
                for relative, _, data, _ in changes
            ],
        }
        (history_dir / "deployed.json").write_text(
            json.dumps(current_manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Deployment toegepast: {commit} ({len(changes)} bestanden, {deployment_id})")
    finally:
        for directory in sorted(created_dirs, key=lambda item: len(item.parts), reverse=True):
            try:
                directory.rmdir()
            except OSError:
                pass


if __name__ == "__main__":
    publish()
