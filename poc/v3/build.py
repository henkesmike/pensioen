#!/usr/bin/env python3
"""Build a standalone private v3 preview from the original local prototype."""
import argparse
import json
import math
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
IMAGE_NAMES = ("deelnemer", "partner-glimlach", "partner-neutraal")


def render(template, values):
    return re.sub(r"\{\{([\w-]+)\}\}", lambda match: str(values[match[1]]), template)


def build(reference):
    scenario = json.loads((ROOT / "scenario.json").read_text(encoding="utf-8"))
    rules = json.loads((ROOT / "regeling.json").read_text(encoding="utf-8"))
    texts = [cue["text"].format_map(rules) for cue in scenario]

    # The v3 file contains the existing locally generated speech and cue alignment.
    alignment = re.search(
        r"const lines=(\[[^\n]*?\]), starts=(\[[^\n]*?\]), ends=(\[[^\n]*?\]), pct=",
        reference,
    )
    if not alignment:
        raise ValueError("Geen tijdcodes gevonden in het oorspronkelijke v3-bestand.")
    recorded_texts, starts, ends = (json.loads(group) for group in alignment.groups())
    if texts != recorded_texts:
        raise ValueError("Script of regeling wijkt af van de lokale voice-over.")
    if (
        len(starts) != len(texts) or len(ends) != len(texts) or not starts
        or starts[0] != 0
        or not all(math.isfinite(value) for value in starts + ends)
        or not all(start < end <= next_start for start, end, next_start in zip(
            starts, ends, starts[1:] + [math.inf]
        ))
    ):
        raise ValueError("Ongeldige tijdcodes in het oorspronkelijke v3-bestand.")

    timeline = []
    for index, (cue, text, start, end) in enumerate(zip(scenario, texts, starts, ends)):
        changes = {}
        for target, change in cue["changes"].items():
            to, duration = change if isinstance(change, list) else (change, 0)
            if to == "partnerpensioen":
                to = rules["percentage"] / 100
            if duration == "next":
                duration = starts[index + 1] - start
            changes[target] = {"to": to, "duration": duration}
        timeline.append({"text": text, "start": start, "end": end, "changes": changes})

    images = re.findall(r'data:image/webp;base64,[A-Za-z0-9+/=]+', reference)
    audio = re.findall(r'data:audio/mpeg;base64,[A-Za-z0-9+/=]+', reference)
    if len(images) != len(IMAGE_NAMES) or len(audio) != 1:
        raise ValueError("De drie personageafbeeldingen en de voice-over zijn vereist.")
    scene = render(
        (ROOT / "assets/scene.svg").read_text(encoding="utf-8"),
        {**rules, **dict(zip(IMAGE_NAMES, images))},
    )
    return render(
        (ROOT / "template.html").read_text(encoding="utf-8"),
        {
            **rules,
            "scene": scene.rstrip("\n"),
            "audio": audio[0],
            "timeline": json.dumps(timeline, ensure_ascii=False).replace("<", r"\u003c"),
            "engine": (ROOT / "engine.js").read_text(encoding="utf-8"),
        },
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path, help="Originele lokale partnerpensioen-v3.html")
    parser.add_argument("output", type=Path, help="Nieuw HTML-bestand buiten de repository")
    args = parser.parse_args()

    output = args.output.resolve()
    # Keep embedded speech out of the repository and preserve the source file.
    if output.is_relative_to(ROOT.parents[1]) or output == args.reference.resolve():
        parser.error("Kies een nieuw uitvoerbestand buiten de repository.")
    try:
        html = build(args.reference.read_text(encoding="utf-8"))
        os.umask(0o077)
        with output.open("x", encoding="utf-8") as preview:
            preview.write(html)
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
