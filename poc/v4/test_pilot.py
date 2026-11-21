"""Check the four plans against an HTTP fixture. No external requests."""
import argparse
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile
from threading import Thread

from build import RATE, ROOT

requests = []


class SpeechFixture(BaseHTTPRequestHandler):
    def do_POST(self):
        assert self.path.endswith("/with-timestamps?output_format=pcm_24000")
        assert self.headers["xi-api-key"] == "test"
        text = json.loads(self.rfile.read(int(self.headers["Content-Length"])))["text"]
        requests.append(text)
        duration = len(text) / 20 + 0.1997
        frames = int(duration * RATE)
        pcm = b"".join(struct.pack("<h", 1800 if index % 120 < 60 else -1800)
                       for index in range(frames))
        result = json.dumps({
            "audio_base64": base64.b64encode(pcm).decode(),
            "alignment": {
                "characters": list(text),
                "character_start_times_seconds": [0.2 + i / 20 for i in range(len(text))],
                "character_end_times_seconds": [0.2 + (i + 1) / 20 for i in range(len(text))],
            },
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(result)

    def log_message(self, *_):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as cache, HTTPServer(("127.0.0.1", 0), SpeechFixture) as server:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        command = [
            sys.executable, str(ROOT / "build.py"), str(args.reference), str(args.output),
            "--cache", cache, "--test-api", f"http://127.0.0.1:{server.server_port}",
        ]
        try:
            subprocess.run(command, check=True)
            assert requests == [
                "Je partnerpensioen blijft nog 6 maanden verzekerd.",
                "Je partner ontvangt dan 50 procent van je pensioengevend salaris.",
            ], requests
            with tempfile.TemporaryDirectory() as repeat:
                command[3] = str(Path(repeat) / "repeat.html")
                subprocess.run(command, check=True)
            assert len(requests) == 2
        finally:
            server.shutdown()
            thread.join()
    html = args.output.read_text()
    variants = json.loads(re.search(r"const variants = (.*);\n", html)[1])
    rules = {"A": (40, 3), "B": (40, 6), "C": (50, 3), "D": (50, 6)}
    for name, (percentage, months) in rules.items():
        plan = variants[name]
        assert (plan["percentage"], plan["maanden"]) == (percentage, months)
        cues = plan["timeline"]
        assert f"{percentage} procent" in cues[4]["text"]
        assert f"{months} maanden" in cues[9]["text"]
        assert cues[4]["changes"]["income"]["to"] == percentage / 100
        assert all(a["start"] < a["end"] <= b["start"] for a, b in zip(cues, cues[1:]))
        assert f"<option>{name}</option>" in html
    assert len({plan["timeline"][i]["text"] for plan in variants.values() for i in (4, 9)}) == 4
    print("A–D: 4 variabele zinnen, 2 nieuwe HTTP-aanroepen, 0 bij herhaling.")
    script = re.search(r"<script>([\s\S]*?)</script>", html)[1]
    subprocess.run(["node", "--check", "-"], input=script, text=True, check=True)


if __name__ == "__main__":
    main()
