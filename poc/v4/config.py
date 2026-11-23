"""Load and validate the pilot's versioned JSON configuration."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
STABLE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _load(name, collection):
    path = DATA / name
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Kan configuratiebestand {path} niet lezen: {error}") from error
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise ValueError(f"{name}: verwacht een JSON-object met schema_version 1.")
    if not isinstance(value.get(collection), list):
        raise ValueError(f"{name}: veld {collection} moet een lijst zijn.")
    return value[collection]


def _number(value, label, minimum=0):
    if type(value) not in (int, float) or value < minimum:
        raise ValueError(f"{label} moet een getal van minimaal {minimum} zijn.")


def _unique_ids(items, label):
    ids = [item.get("id") for item in items if isinstance(item, dict)]
    if len(ids) != len(items) or any(not isinstance(item, str) or not STABLE_ID.fullmatch(item) for item in ids):
        raise ValueError(f"{label}: elk item moet een object met stabiele id hebben.")
    if len(ids) != len(set(ids)):
        raise ValueError(f"{label}: id's moeten uniek zijn.")
    return set(ids)


def load_configuration():
    """Return validated regulations, character definitions and animation settings."""
    regulations = _load("regelingen.json", "regelingen")
    characters = _load("personages.json", "personages")
    animation = json.loads((DATA / "animaties.json").read_text(encoding="utf-8"))
    if not isinstance(animation, dict) or animation.get("schema_version") != 1:
        raise ValueError("animaties.json: verwacht schema_version 1.")
    settings = animation.get("animaties")
    if not isinstance(settings, dict) or not {"ademhalen", "zwaaien", "knipperen"} <= settings.keys():
        raise ValueError("animaties.json: ademhalen, zwaaien en knipperen zijn verplicht.")

    regulation_ids = _unique_ids(regulations, "regelingen")
    codes = [item.get("code") for item in regulations]
    if len(codes) != len(set(codes)) or any(code not in {"A", "B", "C", "D"} for code in codes):
        raise ValueError("Regelingcodes moeten uniek zijn en A, B, C of D zijn.")
    for rule in regulations:
        if not isinstance(rule.get("naam"), str) or not isinstance(rule.get("partnerpensioen"), dict):
            raise ValueError(f"{rule['id']}: naam en partnerpensioen zijn verplicht.")
        values = rule["partnerpensioen"]
        _number(values.get("percentage_pensioengevend_salaris"), f"{rule['id']}.percentage", 0)
        _number(values.get("uitloop_maanden"), f"{rule['id']}.uitloop_maanden", 1)
        if values["percentage_pensioengevend_salaris"] > 100:
            raise ValueError(f"{rule['id']}: percentage mag maximaal 100 zijn.")

    character_ids = _unique_ids(characters, "personages")
    if character_ids != {"deelnemer", "partner-glimlach", "partner-neutraal"}:
        raise ValueError("De bekende personage-id's moeten alle drie aanwezig zijn.")
    for character in characters:
        if character.get("asset_key") not in character_ids:
            raise ValueError(f"{character['id']}: onbekende asset_key.")
        _number(character.get("x"), f"{character['id']}.x")
        _number(character.get("fase_seconden"), f"{character['id']}.fase_seconden")
        _number(character.get("knippercyclus_seconden"), f"{character['id']}.knippercyclus_seconden", 0.1)

    for key in ("ademhalen", "zwaaien"):
        motion = settings[key]
        _number(motion.get("cyclus_seconden"), f"{key}.cyclus_seconden", 0.1)
        _number(motion.get("amplitude"), f"{key}.amplitude")
    _number(settings["ademhalen"].get("verticale_factor"), "ademhalen.verticale_factor")
    _number(settings["knipperen"].get("duur_seconden"), "knipperen.duur_seconden", 0.01)
    _number(settings["knipperen"].get("drempel"), "knipperen.drempel")
    _number(settings["knipperen"].get("fase_offset_seconden"), "knipperen.fase_offset_seconden")

    if {item["code"] for item in regulations} != {"A", "B", "C", "D"}:
        raise ValueError("Voor deze proef moeten regelingen A, B, C en D aanwezig zijn.")
    return {
        "regelingen": regulations,
        "personages": characters,
        "animaties": settings,
    }
