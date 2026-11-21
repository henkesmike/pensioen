# Pensioen ontdekt — projectstatus
Bijgewerkt: 2026-11-21

## Doel
Interactieve, begrijpelijke uitleg van pensioenregelingen. Iteratief ontwikkelen, eerst fictieve regeling, later zeven geparametriseerde regelingen. Gebruiker bepaalt inhoud en creatieve richting.

## Huidige stand
- Homepage v0.1 gepubliceerd op https://pensioen.myaiprojects.nl.
- Private partnerpensioen-POC: poc/private_animation.py. ElevenLabs API, MP3-generatie en HTML-generatie op VPS gelukt; lokaal op Windows bekeken.
- Beeldkwaliteit afgekeurd: getekende SVG-personages te eenvoudig; witte achtergrond te kaal. Overige eenvoudige iconen akkoord.
- Oorspronkelijke karakterillustratie opnieuw aangeleverd en nieuwe varianten (man, vrouw glimlachend, vrouw neutraal) gemaakt; nog niet geïntegreerd.
- Stem Adam uitsluitend technische test; definitieve stemkeuze uitgesteld. Gratis audio uitsluitend privé testen.
- Ontwerpprincipes toekomstige personages: docs/ontwerpprincipes-personages.md.

## Verhaallijn
Salaris werkgever naar gezinsinkomen; deelnemer overlijdt en vervaagt, geldstroom stopt, werkgever verdwijnt. Pensioenfonds verschijnt, partner krijgt levenslang X% van pensioengevend salaris, geldstroom hervat. Reset naar beiden levend en glimlachend. Uitdiensttreding: werkgever en salaris verdwijnen, tijdelijke risicodekking Y maanden, daarna eindigt die dekking; mogelijkheden voor voortzetting. Verdieping later: partnerdefinitie, pensioengevend salaris, aanvragen, uitdiensttreding en aanvullende voorzieningen. Fictieve waarden X=40, Y=3. Regelingafhankelijke uitzonderingen nog valideren.

## Techniek
Ubuntu VPS, Nginx, HTTPS. Python generator met ElevenLabs timestamps en lokale audiocache, SVG/HTML animatie op audiotijd. API-sleutel uitsluitend buiten webroot/repository op server. Toekomstig: generieke parameterengine, database en backend; nog niet gebouwd. GSAP is kandidaat, huidige POC gebruikt native JS. Geen vertrouwelijke data.

## Eerstvolgende acties
1. Hoogwaardige afzonderlijke karakterafbeeldingen integreren, neutrale gezichtsvariant bij overlijden, warme achtergrond met diepte; eenvoudige gebouwen en geldstromen behouden.
2. Beeld en synchronisatie beoordelen; POC itereren tot akkoord.
3. Geaccordeerd script en architectuur als afzonderlijke versieerbare documenten vastleggen.
4. Daarna nieuwe chat per ontwikkelfase binnen hetzelfde project, start met lezen van dit bestand en relevante code/documenten.
5. Dit bestand aanpassen bij belangrijke beslissingen en afgeronde stappen.

## Publicatie
Private POC niet openbaar publiceren met gratis ElevenLabs-audio. Generator staat in GitHub; gegenereerde audio/HTML blijft privé. Geen secrets in repo.
