#!/usr/bin/env python3
"""Public, tightly bounded endpoint for requesting a partner-pension scheme."""
import fcntl
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
from uuid import uuid4


BASE = Path(os.environ.get("PENSIOEN_BASE", "/var/lib/pensioen-deploy"))
SOURCE = BASE / "source" / "repo"
PRIVATE = BASE / "private"
REFERENCE = PRIVATE / "partnerpensioen-v3.html"
CACHE = PRIVATE / "fase3"
SUPPLEMENT = PRIVATE / "aanvullende-regelingen.json"
ADMIN = BASE / "admin"
JOBS = ADMIN / "jobs"
USAGE = ADMIN / "tts-usage.json"
RATE = ADMIN / "request-limits.json"
BUILD_LOCK = ADMIN / "candidate-build.lock"
ACTIVE_CANDIDATE = ADMIN / "active-candidate.json"
PREVIEWS = BASE / "previews"
CANDIDATES = BASE / "candidates"
SITE_HOST = "pensioen.myaiprojects.nl"
LISTEN_PORT = int(os.environ.get("PENSIOEN_ADMIN_PORT", "8765"))
DAILY_SCHEME_LIMIT = int(os.environ.get("PENSIOEN_SCHEME_DAILY_LIMIT", "2"))
DAILY_TTS_LIMIT = int(os.environ.get("PENSIOEN_TTS_DAILY_LIMIT", "4"))
IP_HOURLY_LIMIT = int(os.environ.get("PENSIOEN_IP_HOURLY_LIMIT", "2"))
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
JOB_RE = re.compile(r"^[0-9a-f]{32}$")
MAX_BODY = 1024
MAX_HTML = 8 * 1024 * 1024
BUILD_TIMEOUT = 300
ARTIFACT_RETENTION_DAYS = 30
_BUILD_MUTEX = threading.Lock()


class PublicError(Exception):
    def __init__(self, status, message):
        self.status = status
        self.message = message


def atomic_json(path, value, mode=0o600):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".admin-", dir=path.parent)
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


def load_json(path, fallback):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return fallback


def read_regulations():
    base_path = SOURCE / "poc/v4/data/regelingen.json"
    base = json.loads(base_path.read_text(encoding="utf-8"))
    additions = load_json(SUPPLEMENT, {"schema_version": 1, "regelingen": []})
    if (not isinstance(base, dict) or base.get("schema_version") != 1
            or not isinstance(base.get("regelingen"), list)
            or not isinstance(additions, dict) or additions.get("schema_version") != 1
            or not isinstance(additions.get("regelingen"), list)):
        raise RuntimeError("De serverconfiguratie voor regelingen is ongeldig.")
    return base["regelingen"] + additions["regelingen"], additions


def code_for_index(index):
    """Spreadsheet-style A..Z, AA.. codes, starting at zero."""
    chars = []
    number = index + 1
    while number:
        number, rem = divmod(number - 1, 26)
        chars.append(chr(ord("A") + rem))
    return "".join(reversed(chars))


def next_code(used):
    index = 0
    while True:
        code = code_for_index(index)
        if code not in used:
            return code
        index += 1


def validate_parameters(value):
    if not isinstance(value, dict) or set(value) != {"percentage", "months"}:
        raise PublicError(400, "Vul alleen percentage en aantal maanden in.")
    percentage, months = value["percentage"], value["months"]
    if type(percentage) is not int or not 1 <= percentage <= 100:
        raise PublicError(400, "Het dekkingspercentage moet een heel getal van 1 tot en met 100 zijn.")
    if type(months) is not int or not 1 <= months <= 120:
        raise PublicError(400, "De voorlopige dekking moet 1 tot en met 120 maanden duren.")
    return percentage, months


def utc_day():
    return datetime.now(timezone.utc).date().isoformat()


def reserve_submission(client_ip):
    """Persist global and per-IP limits; fail closed if the state is damaged."""
    ADMIN.mkdir(parents=True, exist_ok=True)
    lock_path = RATE.with_suffix(".lock")
    with lock_path.open("a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        now = int(time.time())
        day = utc_day()
        state = load_json(RATE, {"date": day, "submissions": 0, "by_ip": {}})
        if state.get("date") != day:
            state = {"date": day, "submissions": 0, "by_ip": {}}
        submissions = state.get("submissions")
        by_ip = state.get("by_ip")
        if type(submissions) is not int or submissions < 0 or not isinstance(by_ip, dict):
            raise RuntimeError("De aanvraaglimiet kan niet veilig worden gecontroleerd.")
        recent = [stamp for stamp in by_ip.get(client_ip, [])
                  if type(stamp) is int and now - stamp < 3600]
        if len(recent) >= IP_HOURLY_LIMIT:
            raise PublicError(429, "Probeer het later opnieuw; dit adres heeft de uurgrens bereikt.")
        if submissions >= DAILY_SCHEME_LIMIT:
            raise PublicError(429, "De daggrens voor nieuwe regelingen is bereikt.")
        recent.append(now)
        state["submissions"] = submissions + 1
        state["by_ip"][client_ip] = recent
        atomic_json(RATE, state)


def update_job(job_id, **changes):
    path = JOBS / f"{job_id}.json"
    job = load_json(path, {"id": job_id})
    job.update(changes)
    job["updated_at"] = datetime.now(timezone.utc).isoformat()
    atomic_json(path, job)
    return job


def cleanup_expired_artifacts():
    """Remove old public candidates and job records without touching GitHub previews."""
    cutoff = time.time() - ARTIFACT_RETENTION_DAYS * 24 * 60 * 60
    active = load_json(ACTIVE_CANDIDATE, {}).get("commit")
    for metadata_path in CANDIDATES.glob("*.json"):
        try:
            metadata = load_json(metadata_path, {})
            candidate_id = metadata.get("commit")
            if (not metadata.get("request_id") or not isinstance(candidate_id, str)
                    or not COMMIT_RE.fullmatch(candidate_id) or candidate_id == active
                    or metadata_path.stat().st_mtime >= cutoff):
                continue
            candidate_dir = PREVIEWS / candidate_id
            if candidate_dir.is_dir() and not candidate_dir.is_symlink():
                shutil.rmtree(candidate_dir)
            metadata_path.unlink(missing_ok=True)
        except (OSError, AttributeError, TypeError):
            continue
    for job_path in JOBS.glob("*.json"):
        try:
            if job_path.stat().st_mtime < cutoff:
                job_path.unlink(missing_ok=True)
        except OSError:
            continue


def source_commit():
    marker = SOURCE / ".source-commit"
    if not marker.is_file():
        raise PublicError(503, "De voice-overbouwer is nog niet klaar. Probeer het later opnieuw.")
    commit = marker.read_text(encoding="ascii").strip()
    if not COMMIT_RE.fullmatch(commit):
        raise RuntimeError("De bronversie van de voice-overbouwer is ongeldig.")
    return commit


def file_lock(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    handle = Path(path).open("a+")
    fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
    return handle


def create_candidate(job_id, rule, all_additions):
    source_version = source_commit()
    if not REFERENCE.is_file() or not CACHE.is_dir():
        raise RuntimeError("De privébron of audiocache ontbreekt op de server.")
    JOBS.mkdir(parents=True, exist_ok=True)
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    CANDIDATES.mkdir(parents=True, exist_ok=True)
    temp_dir = Path(tempfile.mkdtemp(prefix=f".request-{job_id}-", dir=JOBS))
    additions_path = temp_dir / "aanvullende-regelingen.json"
    output_path = temp_dir / "partnerpensioen-demo.html"
    atomic_json(additions_path, {"schema_version": 1, "regelingen": all_additions})
    try:
        build_path = SOURCE / "poc/v4/build.py"
        command = [
            sys.executable, str(build_path), str(REFERENCE), str(output_path),
            "--cache", str(CACHE), "--additional-regulations", str(additions_path),
            "--tts-usage-file", str(USAGE), "--tts-daily-limit", str(DAILY_TTS_LIMIT),
        ]
        environment = {
            "PATH": "/usr/bin:/bin", "HOME": str(BASE), "LANG": "C.UTF-8",
            "ELEVENLABS_API_KEY": os.environ.get("ELEVENLABS_API_KEY", ""),
        }
        if not environment["ELEVENLABS_API_KEY"]:
            raise RuntimeError("De server heeft geen ElevenLabs-sleutel voor deze beheerfunctie.")
        with file_lock(BUILD_LOCK):
            subprocess.run(command, check=True, timeout=BUILD_TIMEOUT, env=environment,
                           stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            if not output_path.is_file() or output_path.stat().st_size > MAX_HTML:
                raise RuntimeError("De gegenereerde preview ontbreekt of is te groot.")
            digest = hashlib.sha256(output_path.read_bytes()).hexdigest()
            candidate_id = hashlib.sha1(f"{job_id}:{digest}".encode()).hexdigest()
            final_dir = PREVIEWS / candidate_id
            staging_dir = PREVIEWS / f".{candidate_id}.{job_id}"
            if staging_dir.exists():
                shutil.rmtree(staging_dir)
            staging_dir.mkdir(mode=0o2750)
            candidate_html = staging_dir / "partnerpensioen-demo.html"
            shutil.copyfile(output_path, candidate_html)
            candidate_html.chmod(0o640)
            staging_dir.chmod(0o2750)

            os.replace(staging_dir, final_dir)
            metadata = {"commit": candidate_id, "sha256": digest, "source_commit": source_version,
                        "request_id": job_id}
            atomic_json(CANDIDATES / f"{candidate_id}.json", metadata)
            # Save the scheme only after the complete, uniquely addressable candidate exists.
            atomic_json(SUPPLEMENT, {"schema_version": 1, "regelingen": all_additions})
            atomic_json(ACTIVE_CANDIDATE, {"commit": candidate_id, "job_id": job_id})
        update_job(job_id, state="preview-ready", code=rule["code"], commit=candidate_id,
                   sha256=digest, preview_url=f"/_candidate/{candidate_id}/partnerpensioen-demo.html")
    except Exception as error:
        # Expose a stable, non-secret error message; keep stack traces and API responses private.
        if isinstance(error, subprocess.CalledProcessError):
            detail = error.stderr.decode("utf-8", "replace") if error.stderr else ""
            message = ("De voice-over kon niet worden gemaakt. De regeling is niet opgeslagen. "
                       + ("De dagelijkse API-limiet is bereikt." if "Daglimiet" in detail else
                          "Controleer de voice-overdienst of probeer het later opnieuw."))
        elif isinstance(error, PublicError):
            message = error.message
        else:
            message = "De voice-over kon niet worden gemaakt. De regeling is niet opgeslagen."
        update_job(job_id, state="failed", code=rule["code"], error=message)
        raise
    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)


def client_address(handler):
    forwarded = handler.headers.get("X-Real-IP", "")
    try:
        return str(ipaddress.ip_address(forwarded))
    except ValueError:
        return str(ipaddress.ip_address(handler.client_address[0]))


class Handler(BaseHTTPRequestHandler):
    server_version = "PensioenRegelingen/1"

    def log_message(self, *_):
        # Public requests can contain operational details; keep them out of stdout/journal.
        return

    def send_json(self, status, value):
        data = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

    def same_site(self):
        origin = self.headers.get("Origin")
        return origin is None or origin == f"https://{SITE_HOST}"

    def do_GET(self):
        path = urlsplit(self.path).path
        match = re.fullmatch(r"/api/regelingen/jobs/([0-9a-f]{32})", path)
        if not match:
            self.send_json(404, {"error": "Niet gevonden."})
            return
        job = load_json(JOBS / f"{match[1]}.json", None)
        if job is None:
            self.send_json(404, {"error": "Aanvraag niet gevonden."})
            return
        response = {key: job[key] for key in ("id", "state", "code", "error", "updated_at") if key in job}
        if job.get("state") == "preview-ready":
            response.update({key: job[key] for key in ("commit", "sha256", "preview_url")})
        self.send_json(200, response)

    def do_POST(self):
        if urlsplit(self.path).path != "/api/regelingen":
            self.send_json(404, {"error": "Niet gevonden."})
            return
        if not self.same_site():
            self.send_json(403, {"error": "Aanvraag geweigerd."})
            return
        if self.headers.get_content_type() != "application/json":
            self.send_json(415, {"error": "Gebruik JSON."})
            return
        acquired = False
        try:
            length = int(self.headers.get("Content-Length", "-1"))
        except ValueError:
            length = -1
        if not 0 < length <= MAX_BODY:
            self.send_json(413, {"error": "Aanvraag is leeg of te groot."})
            return
        try:
            payload = json.loads(self.rfile.read(length))
            percentage, months = validate_parameters(payload)
            client_ip = client_address(self)
            regulations, additions = read_regulations()
            for existing in regulations:
                values = existing["partnerpensioen"]
                if (values["percentage_pensioengevend_salaris"] == percentage
                        and values["uitloop_maanden"] == months):
                    self.send_json(409, {"error": "Deze combinatie bestaat al; er is geen nieuwe voice-over nodig."})
                    return
            if not _BUILD_MUTEX.acquire(blocking=False):
                self.send_json(409, {"error": "Er wordt al een regeling met voice-over verwerkt. Probeer het later opnieuw."})
                return
            code = next_code({item["code"] for item in regulations})
            rule = {
                "id": f"regeling-{code.lower()}",
                "code": code,
                "naam": f"Fictieve regeling {code}",
                "partnerpensioen": {
                    "percentage_pensioengevend_salaris": percentage,
                    "uitloop_maanden": months,
                },
            }
            job_id = uuid4().hex
            additions["regelingen"].append(rule)
            JOBS.mkdir(parents=True, exist_ok=True)
            update_job(job_id, state="building", code=code)
            acquired = True
            reserve_submission(client_ip)
            self.send_json(202, {"id": job_id, "state": "building", "code": code})
            thread = threading.Thread(
                target=self._run_build, args=(job_id, rule, additions["regelingen"]), daemon=True
            )
            thread.start()
            acquired = False
        except PublicError as error:
            if acquired:
                _BUILD_MUTEX.release()
            self.send_json(error.status, {"error": error.message})
        except (json.JSONDecodeError, UnicodeDecodeError):
            if acquired:
                _BUILD_MUTEX.release()
            self.send_json(400, {"error": "Ongeldige JSON."})
        except (OSError, RuntimeError, KeyError, TypeError, ValueError):
            if acquired:
                _BUILD_MUTEX.release()
            self.send_json(503, {"error": "De aanvraag kan nu niet worden verwerkt."})

    @staticmethod
    def _run_build(job_id, rule, additions):
        try:
            create_candidate(job_id, rule, additions)
        except Exception:
            # create_candidate records a user-safe failure; no secret data is logged.
            pass
        finally:
            _BUILD_MUTEX.release()


def main():
    for path in (ADMIN, PRIVATE, CACHE, PREVIEWS, CANDIDATES):
        path.mkdir(parents=True, exist_ok=True)
    cleanup_expired_artifacts()
    server = ThreadingHTTPServer(("127.0.0.1", LISTEN_PORT), Handler)
    server.daemon_threads = True
    server.serve_forever()


if __name__ == "__main__":
    main()
