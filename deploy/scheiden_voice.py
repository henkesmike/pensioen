#!/usr/bin/env python3
"""Process the fixed Scheiden voice-over job with the VPS's local credentials."""
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE = Path("/var/lib/pensioen-deploy")
PREVIEW = BASE / "previews/scheiden-adam"
CACHE = BASE / "private/scheiden-adam"
PUBLIC = Path("/var/www/pensioen/scheiden-adam.html")
REQUEST = "https://raw.githubusercontent.com/henkesmike/pensioen/voiceover-scheiden/deploy/scheiden-request.json"
VOICE = "pNInz6obpgDQGcFmaJgB"
MODEL = "eleven_multilingual_v2"
SPEED = 0.85


def fetch(request, limit):
    with urlopen(request, timeout=45) as response:
        data = response.read(limit + 1)
    if len(data) > limit:
        raise ValueError("Response exceeds its size limit")
    return data


def write(path, data, mode):
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as output:
        temporary = Path(output.name)
        try:
            output.write(data)
            output.flush()
            temporary.chmod(mode)
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)


def build(source):
    captions = re.search(r"const captions = \[\n(.*?)\n\];", source, re.S)[1]
    cues = re.findall(r"^\s*\[([\d.]+|payoutStart),\s*[\d.]+, '([^']+)'\],$", captions, re.M)
    if len(cues) != 7:
        raise ValueError("Expected seven approved Scheiden cues")
    payout = float(re.search(r"const payoutStart = ([\d.]+);", source)[1])
    text = " ".join(line for _, line in cues)
    parameters = {"text": text, "model_id": MODEL, "voice_settings": {"speed": SPEED}}
    body = json.dumps(parameters, ensure_ascii=False).encode()
    fingerprint = hashlib.sha256(VOICE.encode() + body).hexdigest()
    recording = CACHE / (fingerprint + ".json")
    pending = CACHE / (fingerprint + ".pending")
    if not recording.exists():
        if pending.exists():
            raise ValueError("Previous voice request had an uncertain result; inspect before retrying")
        key = os.environ["ELEVENLABS_API_KEY"]
        request = Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_64",
            data=body, headers={"xi-api-key": key, "Content-Type": "application/json"},
        )
        pending.touch(mode=0o600, exist_ok=False)
        result = fetch(request, 4 * 1024 * 1024)
        json.loads(result)
        write(recording, result, 0o600)
        pending.unlink(missing_ok=True)
    response = json.loads(recording.read_text())
    alignment = response["alignment"]
    if "".join(alignment["characters"]) != text:
        raise ValueError("Alignment text does not match the approved script")
    starts = alignment["character_start_times_seconds"]
    ends = alignment["character_end_times_seconds"]
    audio = base64.b64decode(response["audio_base64"], validate=True)
    if not audio or len(starts) != len(text) or len(ends) != len(text):
        raise ValueError("Recording or timestamps are incomplete")
    points = [[0, 0]]
    position = 0
    for planned, line in cues:
        points.append([3.5 + starts[position], payout if planned == "payoutStart" else float(planned)])
        position += len(line) + 1
    points += [[3.5 + ends[-1], 59], [8.5 + ends[-1], 64]]
    if not all(a[0] < b[0] for a, b in zip(points, points[1:])):
        raise ValueError("Audio cue times must increase")
    padded = subprocess.run(
        ["ffmpeg", "-v", "error", "-f", "mp3", "-i", "pipe:0", "-af",
         "adelay=3500:all=1,apad=pad_dur=5", "-b:a", "64k", "-f", "mp3", "pipe:1"],
        input=audio, stdout=subprocess.PIPE, check=True,
    ).stdout
    audio_tag = '<audio id="recording" controls preload="metadata" src="data:audio/mpeg;base64,' + base64.b64encode(padded).decode() + '"></audio>'
    source, changed = re.subn(r'<div class="controls">.*?</div>', lambda _: audio_tag, source, count=1, flags=re.S)
    if changed != 1:
        raise ValueError("Expected the original controls")
    source = source.replace("<title>Scheiden · Pensioen Ontdekt</title>", "<title>Scheiden · Pensioen Ontdekt · Audio: ElevenLabs</title>")
    start = source.index("const duration =")
    end = source.index("function render()", start)
    source = source[:start] + "let time = 0;\n" + source[end:]
    source = source.replace("    element('progress').value = time;\n", "")
    start = source.index("    if (cue === lastCue)")
    end = source.index("</script>", start)
    script = """}
const recording = element('recording');
const anchors = POINTS;
let frame;
function drawFromAudio() {
    const seconds = recording.currentTime;
    const index = anchors.findIndex(([start]) => start > seconds);
    if (index > 0) {
        const [from, first] = anchors[index - 1];
        const [to, last] = anchors[index];
        time = first + (last - first) * phase(seconds, from, to);
    } else {
        time = 64;
    }
    render();
}
function tick() {
    drawFromAudio();
    if (!recording.paused && !recording.ended) frame = requestAnimationFrame(tick);
}
recording.addEventListener('play', () => {
    cancelAnimationFrame(frame);
    tick();
});
recording.addEventListener('pause', () => cancelAnimationFrame(frame));
recording.addEventListener('seeked', drawFromAudio);
recording.addEventListener('ended', () => { time = 64; render(); });
render();
""".replace("POINTS", json.dumps(points))
    return (source[:start] + script + source[end:]).encode()


def main():
    try:
        job = json.loads(fetch(REQUEST, 2048))
    except HTTPError as error:
        if error.code == 404:
            return
        raise
    if job == {"action": "build", "film": "scheiden-v9"}:
        candidate = PREVIEW / "index.html"
        if not candidate.exists():
            source = Path(__file__).with_name("scheiden-v9.html").read_text()
            write(candidate, build(source), 0o640)
        digest = hashlib.sha256(candidate.read_bytes()).hexdigest()
        write(PREVIEW / "status.json", json.dumps({"state": "preview-ready", "sha256": digest}).encode(), 0o640)
    elif isinstance(job, dict) and set(job) == {"action", "film", "sha256"} and job["action"] == "publish" and job["film"] == "scheiden-v9":
        data = (PREVIEW / "index.html").read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if job["sha256"] != digest:
            raise ValueError("Candidate does not match the approved checksum")
        if not PUBLIC.exists() or PUBLIC.read_bytes() != data:
            write(PUBLIC, data, 0o644)
        write(PREVIEW / "status.json", json.dumps({"state": "published", "sha256": digest}).encode(), 0o640)
    else:
        raise ValueError("Unknown voice-over request")


if __name__ == "__main__":
    main()
