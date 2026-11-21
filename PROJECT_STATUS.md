# Pensioen ontdekt — projectstatus
Bijgewerkt: 2026-11-21

## Doel
Interactieve, begrijpelijke uitleg van pensioenregelingen. Iteratief ontwikkelen, eerst fictieve regeling, later zeven geparametriseerde regelingen. Gebruiker bepaalt inhoud en creatieve richting.

De [missie en het einddoel](docs/missie-en-einddoel.md) beschrijven hoe een beoordeeld pensioenreglement via regelingparameters, selectieregels en herbruikbare voice-overs leidt tot regelinggerichte uitleg op de website.

## Huidige stand
- Homepage v0.1 gepubliceerd op https://pensioen.myaiprojects.nl.
- Fase 1 (POC) op 2026-11-21 door gebruiker geslaagd verklaard. Script en visuele afwerking nog niet definitief.
- v1: eenvoudige SVG-personages; v2: verbeterde illustraties, neutrale gezichtsvariant en landschappelijke achtergrond; v3: ook subtiele lichaamsbeweging, ademhaling en knipperen.
- Laatste lokale testbestand: partnerpensioen-v3.html, inclusief privé-audio. Bewaar lokaal; niet publiceren of in openbare repository opnemen.
- Generatoren v1 en v2 staan in `poc/`. De reproduceerbare v3 staat in `poc/v3/` op de [fase 2-branch](https://github.com/henkesmike/pensioen/tree/fase-2-partnerpensioen-v3/poc/v3).
- Stem Adam uitsluitend technische test; definitieve stemkeuze uitgesteld.
- Ontwerpprincipes toekomstige personages: docs/ontwerpprincipes-personages.md.
- Lokale ontwikkeling en tests voorafgaand aan deployment; server niet gewijzigd voor v2/v3 lokale tests.

## Verhaallijn
Salaris werkgever naar gezinsinkomen; deelnemer overlijdt en vervaagt, geldstroom stopt, werkgever verdwijnt. Pensioenfonds verschijnt, partner krijgt levenslang X% van pensioengevend salaris, geldstroom hervat. Reset naar beiden levend en glimlachend. Uitdiensttreding: werkgever en salaris verdwijnen, tijdelijke risicodekking Y maanden, daarna eindigt die dekking; mogelijkheden voor voortzetting. Verdieping later: partnerdefinitie, pensioengevend salaris, aanvragen, uitdiensttreding en aanvullende voorzieningen. Fictieve waarden X=40, Y=3. Regelingafhankelijke uitzonderingen nog valideren.

## Ontwerp voor herbruikbare fragmenten
- Splits de uitleg over partnerpensioen in twee zelfstandig afspeelbare fragmenten: **Tijdens dienstverband** en **Na uitdiensttreding**.
- De pagina Partnerpensioen speelt beide fragmenten in die volgorde. Het event Uitdiensttreding gebruikt hetzelfde tweede fragment als onderdeel van de uitleg. Het tweede fragment krijgt een zelfstandige openingszin en een vaste beginstand met beide personages en de werkgever zichtbaar.
- Elk fragment heeft een eigen scenario, voice-over en tijdcodes vanaf nul. De animatie-engine en illustraties zijn gedeeld. De voice-over hoort bij de regelingwaarden die in het fragment worden getoond.
- Laat bij de overgang alleen het animatiebeeld geleidelijk naar zwart gaan. Wissel bij zwart naar de beginstand van het volgende fragment en laat het beeld terugkomen. Plaats de overgang tussen gesproken zinnen. Eerste testwaarde: circa 0,5 seconde per fade. Bij los afspelen kan het tweede fragment vanaf zwart openen.
- Toets in fase 3 beide afspeelroutes en controleer of beeld, ondertiteling en voice-over vanaf de juiste beginstand lopen, ook bij terugspoelen.

## Techniek
Ubuntu VPS, Nginx, HTTPS. Python generator met ElevenLabs timestamps en lokale audiocache, SVG/HTML animatie op audiotijd. API-sleutel uitsluitend buiten webroot/repository op server. Toekomstig: generieke parameterengine, database en backend; nog niet gebouwd. GSAP is kandidaat, huidige POC gebruikt native JS. Geen vertrouwelijke data.

## Roadmap
1. Fase 1 — POC afgerond.
2. Fase 2 — afgerond voor de partnerpensioenpilot. Gebruiker heeft de privétestversie op 2026-11-21 akkoord bevonden voor deze fase.
3. Fase 3 — dynamische regelingen: verschillende waarden zonder codewijziging; gesproken tekst moet overeenkomen met parameters. Onderzoek hergebruik van audiofragmenten en timestamps.
4. Fase 4 — tweede onderwerp, bijvoorbeeld wezenpensioen, om herbruikbaarheid te toetsen.
5. Fase 5 — inhoud valideren, script en beeld verfijnen, integreren in website en publiceren.

## Vervolg na fase 2
- Eerstvolgende technische stap volgens de roadmap is fase 3: onderzoeken hoe regelingwaarden en gesproken tekst samen kunnen variëren.
- De goedkeuring geldt voor de privétestversie van fase 2. Definitief script, stemkeuze en publicatie staan nog open.

## Eerste proef fase 3
- De [proef met vier regelingen](https://github.com/henkesmike/pensioen/tree/fase-3-vier-regelingen/poc/v4) combineert A (40%, 3 maanden), B (40%, 6 maanden), C (50%, 3 maanden) en D (50%, 6 maanden).
- De backend knipt de originele opname op in drie vaste blokken en twee variabele zinnen. De vier combinaties delen twee percentagezinnen en twee duurzinnen. De bestaande audio bevat 40% en 3 maanden.
- De HTTP-proef verifieerde twee automatische aanroepen, voor 50% en 6 maanden, en nul bij herhaling. Keuzelijst, audiobron, beeldlabels, ondertiteling en herberekende tijdcodes zijn technisch gecontroleerd. De proef gebruikt een lokale test-API met testtonen voor de twee nieuwe zinnen.
- Open voor deze iteratie: echte ElevenLabs-aanroepen met de bestaande sleutel en beluisteren van de overgangen. Privéproef, zonder wijzigingen aan de live site.

## Publicatie
Private POC niet openbaar publiceren met gratis ElevenLabs-audio. Generator staat in GitHub; gegenereerde audio/HTML blijft privé. Geen secrets in repo.
