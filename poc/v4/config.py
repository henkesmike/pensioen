"""Load and validate the pilot's versioned JSON configuration."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
STABLE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PLAN_CODE = re.compile(r"^[A-Z][A-Z0-9_-]{0,19}$")


def _read_json(name):
    path = DATA / name
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Kan configuratiebestand {path} niet lezen: {error}") from error
    if not isinstance(value, dict) or type(value.get("schema_version")) is not int or value["schema_version"] != 1:
        raise ValueError(f"{name}: verwacht een JSON-object met schema_version 1.")
    return value


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
    regulation_data = _read_json("regelingen.json")
    character_data = _read_json("personages.json")
    animation_data = _read_json("animaties.json")
    regulations = regulation_data.get("regelingen")
    characters = character_data.get("personages")
    settings = animation_data.get("animaties")
    if not isinstance(regulations, list) or not regulations:
        raise ValueError("regelingen.json: regelingen moet een niet-lege lijst zijn.")
    if not isinstance(characters, list):
        raise ValueError("personages.json: personages moet een lijst zijn.")
    if not isinstance(settings, dict) or any(
        not isinstance(settings.get(key), dict) for key in ("ademhalen", "zwaaien", "knipperen")
    ):
        raise ValueError("animaties.json: ademhalen, zwaaien en knipperen moeten objecten zijn.")

    _unique_ids(regulations, "regelingen")
    codes = [item.get("code") for item in regulations]
    if any(not isinstance(code, str) or not PLAN_CODE.fullmatch(code) for code in codes):
        raise ValueError("Elke regeling moet een code met hoofdletters en cijfers hebben.")
    if len(codes) != len(set(codes)):
        raise ValueError("Regelingcodes moeten uniek zijn.")
    base_rules = [item for item in regulations if item.get("bron_audio") is True]
    if len(base_rules) != 1:
        raise ValueError("Markeer precies één regeling als bron_audio: true.")
    for rule in regulations:
        if not isinstance(rule.get("naam"), str) or not isinstance(rule.get("partnerpensioen"), dict):
            raise ValueError(f"{rule['id']}: naam en partnerpensioen zijn verplicht.")
        values = rule["partnerpensioen"]
        _number(values.get("percentage_pensioengevend_salaris"), f"{rule['id']}.percentage")
        _number(values.get("uitloop_maanden"), f"{rule['id']}.uitloop_maanden", 1)
        if values["percentage_pensioengevend_salaris"] > 100:
            raise ValueError(f"{rule['id']}: percentage mag maximaal 100 zijn.")

    character_ids = _unique_ids(characters, "personages")
    if character_ids != {"deelnemer", "partner-glimlach", "partner-neutraal"}:
        raise ValueError("De scene vereist deelnemer, partner-glimlach en partner-neutraal.")
    runtime_ids = [item.get("runtime_id") for item in characters]
    asset_keys = [item.get("asset_key") for item in characters]
    if set(runtime_ids) != {"man", "happy", "neutral"} or len(runtime_ids) != len(set(runtime_ids)):
        raise ValueError("Runtime-id's van personages moeten uniek zijn: man, happy en neutral.")
    if set(asset_keys) != character_ids or len(asset_keys) != len(set(asset_keys)):
        raise ValueError("Assetverwijzingen moeten uniek zijn en naar bekende personages wijzen.")
    for character in characters:
        _number(character.get("x"), f"{character['id']}.x")
        _number(character.get("fase_seconden"), f"{character['id']}.fase_seconden")
        _number(character.get("knippercyclus_seconden"), f"{character['id']}.knippercyclus_seconden", 0.1)

    for key in ("ademhalen", "zwaaien"):
        _number(settings[key].get("cyclus_seconden"), f"{key}.cyclus_seconden", 0.1)
        _number(settings[key].get("amplitude"), f"{key}.amplitude")
    _number(settings["ademhalen"].get("verticale_factor"), "ademhalen.verticale_factor")
    _number(settings["knipperen"].get("duur_seconden"), "knipperen.duur_seconden", 0.01)
    _number(settings["knipperen"].get("drempel"), "knipperen.drempel")
    _number(settings["knipperen"].get("fase_offset_seconden"), "knipperen.fase_offset_seconden")

    return {
        "regelingen": regulations,
        "basis_regeling": base_rules[0]["code"],
        "personages": characters,
        "animaties": settings,
    }
