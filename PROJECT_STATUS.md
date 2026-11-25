# Pensioen Ontdekt — projectstatus

Bijgewerkt op 25 november 2026.

## Doel

### Missie

Pensioen Ontdekt helpt deelnemers begrijpen wat hun pensioenregeling betekent bij gebeurtenissen zoals uitdiensttreding, arbeidsongeschiktheid, overlijden en scheiden. De website geeft interactieve uitleg die aansluit bij de regeling en persoonlijke situatie. Filmpjes, fragmenten en voice-overs zijn herbruikbaar.

### Visie

AI maakt het mogelijk om pensioencommunicatie op maat te maken binnen één omgeving. De uitleg sluit aan bij de persoonlijke situatie, de taal en de specifieke pensioenregeling van de deelnemer.

### Technisch einddoel

Het einddoel is dat een beheerder beoordeelde regelingparameters kan uploaden. De website toont daarna de toepasselijke uitleg zonder codewijziging voor ondersteunde scenario’s. De [technische uitwerking](docs/technisch-ontwerp.md#van-pensioenreglement-naar-website) beschrijft de beoogde keten.

## Huidige stand

- De [homepage](https://pensioen.myaiprojects.nl/) en de [Partnerpensioen-demo](https://pensioen.myaiprojects.nl/partnerpensioen-demo.html) staan live. Mike heeft de POC goedgekeurd. De demo heeft herstelde figuurselectie, stille titelkaarten en een losse afspeelroute voor Uitdiensttreding. De rest van de bestaande voice-over blijft hoorbaar.
- Het publieke formulier voor fictieve regelingen werkt. Regeling E stond al opgeslagen (45%, 1 maand). De live proef met 60% en 3 maanden leverde kandidaat F op. F blijft een concept.
- [Scheiden v9](https://pensioen.myaiprojects.nl/?onderwerp=scheiden) staat live via **Uit elkaar gaan**. De publieke versie gebruikt de door Mike goedgekeurde ElevenLabs-opname met Adam. De animatie staat op [scheiden-adam.html](https://pensioen.myaiprojects.nl/scheiden-adam.html). De blokken schuiven uit elkaar bij de zin over de uitbetaling. De goedgekeurde versie is gepubliceerd vanuit commit `176e17456656d0c042f6c3a71a28a477bca3dbc2`.
- De voice-overworker is op de VPS geïnstalleerd. De opname en homepagekoppeling zijn gepubliceerd en gecontroleerd. De publieke opname komt overeen met de goedgekeurde preview (SHA-256 `7dea0e5639135362583fc06185338c839542ab3264c4f16edafb24c1ae2c9090`).

- De productieopdracht voor de homepage met persoonlijke keuzes is klaargezet voor commit `a91deeb257ca0a6063adfa6f1c7a92f59aca7b96`. De homepage gebruikt drie uitklapbare keuzes, zes originele portretten in twee verticale keuzewielen en ‘Zeg ik liever niet’ als eerste keuze bij de persoonlijke situatie. Regeling F blijft concept. Publieke controle van deze uitrol staat nog open.

## Open werk

- Maak korte filmpjes om hergebruik en een herkenbare opbouw te toetsen. Uitdiensttreding en wezenpensioen zijn besproken als mogelijke volgende onderwerpen.
- Valideer regelingafhankelijke uitzonderingen en verfijn waar nodig inhoud, script en beeld voordat nieuwe filmpjes worden gepubliceerd.
- Onderzoek dynamische pensioeninformatie per regeling en persoonlijke situatie.

Onderzoek hoe de website bepaalt welke onderwerpen, filmpjes of fragmenten relevant zijn op basis van de pensioenregeling en de persoonlijke situatie.

1. **Pensioensoorten in de regeling.** Bepaal welke pensioensoorten de regeling wel en niet bevat en stem het getoonde aanbod daarop af.
2. **Partner.** Geef de gebruiker een plek om aan te geven of die een partner heeft. Onderzoek welke uitleg per situatie relevant is.
3. **Kinderen.** Onderzoek hoe de gebruiker kan aangeven of die kinderen heeft en hoe dat de getoonde uitleg beïnvloedt.
4. **Afstand tot de pensioenleeftijd.** Onderzoek wanneer iemand dicht bij de pensioenleeftijd is en welke informatie dan relevant wordt.
5. **Andere factoren.** Onderzoek samen welke aanvullende kenmerken van de regeling of persoonlijke situatie de uitleg relevanter maken.

Deze punten staan open voor een latere uitwerking.

## Documentatie

- [Ontwikkelworkflow](docs/ontwikkelworkflow-filmpjes.md) voor bouwen, testen, voice-over, previews, uitrol en herstel.
- [Technisch ontwerp](docs/technisch-ontwerp.md) voor configuratie, animaties, personages en de beoogde verwerking van reglementen.
- [Voorgaande projectstatus en proefhistorie](https://github.com/henkesmike/pensioen/blob/575d5fce80724e7f8fcbf36b3253b0c3901fd54a/PROJECT_STATUS.md) voor eerdere besluiten, proefbestanden en publicatiechecksums.
