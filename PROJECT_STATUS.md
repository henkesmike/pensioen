# Pensioen Ontdekt — projectstatus

Bijgewerkt op 28 november 2026.

## Doel

### Missie

Pensioen Ontdekt helpt deelnemers begrijpen wat hun pensioenregeling betekent bij gebeurtenissen zoals uitdiensttreding, arbeidsongeschiktheid, overlijden en scheiden. De website geeft interactieve uitleg die aansluit bij de regeling en persoonlijke situatie. Filmpjes, fragmenten en voice-overs zijn herbruikbaar.

### Visie

AI maakt het mogelijk om pensioencommunicatie op maat te maken binnen één omgeving. De uitleg sluit aan bij de persoonlijke situatie, de taal en de specifieke pensioenregeling van de deelnemer.

### Technisch einddoel

Het einddoel is dat een beheerder beoordeelde regelingparameters kan uploaden. De website toont daarna de toepasselijke uitleg zonder codewijziging voor ondersteunde scenario’s. De [technische uitwerking](docs/technisch-ontwerp.md#van-pensioenreglement-naar-website) beschrijft de beoogde keten.

## Huidige stand

- **Algemene bestandsdeployment:** de worker en installer zijn uitgebreid
  in GitHub voor meerdere statische bestanden met padvalidatie, checksumcontrole
  en herstelinformatie. De VPS is nog niet bijgewerkt; daarvoor is eenmalige
  root-installatie nodig. De huidige worker op de VPS ondersteunt nog alleen
  `index.html`; de codewijziging is nog niet op de server geïnstalleerd.
- **Test- en deploymentafspraak (28 november 2026):** iedere proefversie wordt
  op de bestaande Pensioen Ontdekt-server getest via de gewone site-URL. Er
  komt geen aparte testomgeving en een lokale ChatGPT-preview geldt niet als
  eindtest. De testdeployment is meteen de actieve siteversie; bij afkeuring
  wordt de vorige werkende GitHub-commit opnieuw uitgerold. Deployments worden
  aan commit-ID en checksum gekoppeld, zodat herstel controleerbaar is.


- De personageproef v1 blijft ongewijzigd en niet goedgekeurd. Mike meldde dat in v2 de neutrale mond niet zichtbaar was en dat de hele figuur verdween bij die stand. V3 scheidt huidpatch, mondlijn en basisfiguur; de oogmaskers zijn iets verkleind. De afzonderlijke lagen en ongewijzigde bronfiguren zijn statisch gecontroleerd. De oude lokale browsercontrole is niet uitgevoerd omdat file:// werd geblokkeerd; volgens de nieuwe afspraak moet V3 voor de eerstvolgende beoordeling op de server worden gedeployed. V3 is daarom nog onbeoordeeld en niet gepubliceerd: [preview v3](https://chatgpt.com/library?file_id=libfile_61fa1a81445081919a0b577c611a330a&account_id=personal). De technische bevinding en controle-uitkomst staan in [Werkwijze voor nieuwe geanimeerde personages](docs/werkwijze-nieuw-personage.md#follow-up-correctie-naar-personageproef-v3--27-november-2026).

- De [homepage](https://pensioen.myaiprojects.nl/) en de [Partnerpensioen-demo](https://pensioen.myaiprojects.nl/partnerpensioen-demo.html) staan live. Mike heeft de POC goedgekeurd. De demo heeft herstelde figuurselectie, stille titelkaarten en een losse afspeelroute voor Uitdiensttreding. De rest van de bestaande voice-over blijft hoorbaar.
- Het publieke formulier voor fictieve regelingen werkt. Regeling E stond al opgeslagen (45%, 1 maand). De live proef met 60% en 3 maanden leverde kandidaat F op. F blijft een concept.
- [Scheiden v9](https://pensioen.myaiprojects.nl/?onderwerp=scheiden) staat live via **Uit elkaar gaan**. De publieke versie gebruikt de door Mike goedgekeurde ElevenLabs-opname met Adam. De animatie staat op [scheiden-adam.html](https://pensioen.myaiprojects.nl/scheiden-adam.html). De blokken schuiven uit elkaar bij de zin over de uitbetaling. De goedgekeurde versie is gepubliceerd vanuit commit `176e17456656d0c042f6c3a71a28a477bca3dbc2`.
- De voice-overworker is op de VPS geïnstalleerd. De opname en homepagekoppeling zijn gepubliceerd en gecontroleerd. De publieke opname komt overeen met de goedgekeurde preview (SHA-256 `7dea0e5639135362583fc06185338c839542ab3264c4f16edafb24c1ae2c9090`).

- De homepageversie met **Mijn instellingen** staat live vanaf commit `d4b955a08b39eb08e241a29178798290b5e91546`. De publieke homepage komt byte voor byte overeen met de goedgekeurde proef (SHA-256 `e0f0115990f2eb69b2fdda8895d5def48b41d4152a237134d990b9c83a75c4f8`). Eén uitklapbaar blok **Mijn instellingen** bevat de drie kolommen. Tot **Bewaren** blijven de filmpjes vergrendeld en wisselen de portretten rechtsboven. Na **Bewaren** klapt het blok dicht, worden de filmpjes vrijgegeven en blijven de gekozen portretten staan.

## Open werk

### Afspraak voor de volgende filmpjes

Voorlopig bouwen we ieder onderwerp als een zelfstandig filmpje. Het hergebruik van losse inhoudelijke filmfragmenten als aparte filmpjes of onderdelen van andere filmpjes staat op pauze. Algemene animatiefuncties, personages, instellingen en passende losse assets kunnen wel opnieuw worden gebruikt.

### Voorgestelde volgorde

1. **Uit dienst gaan als zelfstandig filmpje.** Maak het onderwerp bereikbaar vanaf de homepage, geef de bewaarde regeling en gekozen personages door en deploy eerst een testversie naar de gewone site-URL.
2. **Inhoud en regelingsverschillen valideren.** Controleer het scenario op relevante uitzonderingen per regeling en pas tekst, animatie en voice-over aan voordat het filmpje wordt gepubliceerd.
3. **Persoonlijke relevantie bepalen.** Werk uit hoe partner, kinderen en afstand tot de pensioenleeftijd invloed hebben op welke onderwerpen worden aangeboden. Houd **Zeg ik liever niet** als geldige keuze.
4. **Een volgend onderwerp volledig uitwerken.** Kies na de uitdienstproef één onderwerp, bijvoorbeeld partner- en wezenpensioen, arbeidsongeschiktheid of scheiden, en maak daarvoor een zelfstandig filmpje.
5. **Selectie en regelinggegevens stapsgewijs parametriseren.** Leg vast welke onderwerpen per regeling en persoonlijke situatie beschikbaar zijn. Begin met versieerbare configuratie en automatische validatie; bouw pas verder uit als de eerste filmpjes die structuur nodig hebben.

## Documentatie

- [Werkwijze voor nieuwe geanimeerde personages](docs/werkwijze-nieuw-personage.md) is verplicht vóór iedere nieuwe personagegeneratie. Lees dit bestand en laad de daarin aangewezen goedgekeurde beeldreferenties; maak eerst één proef en test de echte animaties vóór verdere generatie of publicatie.
- [Ontwikkelworkflow](docs/ontwikkelworkflow-filmpjes.md) voor bouwen, servertesten, voice-over, uitrol en herstel.
- [Technisch ontwerp](docs/technisch-ontwerp.md) voor configuratie, animaties, personages en de beoogde verwerking van reglementen.
- [Voorgaande projectstatus en proefhistorie](https://github.com/henkesmike/pensioen/blob/575d5fce80724e7f8fcbf36b3253b0c3901fd54a/PROJECT_STATUS.md) voor eerdere besluiten, proefbestanden en publicatiechecksums.
