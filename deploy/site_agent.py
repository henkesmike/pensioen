"""Build, privately preview, and publish approved Pensioen releases."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.error import HTTPError
from urllib.request import urlopen

from publish import publish as publish_homepage

ORIGIN = "https://raw.githubusercontent.com/henkesmike/pensioen"
PREVIEW_REQUEST = f"{ORIGIN}/uitrol-preview/deploy/preview.json"
RELEASE_REQUEST = f"{ORIGIN}/uitrol-productie/deploy/site-release.json"
BASE = Path("/var/lib/pensioen-deploy")
SOURCE = BASE / "source" / "repo"
PRIVATE = BASE / "private"
REFERENCE = PRIVATE / "partnerpensioen-v3.html"
CACHE = PRIVATE / "fase3"
PREVIEWS = BASE / "previews"
CANDIDATES = BASE / "candidates"
STATE = BASE / "state"
SITE = Path("/var/www/pensioen")
STATUS = SITE / "deployment-status.json"
HTML_LIMIT = 8 * 1024 * 1024
SOURCE_FILES = (
    "poc/v4/build.py",
    "poc/v4/config.py",
    "poc/v4/engine.js",
    "poc/v4/data/regelingen.json",
    "poc/v4/data/personages.json",
    "poc/v4/data/animaties.json",
    "poc/v3/scenario.json",
    "poc/v3/template.html",
    "poc/v3/assets/scene.svg",
)
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
REQUEST_ID_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]{0,63}$")
ALLOWED_TARGETS = {"partnerpensioen-demo.html"}


def fetch(url, limit):
    with urlopen(url, timeout=20) as response:
        if response.geturl() != url:
            raise ValueError("Unexpected redirect while fetching a deployment input.")
        data = response.read(limit + 1)
    if len(data) > limit:
        raise ValueError("Deployment input exceeds its size limit.")
    return data


def fetch_request(url, expected_keys):
    try:
        data = json.loads(fetch(url, 4096))
    except HTTPError as error:
        if error.code == 404:
            return None
        raise
    if not isinstance(data, dict) or set(data) != expected_keys:
        raise ValueError(f"Expected request fields: {', '.join(sorted(expected_keys))}.")
    return data


def atomic_json(path, value, mode=0o644):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".status-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(name, mode)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def report(state, commit=None, sha256=None, request_id=None):
    value = {"state": state}
    if commit:
        value["commit"] = commit
    if sha256:
        value["sha256"] = sha256
    if request_id:
        value["request_id"] = request_id
    if state == "preview-ready":
        value["preview_url"] = (
            f"/_preview/{commit}/partnerpensioen-demo.html"
        )
    atomic_json(STATUS, value)


def validate_commit(value):
    if not isinstance(value, str) or not COMMIT_RE.fullmatch(value):
        raise ValueError("Invalid source commit.")
    return value


def source_for(commit):
    marker = SOURCE / ".source-commit"
    if marker.is_file() and marker.read_text().strip() == commit:
        return
    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".source-", dir=SOURCE.parent))
    try:
        total = 0
        for relative in SOURCE_FILES:
            data = fetch(f"{ORIGIN}/{commit}/{relative}", 2 * 1024 * 1024)
            total += len(data)
            if total > 8 * 1024 * 1024:
                raise ValueError("Source tree exceeds its size limit.")
            target = stage / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            target.chmod(0o640)
        build = stage / "poc/v4/build.py"
        if b'parser.add_argument("--offline"' not in build.read_bytes():
            raise ValueError("The selected source commit does not support offline builds.")
        (stage / ".source-commit").write_text(commit + "\n", encoding="ascii")
        if SOURCE.exists():
            shutil.rmtree(SOURCE)
        os.replace(stage, SOURCE)
    finally:
        if stage.exists():
            shutil.rmtree(stage)


def candidate_path(commit):
    return PREVIEWS / commit / "partnerpensioen-demo.html"


def load_candidate(commit):
    meta_path = CANDIDATES / f"{commit}.json"
    if not meta_path.is_file():
        raise ValueError("The requested candidate has not been built.")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    if meta.get("commit") != commit:
        raise ValueError("Candidate metadata does not match the request.")
    path = candidate_path(commit)
    if not path.is_file() or path.is_symlink():
        raise ValueError("Candidate file is missing or invalid.")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != meta.get("sha256"):
        raise ValueError("Candidate checksum mismatch.")
    return path, meta


def build_preview():
    request = fetch_request(PREVIEW_REQUEST, {"commit", "request_id"})
    if request is None:
        return
    commit = validate_commit(request["commit"])
    request_id = request["request_id"]
    if not isinstance(request_id, str) or not REQUEST_ID_RE.fullmatch(request_id):
        raise ValueError("Invalid preview request_id.")
    previous_state = STATE / "preview-request.json"
    if previous_state.is_file():
        previous = json.loads(previous_state.read_text(encoding="utf-8"))
        if previous.get("commit") == commit and previous.get("request_id") == request_id:
            try:
                _, meta = load_candidate(commit)
                report("preview-ready", commit, meta["sha256"], request_id)
                return
            except ValueError:
                if previous.get("state") == "failed":
                    return
    report("building", commit, request_id=request_id)
    try:
        source_for(commit)
        if not REFERENCE.is_file() or not CACHE.is_dir():
            raise ValueError("The private reference or audio cache is not installed.")
        PREVIEWS.mkdir(parents=True, exist_ok=True)
        temp_dir = Path(tempfile.mkdtemp(prefix=".candidate-", dir=PREVIEWS))
        try:
            output = temp_dir / "partnerpensioen-demo.html"
            command = [
                sys.executable, str(SOURCE / "poc/v4/build.py"),
                str(REFERENCE), str(output), "--cache", str(CACHE), "--offline",
            ]
            env = {"PATH": "/usr/bin:/bin", "HOME": str(BASE), "LANG": "C.UTF-8"}
            subprocess.run(command, check=True, timeout=840, env=env)
            if not output.is_file() or output.stat().st_size > HTML_LIMIT:
                raise ValueError("The generated preview is missing or too large.")
            digest = hashlib.sha256(output.read_bytes()).hexdigest()
            output.chmod(0o640)
            temp_dir.chmod(0o2750)
            final_dir = PREVIEWS / commit
            if final_dir.exists():
                shutil.rmtree(final_dir)
            os.replace(temp_dir, final_dir)
            CANDIDATES.mkdir(parents=True, exist_ok=True)
            atomic_json(CANDIDATES / f"{commit}.json",
                        {"commit": commit, "sha256": digest}, mode=0o640)
            atomic_json(previous_state,
                        {"commit": commit, "request_id": request_id, "state": "ready"},
                        mode=0o640)
            report("preview-ready", commit, digest, request_id)
            print(f"Preview ready: {commit} {digest}")
        finally:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
    except Exception as error:
        atomic_json(previous_state,
                    {"commit": commit, "request_id": request_id, "state": "failed"},
                    mode=0o640)
        report("build-failed", commit, request_id=request_id)
        print(f"Preview build failed for {commit}: {type(error).__name__}: {error}")
        raise


def publish_candidate():
    request = fetch_request(RELEASE_REQUEST, {"candidate_commit", "sha256", "target"})
    if request is None:
        return
    commit = validate_commit(request["candidate_commit"])
    expected = request["sha256"]
    target_name = request["target"]
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
        raise ValueError("Invalid candidate checksum.")
    if target_name not in ALLOWED_TARGETS:
        raise ValueError("The requested publication target is not allowed.")
    candidate, meta = load_candidate(commit)
    if meta["sha256"] != expected:
        raise ValueError("Approved checksum does not match the built candidate.")
    active = SITE / target_name
    data = candidate.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError("Candidate changed after approval.")
    if active.is_file() and hashlib.sha256(active.read_bytes()).hexdigest() == expected:
        report("published", commit, expected)
        return
    backup = BASE / "backups" / f"{target_name}.{commit}.previous"
    backup.parent.mkdir(parents=True, exist_ok=True)
    if active.is_file() and not backup.exists():
        shutil.copy2(active, backup)
    fd, name = tempfile.mkstemp(prefix=".release-", dir=SITE)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(name, 0o644)
        os.replace(name, active)
    finally:
        if os.path.exists(name):
            os.unlink(name)
    report("published", commit, expected)
    print(f"Published {target_name}: {commit} ({expected})")


def main():
    # Preserve the already installed, independent homepage release route.
    publish_homepage()
    try:
        build_preview()
    except Exception:
        # The timer remains available for a retry with a new request_id.
        pass
    publish_candidate()


if __name__ == "__main__":
    main()
