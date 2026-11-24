# Pensioen ontdekt — projectstatus
Bijgewerkt: 2026-11-24

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
- De proef voor variërende regelingwaarden en gesproken tekst in fase 3 is geslaagd. Zie de eerste proef hieronder.
- De goedkeuring geldt voor de privétestversie van fase 2. Definitief script, stemkeuze en publicatie staan nog open.

## Eerstvolgende iteratie
De OTAP-opzet op één VPS is op 22 november door de gebruiker goedgekeurd.

De [ontwikkelworkflow voor filmpjes](docs/ontwikkelworkflow-filmpjes.md) beschrijft OTAP op de bestaande VPS: één release bouwen en testen, afgeschermd accepteren en dezelfde release na akkoord publiceren. De eerstvolgende proef gebruikt het bestaande filmpje met A, B, C en D. Fragmenthergebruik en database volgen na de deploymentproef.

Op 22 november werkte de privépreview van fase3-v1 op de VPS via een SSH-tunnel. De gebruiker bevestigde de werking op zijn Mac. De gebruiker bevestigde daarna ook de [publieke demo](https://pensioen.myaiprojects.nl/partnerpensioen-demo.html) met echte audio. Het geteste bestand kreeg voor de niet-commerciële publicatie een ElevenLabs-vermelding in de titel. De link ‘Bekijk de demo’ op de Partnerpensioen-pagina staat in GitHub. De koppeling is via de automatische GitHub-uitrol op de VPS gepubliceerd. De prototypekeuzelijst is uit de hoofdpagina verwijderd; de keuze A–D staat in het filmpje.

De [geautomatiseerde uitrol vanaf GitHub](docs/ontwikkelworkflow-filmpjes.md#geautomatiseerde-uitrol-vanaf-github) via branch `uitrol-productie` is getest. De VPS haalt de gewenste `index.html` op aan de hand van commit en checksum, publiceert die automatisch en bewaart de vorige homepage. Deze route is gebruikt en de live homepage is gecontroleerd. De route ondersteunt nu alleen `index.html`; build en uitrol van filmpjes volgen later.

## Homepage aangepast: actieve onderwerpen openen direct het filmpje (23 november 2026)

Na de eerste proef is de oorspronkelijke homepage-indeling teruggezet. De drie onderwerpblokken en de actieve onderwerpen zijn behouden; alleen de regelingkeuze en de aparte animatiepagina zijn verwijderd. De actieve links **Overlijden**, **Partnerpensioen** en **Mijn partner** openen nu rechtstreeks `/partnerpensioen-demo.html`. De regelingkeuze A–D en de animatie blijven in het filmpje zelf.

De definitieve homepage is automatisch gepubliceerd via branch `uitrol-productie`, vanaf commit `7293c961d7116982b38d0b7aaeea1b803ff9f1d3`, met checksum `35dd9816b498207852ccac2659a3b2ca48cdb1170cae8ba5205c9802d1fcb9d2`. De live browsercontrole bevestigde de oorspronkelijke indeling, het ontbreken van de oude regelingkeuze en animatiepagina, en de drie directe filmkoppelingen.

## Eerste proef fase 3
- De [proef met vier regelingen](https://github.com/henkesmike/pensioen/tree/fase-3-vier-regelingen/poc/v4) combineert A (40%, 3 maanden), B (40%, 6 maanden), C (50%, 3 maanden) en D (50%, 6 maanden).
- De backend knipt de originele opname op in drie vaste blokken en twee variabele zinnen. De vier combinaties delen twee percentagezinnen en twee duurzinnen. De bestaande audio bevat 40% en 3 maanden.
- De HTTP-proef verifieerde twee automatische aanroepen, voor 50% en 6 maanden, en nul bij herhaling. Keuzelijst, audiobron, beeldlabels, ondertiteling en herberekende tijdcodes zijn technisch gecontroleerd. De proef gebruikt een lokale test-API met testtonen voor de twee nieuwe zinnen.
- De echte ElevenLabs-proef slaagde op de VPS nadat de generator een afrondingsverschil van minder dan één milliseconde in de tijdcodes kon verwerken. De gebruiker opende de uitvoer op zijn Mac en bevestigde dat de POC werkt. Dit was een privéproef buiten de live site. De automatische start na regeling-upload blijft onderdeel van het eindontwerp.

## Overdracht 22 november 2026

- De [publieke Partnerpensioen-demo](https://pensioen.myaiprojects.nl/partnerpensioen-demo.html) is bijgewerkt na gebruikersacceptatie. De homepage verwijst naar deze demo. De gebruiker heeft het bestand op de VPS gepubliceerd met een herstelkopie van de vorige versie. De publieke controle gaf dezelfde SHA-256 als het geaccepteerde bestand: `fa80f185429e26d791e5a720269190465f068876658adabef0e3e3a9c99faca8`.
- De selectie biedt drie huidtinten en vier koppelcombinaties. Bij twee personen van hetzelfde geslacht verschijnt een andere figuur als partner. Regeling A–D wordt afzonderlijk in het filmpje gekozen.
- Zes vernieuwde personages gebruiken per figuur gemeten oogleden. Alleen het mondgebied wijzigt bij de wissel naar neutraal. Gedeelde beweging: ademen op 70% en knipperen met sluitduur op 270%, met twee enkele knippers en één dubbele per acht seconden.
- De programmatest controleerde de twaalf combinaties, vier regelingkeuzes en terugknop. De gebruiker accepteerde de testversie. De publieke nacontrole verifieerde de bestandsinhoud via checksum. De aparte wenkbrauw- en hoofdproef dient als voorbereiding voor later.
- Volgende inhoudelijke stap: maak **Na uitdiensttreding** herbruikbaar als zelfstandig fragment. De automatische uitrol ondersteunt nu alleen de homepage. Voor uitrol van demo-updates zonder Terminal kan die worden uitgebreid naar het specifieke demobestand.

## Documentatie animatietechniek (23 november 2026)

De [technische opzet van animaties en afbeeldingen](docs/technische-opzet-animaties.md) beschrijft per beweging en attribuut welke extra afbeelding of grafische laag nodig is, hoe de beweging werkt, de huidige implementatiestatus en de grenzen van de 2D-opzet. Alleen documentatie toegevoegd; geen code of publieke demo gewijzigd.

## Architectuurafspraak JSON (23 november 2026)

Besloten om regelingparameters, personagegegevens en animatie-instellingen in gestructureerde JSON te beheren, met generieke code, stabiele ID's, validatie en een centrale inleeslaag. Een database is voorlopig niet nodig; de gegevensstructuur moet latere migratie mogelijk maken. Zie [architectuur JSON-configuratie](docs/architectuur-json-configuratie.md).

Een eerste implementatie voor de privéproef met vier regelingen staat op [branch implement-json-config](https://github.com/henkesmike/pensioen/tree/implement-json-config/poc/v4). De technische proef is in de assistentomgeving geslaagd met lokale testaudio. De generator en JSON-configuratie zijn nog niet op de VPS geïnstalleerd en de live demo is niet gewijzigd.

## Werkwijze van idee tot deployment (23 november 2026)

De gebruiker wil vanuit idee naar een complete deployment met zo min mogelijk eigen handelingen en zonder herhaald code- of commandokopiëren. Eerst wordt de volledige, veilige route ontworpen en vastgelegd; daarna volgt de implementatie. Zie [ontwikkelworkflow voor filmpjes](docs/ontwikkelworkflow-filmpjes.md#doel-van-idee-naar-deployment-met-zo-min-mogelijk-handwerk).

De beoogde normale route is: wijziging via chat op een aparte GitHub-branch, automatische build en controles op de VPS, een afgeschermde preview-link, akkoord in de chat, daarna publicatie van exact dezelfde kandidaat met checksum en herstelmogelijkheid. Terminalhandelingen horen alleen nodig te zijn bij de eenmalige inrichting of bij storing/beheer.

De huidige automatische uitrol ondersteunt alleen `index.html`; de generator en Partnerpensioen-demo hebben nog geen volledige build-preview-publicatieroute. Tijdens het uitwerken van die werkwijze zijn geen server- of live wijzigingen uitgevoerd.

## Personages
De bewegingsproef is goedgekeurd. [De ontwerpprincipes](docs/ontwerpprincipes-personages.md#goedgekeurde-basisbeweging) leggen de gedeelde instellingen vast. De vier aanvullende personages krijgen ieder een glimlachende en neutrale variant.

## Publicatie
De oorspronkelijke privé-POC en bronopnames blijven privé. De A–D-demo is als afzonderlijke niet-commerciële publicatie beschikbaar met de ElevenLabs-vermelding in de browsertitel. De zichtbare kop is **Partnerpensioen**. De gebruiker heeft deze correctie op de live demo gecontroleerd. De generator staat in GitHub. Sleutels blijven buiten de repository en de webroot.


## Beheerrechten deployment (23 november 2026)

Afgesproken is dat de deploymentvoorziening volledige beheerrechten krijgt voor de
projectomgeving van `pensioen.myaiprojects.nl`: de volledige websiteboom (pagina's,
mappen en assets), projectbronnen, gegenereerde previews en releases, publicatie en
rollback. De rechten gelden ook voor nieuwe bestanden en submappen, niet alleen voor
`index.html`.

De bevoegdheid blijft beperkt tot de afgebakende projectpaden. Andere subdomeinen en
serverbrede instellingen zoals Nginx, DNS, TLS, firewall en besturingssysteem vallen
buiten de normale projectservice. De service krijgt hiervoor geen algemene rootrechten.
Na eenmalige inrichting volgt het normale proces via chat/GitHub, automatische build
en controles, privépreview, expliciet akkoord en publicatie van exact dezelfde release.
Op 23 november is de eerste eenmalige serverinrichting uitgevoerd. De bestaande servicegebruiker `pensioen-deploy` mag schrijven in `/var/www/pensioen` en de eigen projectmappen onder `/var/lib/pensioen-deploy`; de timer is actief. De publieke homepage gaf HTTP 200. De projectgebruiker kan de Pensioen-site schrijven, terwijl `/var/www/puzzle` buiten bereik blijft. Deze stap wijzigde geen website-inhoud of Nginx. De site-agent is op 23 november geïnstalleerd vanaf branch
[`deployment-json-config`](https://github.com/henkesmike/pensioen/tree/deployment-json-config).
De eenmalige root-installatie voegde een Basic Auth-previewlocatie toe aan alleen de
Pensioen-vhost; de projectservice heeft geen Nginx-beheer. De timer bouwde de JSON-generator offline en bood de kandidaat beveiligd aan.
Na expliciet akkoord van Mike is exact die kandidaat gepubliceerd als
`partnerpensioen-demo.html`. Het publieke statusbestand meldt `published` met
dezelfde checksum als de goedgekeurde preview:
`529a752a80b8df06e945eaaaa8fd6fc07ab4e26a6b9fe5d928f656e9e815d591`.
De vorige demo is als herstelkopie bewaard. De eerste versie publiceert alleen de
Partnerpensioen-demo; bredere releasebestemmingen kunnen daarna worden toegevoegd.
De oude homepage-uitrol voor `index.html` blijft daarnaast actief.


## Publieke invoer voor testregelingen (23 november 2026)

De publieke beheerfunctie is voorbereid op branch `publieke-regelingbeheer`. Iedere bezoeker kan uitsluitend een percentage partnerpensioen (1–100%) en voorlopige dekkingsduur (1–120 maanden) invoeren. De functie maakt automatisch een regelingcode en naam, past de gesproken tekst aan, vraagt alleen ontbrekende zinsdelen op bij ElevenLabs en bewaart de regeling pas na een geslaagde build.

De invoer is begrensd op maximaal twee nieuwe regelingen per dag, maximaal twee aanvragen per IP-adres per uur en vier nieuwe ElevenLabs-zinsopnamen per dag. Een kandidaatvideo krijgt een unieke link. De aanvraag publiceert niets automatisch; productie blijft achter expliciet akkoord van Mike. API-sleutel, bronopname en audiocache blijven op de server.

De eenmalige VPS-installatie is op 23 november uitgevoerd. De beheer-API draait lokaal achter Nginx en de publieke API-route antwoordt. De homepage is daarna uitgerold via `uitrol-productie` vanaf commit `0f12d31b23ea7a9b35b659c7efd06ed886535261`, checksum `680397f371908bc30c4687c0e8ee6c295af3eeeb202d943d05efd7ed813b657e`. De live browsercontrole toont de twee velden met grenzen 1–120 maanden en 1–100%; de bestaande homepagekaarten en videolinks zijn behouden. De eerste live proefaanvraag met 60% en 3 maanden is succesvol verwerkt als fictieve regeling F; de gegenereerde kandidaat toont de juiste waarde en bevat afspeelbare audio. In de aanvullende servergegevens stond regeling E (45%, 1 maand) al vóór die proef; de herkomst daarvan is niet vast te stellen via de site. Kandidaat F blijft een concept en is niet live gepubliceerd.

## Herstel figuurselectie (24 november 2026)

De eerder goedgekeurde selectie is in de JSON-generator hersteld op [branch `herstel-figuurselectie`](https://github.com/henkesmike/pensioen/tree/herstel-figuurselectie). De bezoeker kiest uit drie huidtinten en vier koppels. Bij man–man en vrouw–vrouw toont de animatie twee verschillende figuren. Via **Wijzig situatie** kan de bezoeker terug naar de keuze en blijft de regeling geselecteerd. De zes bestaande illustraties, oogleden en neutrale mondvarianten zitten in `personages.json`.

De technische bouwproef A–D en de JavaScript-controle van alle twaalf combinaties zijn geslaagd. Via `uitrol-preview` is een afgeschermde VPS-build aangevraagd voor commit `2f524c1be4a07b694d5ac0c99748b56c8ee42325`. De previewroute vraagt om inloggen. De build en weergave op de VPS zijn nog niet bevestigd. De publieke demo geeft dezelfde checksum als de vorige gepubliceerde versie. Er is geen publicatieopdracht gegeven.

## Titelkaarten en Uitdiensttreding (24 november 2026)

Mike heeft twee gesproken titelkaarten goedgekeurd. Partnerpensioen opent met **Wat gebeurt er als je overlijdt terwijl je in dienst bent?** Het tweede deel opent met **Wat gebeurt er als je uit dienst gaat?**. Bij de overgang vervaagt de animatie in circa een halve seconde naar de titelkaart. Na de vraag vervaagt de kaart naar de nieuwe beginstand met beide personages en de werkgever zichtbaar. Uitdiensttreding kan zelfstandig worden geopend via de onderwerpkeuze of `?onderwerp=uitdiensttreding`; daarbij start hetzelfde deel met eigen audio en tijdcodes vanaf nul.

De implementatie staat op [branch `titelkaarten-uitdienst`](https://github.com/henkesmike/pensioen/tree/titelkaarten-uitdienst), met de herstelde figuurselectie als basis. De bouwproef A–D met een lokale spraakfixture en de JavaScript-controle van titelkaarten, fades, terugspoelen, beginstand en figuurselectie zijn geslaagd. De twee echte opnamen moeten nog via de bestaande ElevenLabs-bouwroute worden aangemaakt in de VPS-audiocache. De afgeschermde uitrol bouwt offline en kan die opnamen daarna hergebruiken. Er is nog geen nieuwe VPS-preview met echte voice-over bevestigd.
