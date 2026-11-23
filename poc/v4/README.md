# Fase 3 – vier fictieve regelingen

Deze private proef gebruikt versie 1 van de JSON-configuratie in `data/`:

- `regelingen.json`: de regelingcodes en waarden voor percentage en uitloopduur.
- `personages.json`: stabiele personage-id's, assetverwijzingen en bewegingsposities.
- `animaties.json`: ademhalings-, zwaai- en knipperinstellingen.

`config.py` leest de bestanden centraal in en controleert schema-versies,
verplichte velden, typen, grenzen, unieke id's en verwijzingen voordat de
generator een preview maakt. Tijdseenheden zijn seconden; percentages zijn
percentagepunten (40 betekent 40%); posities zijn SVG-eenheden. De generator
zet de gevalideerde instellingen om naar runtimeconfiguratie voor de browser.
De preview blijft één statisch HTML-bestand.

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

De proef verwacht twee API-aanroepen voor 50 procent en 6 maanden en nul
aanroepen bij een volgende run met dezelfde cache. Bewaar de gegenereerde
HTML en audiocache buiten de repository en de webroot. De publieke demo
wordt door deze private proef niet gewijzigd.
