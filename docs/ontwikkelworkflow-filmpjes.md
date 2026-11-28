# Ontwikkelworkflow voor filmpjes

## Doel: van wijziging naar test op de server

De test verloopt op de bestaande Pensioen Ontdekt-server. Er komt geen aparte
testomgeving. Een testversie wordt op de site zelf geplaatst en in een echte
browser via de gewone HTTPS-route bekeken. Ook HTML-voorbeelden en animaties
worden op deze manier getest; een lokale ChatGPT-preview is geen eindtest.

1. **Wijziging vastleggen:** werk op een GitHub-branch en commit de wijziging.
   Koppel iedere testdeployment aan de volledige commit-ID. Privé-audio,
   API-sleutels en andere geheimen blijven buiten de repository.
2. **Bouwen en controleren:** de server bouwt vanaf die exacte commit en voert
   de beschikbare automatische controles uit. Bij een bouw- of smoke-testfout
   blijft de huidige versie actief.
3. **Testdeployment:** plaats de kandidaat op de bestaande server en open de
   normale site-URL. Dit is dezelfde omgeving die na acceptatie actief blijft;
   er is geen aparte testpublicatie of tweede server.
4. **Beoordelen:** Mike controleert de versie in de browser. Bij akkoord blijft
   deze versie staan. Er is geen tweede publicatiestap nodig.
5. **Herstellen:** bij afkeuring of een fout wordt de laatst werkende versie
   opnieuw uitgerold vanaf de bijbehorende GitHub-commit. Bewaar per deployment
   commit-ID, versie en checksum. Herschrijf of force-push de Git-geschiedenis
   niet; herstel door de gekozen eerdere versie opnieuw te deployen.

Testen gebeurt op de website zelf. Plan daarom vóór de deployment een
terugzetbare versie en houd de vorige deployment beschikbaar. Als een
bestemming nog geen deployment- en rollbackroute heeft, richt die route eerst
in voordat die bestemming op de server wordt getest.

Daarna loopt de normale bediening via ChatGPT en GitHub. Mike hoeft geen code
of herhaalde Terminal-commando's te kopiëren. Eenmalige serverinrichting mag
één gebundelde handeling vereisen; Terminal blijft beschikbaar voor beheer en
probleemoplossing.

### Afgesproken beheergrens voor de deployment

De deploymentvoorziening krijgt volledige beheerrechten binnen de projectomgeving van
`pensioen.myaiprojects.nl`. Dat omvat de volledige websiteboom met pagina's, mappen en
assets, plus de bijbehorende bronbestanden, gegenereerde previews, releasebestanden,
publicatie en rollback. De rechten moeten dus ook werken voor nieuwe bestanden en
submappen; ze zijn niet beperkt tot `index.html`.

De projectservice krijgt volledige schrijfrechten binnen haar afgebakende
projectpaden, zonder rootrechten voor de VPS. Ze krijgt geen toegang om Nginx,
DNS, TLS, firewall, besturingssysteem of andere subdomeinen te beheren. Voor een
beveiligde preview mag de eenmalige root-installatie alleen een previewlocatie
toevoegen aan de bestaande Nginx-vhost voor `pensioen.myaiprojects.nl`; die
wijziging geeft de projectservice zelf geen beheer over Nginx.

Na de eenmalige inrichting loopt het normale proces via chat en GitHub. De
site-agent haalt een expliciet previewverzoek op, bouwt offline op de VPS en biedt
de kandidaat beveiligd aan. Pas na akkoord publiceert de agent exact die kandidaat.
De eerste beveiligde preview is op 23 november aan Mike getoond en na zijn
expliciete akkoord gepubliceerd. Het publieke statusbestand bevestigde dat de
gepubliceerde checksum gelijk is aan die van de goedgekeurde preview. De vorige demo
is bewaard voor herstel. De bestaande homepage-uitrol voor `index.html` blijft actief;
de nieuwe route publiceert in deze eerste versie alleen de Partnerpensioen-demo.

### Eerste VPS-inrichting uitgevoerd (23 november 2026)

De bestaande servicegebruiker `pensioen-deploy` heeft schrijfrechten op
`/var/www/pensioen` en op de projectmappen onder
`/var/lib/pensioen-deploy` voor broncode, builds, previews, releases en backups.
De systemd-timer is actief. De publieke homepage gaf HTTP 200; de gebruiker
`pensioen-deploy` kan de Pensioen-site schrijven en `/var/www/puzzle` blijft
buiten bereik. De websitebestanden en Nginx-configuratie zijn bij deze stap niet
gewijzigd.

De eerste previewbuild is via de nieuwe agent uitgevoerd zonder ElevenLabs-
aanroepen. De kandidaat staat buiten de webroot en is bereikbaar via de
Basic Auth-previewlocatie. De productieversie is niet gewijzigd. Publicatie na akkoord
en automatische rollback zijn onderdeel van de agent; de eerste versie ondersteunt
als releasebestemming alleen `partnerpensioen-demo.html`.

### Twee soorten deployment

- **Generator en configuratie:** Python-code en JSON worden op de server gezet
  in een privé werkmap. Dit wijzigt op zichzelf de publieke website niet.
- **Gegenereerde demo:** de server bouwt een statisch HTML-bestand met audio en
  animaties. Dat bestand krijgt een privépreview en wordt na akkoord als
  afzonderlijke release gepubliceerd.

De preview en productie gebruiken hetzelfde gebouwde bestand. De bron-HTML,
cache en API-sleutel blijven op de server en buiten de publieke webroot.

### Huidige beperking

De bestaande GitHub-timer leest een declaratief verzoek en publiceert uitsluitend
`index.html`. Hij bouwt nog geen filmpjes en ondersteunt geen
`partnerpensioen-demo.html`-release. De volgende infrastructuurstap is daarom
een aparte, afgebakende route voor generatorbuilds, beveiligde previews en de
toegestane demo-bestemming. De bestaande homepage-uitrol blijft ongewijzigd.


## Testdeployment en rollback op één server

Gebruik GitHub als versiebeheer en de bestaande VPS als enige test- en
productieomgeving. Er is geen aparte testserver of aparte acceptatieomgeving.
De testdeployment vervangt tijdelijk de versie op de normale site-URL. Omdat
de site alleen voor Mike is bedoeld, kan de functionele beoordeling daar
plaatsvinden.

| Stap | Waar | Wat gebeurt er? |
|---|---|---|
| Wijziging | GitHub-branch | Leg code, configuratie en benodigde assets vast. Maak een commit die later afzonderlijk opnieuw kan worden uitgerold. |
| Bouwen | VPS | Bouw vanaf de volledige commit-ID. Voer de beschikbare automatische controles uit. Bij een fout blijft de huidige versie actief. |
| Test | Bestaande site-URL | Deploy de kandidaat naar de bestaande website en controleer hem in een echte browser via HTTPS. Gebruik deze serverdeployment ook voor animaties en losse HTML-voorbeelden. |
| Beoordeling | Chat en browser | Mike beoordeelt de draaiende versie. Bij akkoord blijft de deployment actief. |
| Herstel | GitHub en VPS | Bij afkeuring deploy je de laatst werkende GitHub-commit opnieuw. Controleer daarna de site-URL en noteer de herstelde commit en checksum. |

Elke deployment is herleidbaar tot één commit en checksum. Bewaar de vorige
werkende release voordat de actieve versie wordt vervangen. Herstel door de
eerdere commit of release opnieuw te deployen; verwijder of herschrijf geen
Git-geschiedenis. Zo blijft de nieuwe versie beschikbaar voor later herstel of
aanpassing.

Lokale previews mogen worden gebruikt als snelle tussencontrole, maar gelden
niet als test of oplevering. De eindtest vindt altijd plaats op de server. Een
releasebestemming mag pas worden getest nadat zowel deployment als terugzetten
naar een eerdere GitHub-versie voor die bestemming werkt.


## Geautomatiseerde uitrol vanaf GitHub

Gebruik GitHub als bedieningspunt en laat de VPS uitgaand ophalen. De assistent kan via GitHub wijzigingen klaarzetten en na akkoord de opdracht voor een specifieke release vastleggen. Een systemd-timer op de VPS leest die opdracht en voert een vast lokaal publicatiescript uit. Directe SSH-toegang vanuit de assistent of het delen van het rootwachtwoord is hiervoor overbodig.

- Gebruik een aparte servicegebruiker voor Pensioen Ontdekt, met schrijfbevoegdheid voor de eigen releasepaden. De andere websites en de Nginx-configuratie vallen buiten die bevoegdheid. Is de repository privé, gebruik dan een alleen-lezen deploy key voor deze repository. De privésleutel blijft op de VPS.
- Werk met één aangewezen uitrolbranch en een klein declaratief bestand. De eerste versie accepteert alleen een bestaande kandidaatversie en verwachte checksum, of de afgesproken statische homepage als beperkte test. Het bestand levert geen shellcommando's aan. Een normale commit op main start geen productie-uitrol.
- Een productieopdracht wijst naar een goedgekeurde kandidaat. De VPS controleert de bron en checksum, zet bestanden eerst klaar buiten de live versie en wisselt daarna de actieve versie in één stap. Dezelfde opdracht kan veilig opnieuw worden gelezen. Log resultaat en versie op de VPS. Gebruik terugzetten naar een eerdere versie als rollback.
- De eerste homepage-uitrol is op 23 november 2026 getest met een exacte commit en SHA-256. De actuele productieversie en het gedrag van de homepage staan in de [projectstatus](../PROJECT_STATUS.md).
- De automatische homepage-uitrol ondersteunt alleen `index.html`. Voor generator- en demo-updates zijn de privépreview en releasebestemming nog uit te breiden. De publieke en private audio blijven voldoen aan de bestaande publicatieafspraken.
- Eenmalige inrichting vereist toegang op de VPS. Bundel die in één installatiecommando. Normale publicaties verlopen daarna vanuit GitHub, na akkoord op de release. Directe SSH blijft beschikbaar voor beheer en probleemoplossing.

### Voortgang tijdens elke uitrol

Geef vooraf aan welke stappen deze uitrol heeft en hoeveel het er zijn. Meld na elke stap het nummer, het resultaat, wat nog openstaat en de eerstvolgende stap. Bijvoorbeeld: “Stap 3 van 5 afgerond. De privépreview is akkoord. Volgende stap: de goedgekeurde versie publiceren.” Meld een blokkade bij de betreffende stap. Zet een stap pas op afgerond nadat het resultaat is gecontroleerd.

Gebruik als standaard: 1. wijziging klaarzetten, 2. bouwen en testen, 3. acceptatie, 4. publiceren, 5. publiek controleren. Vermeld per stap of de assistent die uitvoert of dat de gebruiker iets moet doen en waar. Kleine wijzigingen kunnen dezelfde stappen kort doorlopen.

Voor de huidige demo is de zichtbare kop **Partnerpensioen**. De vermelding voor de bestaande ElevenLabs-opname blijft in de browsertitel.

### Smoke test vóór acceptatie

Bij stap 2 controleert de maker het exacte bestand of de URL die de gebruiker krijgt. Open de versie in een echte browser via dezelfde route als de gebruiker. Probeer de belangrijkste knoppen en selecties en controleer steeds het zichtbare resultaat. Bij de partnerpensioendemo omvat dit persoonlijke keuzes wijzigen, **Naar het filmpje**, een andere regeling kiezen, afspelen starten en teruggaan met **Wijzig situatie**. Voor de homepage controleer je dat de filmknoppen zichtbaar en vergrendeld zijn, dat **Mijn instellingen** de drie kolommen tegelijk opent en dat **Bewaren** pas na een regelingkeuze de filmpjes vrijgeeft. Controleer de wisselende portretten vóór het bewaren en de gekozen portretten erna. Open een beschikbaar filmpje en test de terugknop. Controleer ook op JavaScript-fouten. Herhaal de getroffen route na elke reparatie.

Noteer in de oplevering wat is gecontroleerd. Als de browserproef blokkeert, meld dan expliciet welke browsercontrole openstaat en presenteer een programmatest als zodanig. De inhoudelijke en functionele acceptatie doet de gebruiker zelf.

## Opslag voor de eerste versie

Voorkeur voor de pilot: SQLite voor de gegevens en koppelingen, met afbeeldingen en audiobestanden op schijf. Houd bewerkbare scenario's en het manifest in versiebeheer voor zover ze geen privémateriaal bevatten. Dezelfde gegevensstructuur kan aanvankelijk ook met een manifest en een map op schijf worden getest.

| Onderdeel | Wat wordt opgeslagen? |
|---|---|
| Filmpje | Identificatie, titel, versie en geordende verwijzingen naar fragmentversies. |
| Fragment | Identificatie, versie, eigen beginbeeld, scenario en regelingparameters. Het verwijst in afspeelvolgorde naar audioblokken. |
| Audioblok | Gesproken tekst, stem en instellingen. Een opname verwijst naar een audiobestand, speelduur en lokale tijdcodes. Dezelfde opname kan in meerdere fragmenten of regelingen terugkomen. |
| Pagina of gebeurtenis | Verwijzing naar een filmpje of zelfstandig fragment, eventueel afhankelijk van regelingparameters. |

Gebruik voor hergebruik de ingevulde tekst en steminstellingen als sleutel. Het scenario bepaalt de knip op een natuurlijke zinsgrens. De generator bewaart timing per blok en verschuift de starttijden op basis van de echte speelduur en tussenpauzes. Gebruik bij koppelingen expliciete versies, zodat een later gewijzigd fragment een bestaande publicatie niet onverwacht verandert.

De upload van een **filmpje** voegt scenario's en media toe. De upload van **regelingparameters** vult een bestaand scenario met andere waarden. Voor die tweede upload blijft gelden dat de backend zelf ontbrekende opnames opvraagt via de spraak-API en de opnames met tijdcodes opslaat. De sleutel staat op de server.

## Eerste iteratie

Gebruik het bestaande partnerpensioenfilmpje met A, B, C en D. De HTML met echte audio is al op de VPS gebouwd. Registreer die als eerste kandidaat-release met een klein manifest en checksum, open hem via de privépreview en controleer alle vier varianten. Publiceer daarna dezelfde release onder een eigen URL, zodra de audio voor publiek gebruik is vrijgegeven. Controleer de URL en leg vast hoe de vorige versie kan worden teruggezet of hoe de route bij de eerste publicatie weer kan worden uitgezet.

Daarna doorlopen we de route opnieuw met een kleine wijziging vanuit Git. Dan toetsen we ook de automatische bouw en testen. Het opsplitsen van het filmpje en de database volgen na deze eerste deploymentproef.


## Publieke invoer voor een testregeling

De homepage biedt een ingeklapt formulier met precies twee numerieke velden: voorlopige dekking in maanden (1–120) en dekkingspercentage partnerpensioen (1–100%). Er is geen vrije tekstinvoer. Iedere bezoeker kan een aanvraag indienen. De server maakt automatisch de regelingcode en fictieve naam, bouwt het script en de video opnieuw en doet alleen de ontbrekende ElevenLabs-aanroepen. De regeling wordt pas opgeslagen als de build slaagt.

De publieke route is begrensd tot maximaal twee nieuwe regelingen per dag, twee per IP-adres per uur en vier nieuwe ElevenLabs-zinsopnamen per dag. Mislukte verzoeken tellen mee voor de aanvraag/API-limiet; een duplicaat wordt vóór de limiet geweigerd. Kandidaten zijn te bekijken via een unieke, niet-geïndexeerde URL en verlopen na 30 dagen. De regelinggegevens blijven opgeslagen.

Een inzending is een concept, geen automatische productiepublicatie. Mike bekijkt de video en keurt de exacte checksum in de bestaande releaseflow goed voordat de demo live wijzigt. De API-sleutel staat alleen in een root-beheerd systemd environment-bestand; de service luistert uitsluitend op localhost. De eenmalige serverinstallatie beperkt Nginx-aanpassingen tot de Pensioen-vhost.

De implementatie staat op branch `publieke-regelingbeheer` en is live. De root-installatie voegde de lokale API-service en routes toe aan uitsluitend de Pensioen-vhost; de API-sleutel staat root-beheerd op de server. De homepage is via de bestaande uitrolbranch gepubliceerd vanaf commit `0f12d31b23ea7a9b35b659c7efd06ed886535261` met checksum `680397f371908bc30c4687c0e8ee6c295af3eeeb202d943d05efd7ed813b657e`. De browsercontrole bevestigde het formulier, de twee numerieke invoervelden en hun grenzen. De eerste live proefaanvraag (60%, 3 maanden) is geslaagd als regeling F; de kandidaat toont de aangepaste waarde en bevat afspeelbare audio. Regeling E (45%, 1 maand) stond al in de aanvullende servergegevens; de site geeft geen herkomst. Kandidaat F is niet live gepubliceerd.

## HTML-voorbeelden testen

Een zelfstandig proefbestand, bijvoorbeeld een animatie, wordt ook als
serverdeployment getest. Commit het bestand in GitHub, deploy de bijbehorende
versie naar de bestaande Pensioen Ontdekt-server en open de echte HTTPS-route
in de browser. De gebruiker beoordeelt die versie op de server.

Een lokaal bestand of een preview in de ChatGPT-omgeving is hooguit een
tussentijdse controle en vervangt de servertest niet. Bewaar de laatst werkende
GitHub-versie en de deploymentgegevens. Als de proef niet bevalt, deploy dan
de commit van de vorige werkende versie opnieuw en controleer dat de site weer
die versie toont.


## Voice-over ophalen via ElevenLabs

Gebruik voor Scheiden en nieuwe filmpjes die moeten aansluiten bij de oorspronkelijke Partnerpensioen-proef **Adam**, met voice-ID `pNInz6obpgDQGcFmaJgB` en model `eleven_multilingual_v2`. Gebruik de vaste ID uit de bestaande generator. Een gelijknamige stem, een automatisch gekozen voorleesstem of een vervangende voice-ID geldt niet als Adam. Meld het als de stem voor het account niet beschikbaar is.

Haal de opname met tijdcodes op via de bestaande VPS-bouwroute. Bewaar de API-sleutel op de VPS buiten de webroot en Git. Hergebruik alleen audio waarvan stem-ID, model, tekst en relevante spraakinstellingen overeenkomen. Gebruik de tijdcodes van de opname voor de scèneovergangen en controleer bij Scheiden dat de blokken uit elkaar schuiven bij de zin over de uitbetaling. Behoud het afgesproken rustige spreektempo.

### Pilot: voice-over aanmaken via GitHub

De pilot staat op [voiceover-scheiden](https://github.com/henkesmike/pensioen/tree/voiceover-scheiden), installatiecommit `ca500ebb0c094ff979431cc30b26d8a086eeb291`. De VPS-worker verwerkt alleen de goedgekeurde film Scheiden v9. De eerste bouwopdracht staat klaar. De worker gebruikt de bestaande VPS-sleutel en maakt één opname met Adam op snelheid 0,85. De tijdcodes sturen de animatie. De opname wordt gecachet. Na een onzekere API-uitkomst inspecteer je eerst `journalctl -u pensioen-scheiden-voice.service` en de cache voordat je een nieuwe poging vrijgeeft.

Eenmalig als root op de VPS, na controle van de installatiecommit:

```bash
curl -fsS https://raw.githubusercontent.com/henkesmike/pensioen/ca500ebb0c094ff979431cc30b26d8a086eeb291/deploy/install-scheiden-voice.sh -o /tmp/install-scheiden-voice.sh
bash /tmp/install-scheiden-voice.sh ca500ebb0c094ff979431cc30b26d8a086eeb291
```

De timer haalt `deploy/scheiden-request.json` op uit de pilotbranch. Bij `{"action":"build","film":"scheiden-v9"}` verschijnt het resultaat achter de bestaande previewbeveiliging op `/_preview/scheiden-adam/index.html`. De checksum staat op `/_preview/scheiden-adam/status.json`. Controleer de stem, het tempo en het uit elkaar schuiven bij de slotzin. Na akkoord gebruikt de publicatieopdracht `{"action":"publish","film":"scheiden-v9","sha256":"<goedgekeurde checksum>"}`. De worker publiceert exact die kandidaat naar `/scheiden-adam.html`. Koppel daarna **Uit elkaar gaan** via de bestaande homepage-uitrol aan die pagina en controleer de publieke weergave.

De worker is op de VPS geïnstalleerd. De goedgekeurde opname met Adam en de koppeling vanaf **Uit elkaar gaan** zijn gepubliceerd en gecontroleerd. De actuele release staat in de [projectstatus](../PROJECT_STATUS.md).

## Homepage installeren en herstellen

De bestaande timer leest `deploy/productie.json` op `uitrol-productie` en controleert ongeveer elke minuut. Een commit op `main` activeert geen release. De productieopdracht bevat de volledige commit-ID en SHA-256 van de exacte bytes van `index.html`. Houd het bestand onder de uitrollimiet van 256 KiB. Vergelijk na publicatie de SHA-256 van de publieke homepage met die van de goedgekeurde proef.

Voer de eenmalige installatie als root uit met `bash install.sh VOLLEDIGE_COMMIT_ID`. Gebruik de commit waaruit je [het installatiescript](../deploy/install.sh) hebt opgehaald. Het script bewaart de eerdere homepage in `/var/lib/pensioen-deploy/index.voor-automatisering.html` en koppelt de publieke homepage aan de beheerde kopie. De homepage-uitrol gebruikt HTTPS en vereist geen GitHub- of ElevenLabs-sleutel.

Controleer de timer met `systemctl status pensioen-deploy.timer` en de uitvoer met `journalctl -u pensioen-deploy.service -n 30 --no-pager`. Herstel een eerdere versie via een nieuw verzoek met de eerdere commit en checksum. De direct voorafgaande kopie staat in `/var/lib/pensioen-deploy/public/previous.html`. Stop bij handmatig herstel eerst de timer en de service, zodat de oude opdracht niet opnieuw wordt uitgevoerd.

## Personages genereren en controleren

### 1. Glimlachende basis maken

Gebruik een goedgekeurd personage als stijlreferentie. Vul de velden tussen blokhaken in.

> Maak een volledig 2D-cartoonpersonage in de stijl van de referentie. Het nieuwe personage heeft [uiterlijk, leeftijd en kleding]. Recht van voren, ogen open, hoofd recht, armen ontspannen naast het lichaam. Toon het hele figuur met schoenen. Gebruik een transparante achtergrond. Geef het figuur een vriendelijke, rustige glimlach. Maak de ogen iets kleiner en laat de oogcontouren vrij van haar en harde schaduw. Gebruik eenvoudige, iets kleinere wenkbrauwen met vrije huid erboven. Laat iets meer natuurlijke nek zien met een lage of open kraag. Houd de uitsnede en de ankerpunten van de referentie zo goed mogelijk aan.

### 2. Neutrale uitdrukking maken

Gebruik de goedgekeurde glimlachende afbeelding als invoer voor een lokale bewerking.

> Maak de lippen zacht gesloten met bijna horizontale mondhoeken. Wijzig alleen de mond en de directe omgeving. Laat ogen, hoofd, haar, kleding, houding, uitsnede en transparantie op dezelfde plek.

Plaats in de afspeelproef alleen het neutrale mondgebied over het basisbeeld, met een zachte rand. Daarmee blijven de rest van het beeld en de oogankers exact op hun plaats, ook als de beeldgenerator elders kleine verschillen heeft gemaakt.

### 3. Parameters en controle per personage

- Gebruik één canvas voor beide uitdrukkingen en meet de ankers op de uiteindelijke afbeelding. Noteer canvasbreedte en -hoogte, voetenanker, nekpunt, per oog het middelpunt, breedte en hoogte van het gesloten ooglid en de ooglidkleur. Noteer voor de mond het middelpunt, de afmetingen en de zachte rand van het masker. Coördinaten lopen vanaf linksboven.
- Gebruik gemeten maten voor de animatie. Promptmaten zijn richtwaarden. Herschaal coördinaten en afbeeldingen samen als de export kleiner wordt.
- Controleer beide mondstanden met open en gesloten ogen. Kijk of het oogwit volledig bedekt is en of de mondwissel geen lijn of verspringing geeft. Bekijk het figuur vergroot en op de gebruikelijke grootte in het filmpje.
- De gedeelde bewegingsinstellingen blijven zoals vastgelegd in de [ontwerpprincipes](technisch-ontwerp.md#goedgekeurde-basisbeweging).

### Voorwaarden voor latere beweging van wenkbrauwen en hoofd

- **Ogen en wenkbrauwen.** Beide ogen zijn volledig zichtbaar en vrij van haar en harde slagschaduw. De wenkbrauwen zijn compact en eenvoudig, met vrije huid erboven. Meet per oog de volledige contour, inclusief de ooghoeken. Leg per wenkbrauw het middelpunt en de boven-, onder- en zijgrenzen vast. Meet na export.
- **Hoofd en nek.** Recht van voren, zonder kanteling in het basisbeeld. Kies een natuurlijk iets langere, duidelijk zichtbare nek en een open of lage kraag. Houd haar, sieraden en kleding zo veel mogelijk vrij van de overgang tussen kaak en nek. Leg het draaipunt in de nek en de zone waarin de beweging naar de kraag vloeiend afneemt vast.
- **Uitdrukkingen en uitlijning.** Gebruik de glimlachende basis als bron voor de neutrale mond. Houd het canvas, de voeten, de hoofdstand en de ankers gelijk. Meng alleen het mondgebied met een zachte rand als de generator elders pixels heeft veranderd.
- **Acceptatie per figuur.** Test open en gesloten ogen, beide mondstanden, maximale subtiele wenkbrauwlift, hoofdkanteling naar links en rechts en de combinatie van beide. Controleer op volledig bedekt oogwit, witte of transparante randen en verspringing, zowel ingezoomd als op speelgrootte. Voor de beweging benutten we vloeiende vervorming van het beeld rond de wenkbrauwen en nek. Een generatieresultaat is pas gevalideerd als de gemeten ankers en visuele proef kloppen.
- Begin voor de technische proef rond ±4 graden hoofdkanteling en circa 1% van de hoofdhoogte aan wenkbrauwlift. Dit zijn instelbare testgrenzen. De twee bewegingen zijn voorbereid voor later gebruik.

### Gemeten proefwaarden voor de man met het blauwe overshirt

Deze waarden horen bij het proefbeeld van 725 × 2170 px en vormen een voorbeeld voor het registreren van een nieuw figuur.

| Onderdeel | Middelpunt x, y | Halve breedte × halve hoogte |
|---|---|---|
| Oog links in beeld | 301, 283 | 37 × 33 px |
| Oog rechts in beeld | 425, 283 | 37 × 33 px |
| Mondmasker | 364, 402 | 95 × 57 px |

De mondblend is volledig dekkend tot 74% van de straal en vervaagt daarna. De gekozen ooglidvorm dekte het gedetecteerde oogwit in de bronpixels. Visuele beoordeling in het filmpje volgt bij integratie.
