#!/usr/bin/env python3
"""Prepare the four private phase 3 previews and their voice-over."""
import argparse
import base64
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from urllib.parse import quote
from urllib.request import Request, urlopen

from config import load_configuration

ROOT = Path(__file__).resolve().parent
V3 = ROOT.parent / "v3"
RATE = 24000
# Original v3 starts at 40% and 3 months. Cut between spoken sentences.
BLOCKS = [(0, 4), (4, 5), (5, 9), (9, 10), (10, 12)]
VOICE = "pNInz6obpgDQGcFmaJgB"
MODEL = "eleven_multilingual_v2"


def ffmpeg(data, *args):
    return subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", *args],
        input=data, stdout=subprocess.PIPE, check=True,
    ).stdout


def original_blocks(html, texts):
    match = re.search(r"const lines=(\[[^\n]*?\]), starts=(\[[^\n]*?\]), ends=(\[[^\n]*?\]), pct=", html)
    if not match:
        raise ValueError("Gebruik het oorspronkelijke privébestand partnerpensioen-v3.html.")
    lines, starts, ends = (json.loads(group) for group in match.groups())
    if texts != lines:
        raise ValueError("De tekst van regeling A moet bij de oorspronkelijke opname passen.")
    mp3 = re.search(r'data:audio/mpeg;base64,([A-Za-z0-9+/=]+)', html)[1]
    pcm = ffmpeg(base64.b64decode(mp3), "-i", "pipe:0", "-ar", str(RATE),
                 "-ac", "1", "-f", "s16le", "pipe:1")
    cuts = [0] + [round(RATE * (ends[i - 1] + starts[i]) / 2) for i, _ in BLOCKS[1:]]
    cuts.append(len(pcm) // 2)
    return {
        tuple(lines[first:last]): (
            pcm[2 * cuts[i]:2 * cuts[i + 1]],
            [[starts[j] - cuts[i] / RATE, ends[j] - cuts[i] / RATE] for j in range(first, last)],
        )
        for i, (first, last) in enumerate(BLOCKS)
    }


def reserve_daily_tts_call(usage_file, daily_limit):
    """Reserve one API call atomically; failed requests still use the quota."""
    if daily_limit < 1:
        raise ValueError("De dagelijkse ElevenLabs-limiet moet minimaal 1 zijn.")
    path = Path(usage_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = path.with_suffix(path.suffix + ".lock")
    with lock_path.open("a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        today = datetime.now(timezone.utc).date().isoformat()
        try:
            usage = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            usage = {"date": today, "calls": 0}
        if usage.get("date") != today:
            usage = {"date": today, "calls": 0}
        calls = usage.get("calls")
        if type(calls) is not int or calls < 0:
            raise ValueError("Ongeldige ElevenLabs-gebruiksadministratie.")
        if calls >= daily_limit:
            raise ValueError("Daglimiet voor nieuwe ElevenLabs-aanroepen bereikt.")
        usage["calls"] = calls + 1
        fd, temp_name = tempfile.mkstemp(prefix=".tts-usage-", dir=path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                json.dump(usage, stream)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.chmod(temp_name, 0o600)
            os.replace(temp_name, path)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)


def speech(lines, cache, endpoint, key, before_api_call=None, allow_api=True):
    text = " ".join(lines)
    fingerprint = hashlib.sha256(json.dumps([endpoint, VOICE, MODEL, text]).encode()).hexdigest()
    file = cache / (fingerprint + ".json")
    hit = file.exists()
    if hit:
        response = json.loads(file.read_text(encoding="utf-8"))
    else:
        if not allow_api:
            raise ValueError(f"Offline bouw gestopt: audio ontbreekt voor: {text}")
        if before_api_call is not None:
            before_api_call()
        url = f"{endpoint.rstrip('/')}/{quote(VOICE, safe='')}/with-timestamps?output_format=pcm_24000"
        request = Request(url, data=json.dumps({"text": text, "model_id": MODEL}).encode(),
                          headers={"xi-api-key": key, "Content-Type": "application/json"})
        with urlopen(request, timeout=60) as result:
            response = json.load(result)
    align = response["alignment"]
    pcm = base64.b64decode(response["audio_base64"], validate=True)
    if "".join(align["characters"]) != text or not pcm or len(pcm) % 2:
        raise ValueError("De API-opname of tijdcodes passen niet bij de opgevraagde tekst.")
    timings = []
    offset = 0
    for line in lines:
        start = align["character_start_times_seconds"][offset]
        end = align["character_end_times_seconds"][offset + len(line) - 1]
        duration = len(pcm) / (2 * RATE)
        # The API rounds timestamps to milliseconds; PCM ends on a sample boundary.
        if not 0 <= start < min(end, duration) or end > duration + 0.001:
            raise ValueError(
                f"Tijdcodes buiten opname: start={start:.6f}s, eind={end:.6f}s, audio={duration:.6f}s."
            )
        timings.append([start, min(end, duration)])
        offset += len(line) + 1
    if not hit:
        temp = file.with_suffix(".tmp")
        temp.write_text(json.dumps(response), encoding="utf-8")
        temp.replace(file)
        print(f"TTS API: {text}")
    return pcm, timings


def render(template, values):
    return re.sub(r"\{\{([\w-]+)\}\}", lambda match: str(values[match[1]]), template)


def prepare(original, cache, endpoint, key, additional_regulations_path=None,
            before_api_call=None, allow_api=True):
    reference = original.read_text(encoding="utf-8")
    configuration = load_configuration(additional_regulations_path)
    rules = {
        rule["code"]: {
            "percentage": rule["partnerpensioen"]["percentage_pensioengevend_salaris"],
            "maanden": rule["partnerpensioen"]["uitloop_maanden"],
        }
        for rule in configuration["regelingen"]
    }
    base_code = configuration["basis_regeling"]
    scenario = json.loads((V3 / "scenario.json").read_text())
    assets = re.findall(r'data:image/webp;base64,[A-Za-z0-9+/=]+', reference)
    asset_names = ("deelnemer", "partner-glimlach", "partner-neutraal")
    if len(assets) != len(asset_names):
        raise ValueError("De oorspronkelijke personageafbeeldingen ontbreken.")
    scene_source = (V3 / "assets/scene.svg").read_text()
    recordings = original_blocks(reference, [cue["text"].format_map(rules[base_code]) for cue in scenario])
    variants = {}
    for name, rule in rules.items():
        lines = [cue["text"].format_map(rule) for cue in scenario]
        chunks, timing = [], []
        samples = 0
        for first, last in BLOCKS:
            phrase = tuple(lines[first:last])
            if phrase not in recordings:
                recordings[phrase] = speech(
                    phrase, cache, endpoint, key, before_api_call, allow_api
                )
            pcm, local = recordings[phrase]
            timing.extend((start + samples / RATE, end + samples / RATE) for start, end in local)
            chunks.append(pcm)
            samples += len(pcm) // 2
        timeline = []
        for i, (cue, text, (start, end)) in enumerate(zip(scenario, lines, timing)):
            changes = {}
            for target, change in cue["changes"].items():
                to, duration = change if isinstance(change, list) else (change, 0)
                if to == "partnerpensioen":
                    to = rule["percentage"] / 100
                if duration == "next":
                    duration = timing[i + 1][0] - start
                changes[target] = {"to": to, "duration": duration}
            timeline.append({"text": text, "start": start, "end": end, "changes": changes})
        mp3 = ffmpeg(b"".join(chunks), "-f", "s16le", "-ar", str(RATE), "-ac", "1",
                     "-i", "pipe:0", "-f", "mp3", "pipe:1")
        variants[name] = {
            "timeline": timeline,
            "audio": "data:audio/mpeg;base64," + base64.b64encode(mp3).decode(),
            **rule,
        }
    runtime_config = {
        "basisRegeling": base_code,
        "planCodes": list(rules),
        "personages": [
            {
                "id": personage["runtime_id"],
                "x": personage["x"],
                "phase": personage["fase_seconden"],
                "period": personage["knippercyclus_seconden"],
            }
            for personage in configuration["personages"]
        ],
        "animaties": configuration["animaties"],
    }
    return variants, render(scene_source, {**rules[base_code], **dict(zip(asset_names, assets))}), runtime_config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--cache", required=True, type=Path)
    parser.add_argument("--test-api", help="HTTP fixture op localhost voor de technische proef")
    parser.add_argument("--additional-regulations", type=Path,
                        help="Privé JSON-bestand met aanvullende regelingen")
    parser.add_argument("--tts-usage-file", type=Path,
                        help="Privé dagteller voor echte TTS-aanroepen")
    parser.add_argument("--tts-daily-limit", type=int, default=0,
                        help="Maximum aantal echte TTS-aanroepen per UTC-dag")
    parser.add_argument("--offline", action="store_true",
                        help="Gebruik alleen al gecachete audio; doe geen API-aanroepen")
    args = parser.parse_args()
    if args.output.resolve().is_relative_to(ROOT.parents[1]) or args.cache.resolve().is_relative_to(ROOT.parents[1]):
        parser.error("Kies een uitvoer- en cachepad buiten de repository.")
    key = os.environ.get("ELEVENLABS_API_KEY", "")
    if args.test_api and not re.fullmatch(r"http://127\.0\.0\.1:\d+", args.test_api):
        parser.error("Gebruik voor de test-API uitsluitend http://127.0.0.1:<poort>.")
    if not args.test_api and not args.offline and not key:
        parser.error("ELEVENLABS_API_KEY ontbreekt.")
    if args.tts_usage_file and (args.offline or args.test_api or args.tts_daily_limit < 1):
        parser.error("De TTS-dagteller vereist een echte online bouw en een limiet van minimaal 1.")
    if args.tts_daily_limit and not args.tts_usage_file:
        parser.error("Gebruik --tts-daily-limit alleen samen met --tts-usage-file.")
    os.umask(0o077)
    args.cache.mkdir(parents=True, exist_ok=True)
    before_api_call = None
    if args.tts_usage_file:
        before_api_call = lambda: reserve_daily_tts_call(args.tts_usage_file, args.tts_daily_limit)
    variants, scene, runtime_config = prepare(args.reference, args.cache,
                                              args.test_api or "https://api.elevenlabs.io/v1/text-to-speech",
                                              "test" if args.test_api else key,
                                              args.additional_regulations, before_api_call,
                                              allow_api=not args.offline)
    template = (V3 / "template.html").read_text().replace("POC v3", "POC fase 3").replace("PROTOTYPE · V3", "PROTOTYPE · FASE 3")
    options = "".join(f"<option>{code}</option>" for code in runtime_config["planCodes"])
    template = re.sub(r"<h1>Partnerpensioen</h1><p>[^<]+</p>",
                      f'<h1>Partnerpensioen</h1><label>Fictieve regeling <select id="plan">{options}</select></label><p id="summary"></p>', template)
    if args.test_api:
        template = template.replace("Audio: ElevenLabs.", "Technische proef: bij 50% en 6 maanden staat een korte testtoon in plaats van de nieuwe gesproken zin.")
    template = template.replace("const timeline = {{timeline}};", "const runtimeConfig = {{runtimeConfig}};\nconst variants = {{variants}};\nlet timeline = variants[{{basisRegeling}}].timeline;")
    engine = (ROOT / "engine.js").read_text()
    start = engine.index("for (const { start, changes } of timeline)")
    end = engine.index("\n\nfunction draw()", start)
    build_tracks = engine[start:end]
    engine = engine[:start] + engine[end:]
    engine = engine.removesuffix("draw();\n")
    engine += """
function selectPlan(name) {
    const plan = variants[name];
    audio.pause();
    audio.src = plan.audio;
    timeline = plan.timeline;
    element('summary').textContent = `${plan.percentage}% van pensioengevend salaris · ${plan.maanden} maanden tijdelijke dekking`;
    element('percent').querySelector('text').textContent = plan.percentage + '%';
    element('coverage').querySelector('text').textContent = plan.maanden + ' maanden verzekerd';
    tracks.clear();
""" + "\n".join("    " + line for line in build_tracks.splitlines()) + """
}
element('plan').addEventListener('change', event => selectPlan(event.target.value));
selectPlan(runtimeConfig.basisRegeling);
draw();
"""
    base_code = runtime_config["basisRegeling"]
    output = render(template, {"scene": scene, "audio": variants[base_code]["audio"],
                               "variants": json.dumps(variants, ensure_ascii=False).replace("<", r"\u003c"),
                               "runtimeConfig": json.dumps(runtime_config, ensure_ascii=False).replace("<", r"\u003c"),
                               "basisRegeling": json.dumps(base_code),
                               "engine": engine})
    with args.output.open("x", encoding="utf-8") as preview:
        preview.write(output)


if __name__ == "__main__":
    main()
