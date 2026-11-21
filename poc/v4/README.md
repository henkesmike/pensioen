# Fase 3 – vier fictieve regelingen

Voer de proef privé uit met Python 3.9+, ffmpeg en het oorspronkelijke
`partnerpensioen-v3.html`. Stel voor echte spraak `ELEVENLABS_API_KEY` in
via de bestaande geheime configuratie.

```sh
python3 poc/v4/build.py ~/Downloads/partnerpensioen-v3.html ~/Downloads/partnerpensioen-fase3.html --cache ~/pensioen-poc/fase3
```

Open het resultaat in de browser en kies A, B, C of D. De generator knipt
de bestaande opname op pauzes. Hij vraagt alleen ontbrekende zinnen op
en rekent de tijdcodes opnieuw uit op basis van de lengte van elk audioblok.

Voor de technische proef start het volgende commando een lokale test-API.
Die levert een testtoon voor de ontbrekende zinnen. Node is nodig voor
de JavaScript-syntaxiscontrole.

```sh
python3 poc/v4/test_pilot.py ~/Downloads/partnerpensioen-v3.html ~/Downloads/partnerpensioen-fase3-test.html
```

De test verwacht twee API-aanroepen voor 50 procent en 6 maanden en nul
aanroepen bij een volgende run met dezelfde cache. Bewaar de gegenereerde
HTML en audiocache buiten de repository en de webroot.
