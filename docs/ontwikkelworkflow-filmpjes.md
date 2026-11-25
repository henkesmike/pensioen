# Ontwikkelworkflow voor filmpjes

## Doel: van idee naar deployment met zo min mogelijk handwerk

De normale bediening loopt via ChatGPT en GitHub. Mike beschrijft het gewenste
resultaat in de chat; de assistent werkt op een GitHub-branch en voert de
beschikbare controles uit. Na eenmalige inrichting hoeft Mike geen code of
herhaalde Terminal-commando's te kopiëren.

1. **Idee en wijziging:** de assistent maakt of wijzigt code, JSON en documentatie
   op een aparte branch. Privé-audio, API-sleutels en andere geheimen blijven
   buiten de repository.
2. **Automatische controle:** de server bouwt vanaf de exacte commit, hergebruikt
   de audiocache en controleert de preview. Bij ontbrekende betaalde audio stopt
   de bouw voordat nieuwe API-kosten ontstaan; Mike beslist dan of die opname
   gemaakt mag worden.
3. **Privépreview:** een geslaagde build wordt een kandidaat-release met commit,
   versie en SHA-256. De server biedt die afgeschermd aan via een HTTPS-link.
   Mike hoeft de preview alleen in de browser te bekijken.
4. **Publicatie:** na akkoord in de chat publiceert de server precies die
   kandidaat. Publicatie gebruikt een beperkte, declaratieve opdracht met een
   toegestane bestemming en checksum; er worden geen shellcommando's uit GitHub
   uitgevoerd.
5. **Controle en herstel:** de server controleert de publieke URL en bewaart de
   vorige release voor terugzetten.

De eenmalige serverinrichting mag één gebundelde handeling vereisen. Daarna
zijn Terminal, handmatig installeren van hulpmiddelen en herhaald kopiëren van
commando's uitzonderingen voor storingen of beheer.

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


## OTAP op één VPS

Gebruik GitHub voor scenario's, regelingconfiguratie en code. Gebruik de bestaande VPS om releases te bouwen, privé te bekijken en te publiceren. De Mac is je werkplek en browser. Lokaal bouwen blijft mogelijk voor snelle experimenten. De gebruikelijke route loopt via een build op de VPS.

| Stap | Waar | Wat gebeurt er? |
|---|---|---|
| Ontwikkeling | GitHub-branch | Pas scenario's, fragmenten en regelingwaarden aan. Koppel elke bouw aan een concrete Git-commit. |
| Test | VPS, vóór de preview | Eén opdracht bouwt een release. Controleer het manifest, media, tijdcodes en de vier regelingvarianten. Bij een fout stopt de bouw en blijft de publieke versie beschikbaar. |
| Acceptatie | Privépreview op dezelfde VPS | Bekijk en beluister de geteste release via een afgeschermde URL. Gebruik in de eerste proef een preview op localhost met SSH-tunnel. De normale acceptatie is het bekijken van de gerenderde release. |
| Productie | Bestaande website | Na akkoord maakt één publicatieopdracht exact die release beschikbaar. Wijs de publieke route in één stap naar de nieuwe release en bewaar de vorige voor terugzetten. Controleer de publieke URL na publicatie. |

Bouw één keer en gebruik dezelfde bestanden voor acceptatie en productie. Een release krijgt een vaste versie en een checksum. Bewaar kandidaat-releases en bronmedia buiten de publieke webroot. De publicatieopdracht kopieert uitsluitend de geteste, te publiceren webbestanden naar een eigen release-directory. Tag of registreer de versie die actief is. De sleutel voor de spraakservice blijft op de VPS. De generator gebruikt bestaande audioblokken uit de cache en vraagt ontbrekende opnames op als de bouw ze nodig heeft.

Start met twee opdrachten: één voor bouwen en privé bekijken, één voor publiceren. Houd de publicatiestap expliciet. Als beide stappen betrouwbaar werken, kunnen ze achter een knop of een handmatig gestarte workflow komen. Test en Acceptatie delen in deze eerste opzet dezelfde VPS met gescheiden releasepaden.

## Geautomatiseerde uitrol vanaf GitHub

Gebruik GitHub als bedieningspunt en laat de VPS uitgaand ophalen. De assistent kan via GitHub wijzigingen klaarzetten en na akkoord de opdracht voor een specifieke release vastleggen. Een systemd-timer op de VPS leest die opdracht en voert een vast lokaal publicatiescript uit. Directe SSH-toegang vanuit de assistent of het delen van het rootwachtwoord is hiervoor overbodig.

- Gebruik een aparte servicegebruiker voor Pensioen Ontdekt, met schrijfbevoegdheid voor de eigen releasepaden. De andere websites en de Nginx-configuratie vallen buiten die bevoegdheid. Is de repository privé, gebruik dan een alleen-lezen deploy key voor deze repository. De privésleutel blijft op de VPS.
- Werk met één aangewezen uitrolbranch en een klein declaratief bestand. De eerste versie accepteert alleen een bestaande kandidaatversie en verwachte checksum, of de afgesproken statische homepage als beperkte test. Het bestand levert geen shellcommando's aan. Een normale commit op main start geen productie-uitrol.
- Een productieopdracht wijst naar een goedgekeurde kandidaat. De VPS controleert de bron en checksum, zet bestanden eerst klaar buiten de live versie en wisselt daarna de actieve versie in één stap. Dezelfde opdracht kan veilig opnieuw worden gelezen. Log resultaat en versie op de VPS. Gebruik terugzetten naar een eerdere versie als rollback.
- De homepageproef is op 23 november 2026 bijgesteld na feedback. De definitieve versie behoudt de oorspronkelijke indeling en drie onderwerpblokken, maar verwijdert de regelingkeuze en de aparte animatiepagina. De actieve links **Overlijden**, **Partnerpensioen** en **Mijn partner** gaan rechtstreeks naar het filmpje. De VPS publiceerde de exacte commit en checksum uit `uitrol-productie`; live controle bevestigde de drie bestemmingen en dat de oude onderdelen weg zijn. Dit verliep zonder Terminal-commando's van Mike. Zie [de actuele projectstatus](../PROJECT_STATUS.md).
- De automatische homepage-uitrol ondersteunt alleen `index.html`. Voor generator- en demo-updates zijn de privépreview en releasebestemming nog uit te breiden. De publieke en private audio blijven voldoen aan de bestaande publicatieafspraken.
- Eenmalige inrichting vereist toegang op de VPS. Bundel die in één installatiecommando. Normale publicaties verlopen daarna vanuit GitHub, na akkoord op de release. Directe SSH blijft beschikbaar voor beheer en probleemoplossing.

### Voortgang tijdens elke uitrol

Geef vooraf aan welke stappen deze uitrol heeft en hoeveel het er zijn. Meld na elke stap het nummer, het resultaat, wat nog openstaat en de eerstvolgende stap. Bijvoorbeeld: “Stap 3 van 5 afgerond. De privépreview is akkoord. Volgende stap: de goedgekeurde versie publiceren.” Meld een blokkade bij de betreffende stap. Zet een stap pas op afgerond nadat het resultaat is gecontroleerd.

Gebruik als standaard: 1. wijziging klaarzetten, 2. bouwen en testen, 3. acceptatie, 4. publiceren, 5. publiek controleren. Vermeld per stap of de assistent die uitvoert of dat de gebruiker iets moet doen en waar. Kleine wijzigingen kunnen dezelfde stappen kort doorlopen.

Voor de huidige demo is de zichtbare kop **Partnerpensioen**. De vermelding voor de bestaande ElevenLabs-opname blijft in de browsertitel.

### Smoke test vóór acceptatie

Bij stap 2 controleert de maker het exacte bestand of de URL die de gebruiker krijgt. Open de versie in een echte browser via dezelfde route als de gebruiker. Probeer de belangrijkste knoppen en selecties en controleer steeds het zichtbare resultaat. Bij de partnerpensioendemo omvat dit persoonlijke keuzes wijzigen, **Naar het filmpje**, een andere regeling kiezen, afspelen starten en teruggaan met **Wijzig situatie**. Controleer ook op JavaScript-fouten. Herhaal de getroffen route na elke reparatie.

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

## Lokale HTML-preview opleveren

Gebruik voor een zelfstandige proefanimatie zoals Scheiden dezelfde opleverroute als voor versie 4:

1. Maak één zelfstandig HTML-bestand met alle benodigde CSS, JavaScript en afbeeldingen ingebed. Geef het bestand een versienummer, bijvoorbeeld `scheiden-proefanimatie-v5.html`.
2. Plaats en test het bestand in de lokale chatwerkmap. Controleer dat de beoogde animatie, afspeelknoppen en het terugspoelen werken.
3. Sla dezelfde versie duurzaam op in ChatGPT en controleer of het opslaan is gelukt.
4. Geef in het antwoord één directe bestandslink met het werkelijke absolute pad, bijvoorbeeld `[scheiden-proefanimatie-v5.html](sandbox:/werkelijke/chatwerkmap/scheiden-proefanimatie-v5.html)`. Zo kan Mike het HTML-bestand op dezelfde manier openen als de vorige proef. Een GitHub-bronlink is geen vervanging voor deze opleverroute.

Ontbreekt de lokale chatwerkmap, bewaar de exacte versie dan op de beschikbare duurzame projectlocatie en meld dat de directe preview nog niet beschikbaar is. Zodra er weer een werkmap beschikbaar is, haal dezelfde versie op, controleer het bestand en geef de directe bestandslink. Deze route vereist geen publieke deployment.

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

De pilot is voorbereid in GitHub. Installatie, de eerste API-aanroep en het afspelen op de VPS moeten nog worden bevestigd.

## Homepage installeren en herstellen

De bestaande timer leest `deploy/productie.json` op `uitrol-productie` en controleert ongeveer elke minuut. Een commit op `main` activeert geen release. De productieopdracht bevat de volledige commit-ID en SHA-256 van de exacte bytes van `index.html`.

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
