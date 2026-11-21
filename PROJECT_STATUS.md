# Pensioen ontdekt — projectstatus
Bijgewerkt: 2026-11-21

## Doel
Interactieve, begrijpelijke uitleg van pensioenregelingen. Iteratief ontwikkelen, eerst fictieve regeling, later zeven geparametriseerde regelingen. Gebruiker bepaalt inhoud en creatieve richting.

## Huidige stand
- Homepage v0.1 gepubliceerd op https://pensioen.myaiprojects.nl.
- Fase 1 (POC) op 2026-11-21 door gebruiker geslaagd verklaard. Script en visuele afwerking nog niet definitief.
- v1: eenvoudige SVG-personages; v2: verbeterde illustraties, neutrale gezichtsvariant en landschappelijke achtergrond; v3: ook subtiele lichaamsbeweging, ademhaling en knipperen.
- Laatste lokale testbestand: partnerpensioen-v3.html, inclusief privé-audio. Bewaar lokaal; niet publiceren of in openbare repository opnemen.
- Generatoren v1 en v2 staan in poc/; lokale v3 is nog niet als reproduceerbare generator in GitHub opgenomen.
- Stem Adam uitsluitend technische test; definitieve stemkeuze uitgesteld.
- Ontwerpprincipes toekomstige personages: docs/ontwerpprincipes-personages.md.
- Lokale ontwikkeling en tests voorafgaand aan deployment; server niet gewijzigd voor v2/v3 lokale tests.

## Verhaallijn
Salaris werkgever naar gezinsinkomen; deelnemer overlijdt en vervaagt, geldstroom stopt, werkgever verdwijnt. Pensioenfonds verschijnt, partner krijgt levenslang X% van pensioengevend salaris, geldstroom hervat. Reset naar beiden levend en glimlachend. Uitdiensttreding: werkgever en salaris verdwijnen, tijdelijke risicodekking Y maanden, daarna eindigt die dekking; mogelijkheden voor voortzetting. Verdieping later: partnerdefinitie, pensioengevend salaris, aanvragen, uitdiensttreding en aanvullende voorzieningen. Fictieve waarden X=40, Y=3. Regelingafhankelijke uitzonderingen nog valideren.

## Techniek
Ubuntu VPS, Nginx, HTTPS. Python generator met ElevenLabs timestamps en lokale audiocache, SVG/HTML animatie op audiotijd. API-sleutel uitsluitend buiten webroot/repository op server. Toekomstig: generieke parameterengine, database en backend; nog niet gebouwd. GSAP is kandidaat, huidige POC gebruikt native JS. Geen vertrouwelijke data.

## Roadmap
1. Fase 1 — POC afgerond.
2. Fase 2 — generieke architectuur: scheid script/scenario, pensioenparameters, illustraties, audiobibliotheek en animatie-engine. Begin met bestaande partnerpensioen-POC; geen overengineering.
3. Fase 3 — dynamische regelingen: verschillende waarden zonder codewijziging; gesproken tekst moet overeenkomen met parameters. Onderzoek hergebruik van audiofragmenten en timestamps.
4. Fase 4 — tweede onderwerp, bijvoorbeeld wezenpensioen, om herbruikbaarheid te toetsen.
5. Fase 5 — inhoud valideren, script en beeld verfijnen, integreren in website en publiceren.

## Start fase 2
- Nieuwe chat binnen hetzelfde project; lees dit bestand en relevante broncode.
- Leg eerst een minimale bestandsstructuur en interfaces voor. Maak v3 reproduceerbaar zonder audio in GitHub op te nemen.
- Bouw en test lokaal, behoud bestaande POC als referentie. Geen deployment zonder akkoord.
- Gebruik generieke bewegingen per personage; onderhoudbaarheid en eenvoud boven maximale animatiecomplexiteit.
- Leg besluiten en voortgang hier vast. Definitieve scripts nog niet goedgekeurd.

## Publicatie
Private POC niet openbaar publiceren met gratis ElevenLabs-audio. Generator staat in GitHub; gegenereerde audio/HTML blijft privé. Geen secrets in repo.
