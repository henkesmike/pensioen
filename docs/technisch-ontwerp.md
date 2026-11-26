# Technisch ontwerp Pensioen Ontdekt

Zie de [projectstatus](../PROJECT_STATUS.md) voor de actuele stand en de [ontwikkelworkflow](ontwikkelworkflow-filmpjes.md) voor uitvoeringsstappen. De verwerking van volledige pensioenreglementen hieronder beschrijft het beoogde ontwerp.

## Van pensioenreglement naar website

1. **Parameters definiëren.** Een apart analyseproject vergelijkt een aantal pensioenreglementen en stelt een vaste set parameters vast die voor de informatiefilmpjes nodig is. Per parameter worden betekenis, gegevenstype en toegestane waarden beschreven. De set kan per versie worden uitgebreid.
2. **Parameters afleiden.** Een aparte tool buiten Pensioen Ontdekt leest het volledige reglement en stelt met behulp van AI de parameterwaarden voor. De tool levert per waarde een verwijzing naar het reglement en markeert twijfelgevallen voor menselijke beoordeling.
3. **Beoordelen en uploaden.** Een beoordelaar controleert en corrigeert het voorstel. Via de beheerfunctie **Regelingparameters uploaden** importeert een beheerder de beoordeelde set. De applicatie valideert het formaat en de waarden en slaat de set met reglementsversie en ingangsdatum op in de database.
4. **Filmpjes en audio automatisch voorbereiden.** Na een geslaagde upload start de backend zelf de voorbereiding. De backend selecteert de toepasselijke filmpjes en fragmenten, vult per audioblok de gesproken tekst in en bepaalt automatisch of er een passende opname met tijdcodes bestaat voor die tekst en stem. Als die bestaat, hergebruikt de backend de opname. Als die ontbreekt, roept de backend zelf de tekst-naar-spraak-API aan, verwerkt het antwoord en slaat de nieuwe opname met tijdcodes op. De backend voegt de opnames in de gewenste volgorde samen. Een wijziging die alleen het beeld beïnvloedt vereist geen nieuwe opname zolang de gesproken tekst en stem gelijk blijven.
5. **Regeling beschikbaar maken.** Na validatie en voorbereiding verschijnt de regeling als keuze op de website. Een beheerder kan vooraf controleren welke filmpjes en voice-overs bij de regeling horen. Bij een API-fout meldt de backend de fout in het beheer en blijft de regelingversie in voorbereiding totdat de benodigde audio beschikbaar is.
6. **Uitleg per regeling samenstellen.** Parameters kunnen bepalen welke inhoud een filmpje toont, welk alternatief filmpje verschijnt of dat de website voor een onderwerp geen filmpje toont. Binnen een filmpje kunnen dezelfde korte fragmenten worden hergebruikt. Zo kan het fragment over partnerpensioen na uitdiensttreding ook op de pagina Uitdiensttreding worden gebruikt.
7. **Selectieregels gestructureerd opslaan.** Leg per regel vast voor welk onderwerp of welke gebeurtenis de regel geldt, welke voorwaarde wordt getoetst en welk filmpje of welke actie daarbij hoort. De opslag kan in een database of in versiebeheerbare configuratie. Onderstaande structuur is een voorbeeld.

| Onderwerp | Parameter | Voorwaarde | Uitkomst |
|---|---|---|---|
| Arbeidsongeschiktheid | Arbeidsongeschiktheidspensioen | Ja | Toon filmpje XYZ |
| Arbeidsongeschiktheid | Arbeidsongeschiktheidspensioen | Nee | Toon geen filmpje |
| Arbeidsongeschiktheid | Arbeidsongeschiktheidspensioen | Onbekend | Laat de beheerder dit beoordelen |

### Aandachtspunten voor het ontwerp

- **Houd versies herleidbaar.** Leg bij een gepubliceerde regelingversie vast welke bron, beoordeelde parameters en selectieregels daarvoor zijn gebruikt. Zo kan een gewijzigde regeling eerst worden voorbereid terwijl de bestaande uitleg beschikbaar blijft.
- **Hergebruik op basis van de gesproken tekst.** Dezelfde waarde kan in een andere zin voorkomen. Een opname is herbruikbaar als de volledige uitgesproken tekst van het audioblok en de gekozen stem overeenkomen. Een wisseling van filmpje kan ook audio vereisen als het gekozen filmpje bestaande gesproken tekst gebruikt waarvoor nog geen opname beschikbaar is.
- **Voer het iteratief in.** Begin met de fictieve partnerpensioenregeling en één variatie, zodat de keten van parameter tot beeld en audio klein blijft. Breid daarna uit naar andere onderwerpen en regelingen.

### Voice-over per zin variëren

Gebruik standaard de hele zin als dynamisch audioblok. Daarmee kan de stem het getal natuurlijk uitspreken met de klemtoon en intonatie van de zin. Aaneengesloten vaste zinnen mogen één audioblok vormen. Als een overgang hoorbaar onnatuurlijk blijft, neem dan een kort blok van meerdere samenhangende zinnen op.

Voorbeeld met tien zinnen en een percentage in zin 5:

| Audioblok | Inhoud | Verwerking bij een nieuw percentage |
|---|---|---|
| Vaste intro | Zinnen 1 tot en met 4 | Hergebruik |
| Variabele zin | Je partner ontvangt dertig, veertig of vijftig procent van je pensioengevend salaris, met precies één percentage per opname | Hergebruik de opname voor de ingevulde zin en stem, of genereer alleen die zin als de opname ontbreekt |
| Vaste afsluiting | Zinnen 6 tot en met 10 | Hergebruik |

De backend bepaalt dit automatisch na upload. Hij haalt de bestaande audioblokken op en stuurt alleen de tekst van ontbrekende blokken naar de tekst-naar-spraak-API. Vervolgens voegt hij de opnames in scriptvolgorde samen op natuurlijke pauzes. Voor ondertiteling en animatie telt hij bij de lokale tijdcodes van elk blok de werkelijke duur van alle voorgaande blokken en tussenpauzes op. Daardoor blijft de synchronisatie kloppen als de variant langer of korter duurt.

Een audiovisueel fragment zoals **Na uitdiensttreding** kan uit meerdere audioblokken bestaan. Het blijft als zelfstandig fragment bruikbaar op verschillende pagina's.

## Configuratie in JSON

Datum: 23 november 2026
Status: goedgekeurd ontwerpprincipe; implementatie volgt in een volgende technische iteratie.

### Besluit

Houd de programmacode zo generiek mogelijk. Bewaar duidelijke regelingafhankelijke, personage- en animatieparameters in gestructureerde JSON-bestanden, niet als verspreide vaste waarden in Python, HTML of JavaScript. Gebruik voorlopig **geen database**. Ontwerp de gegevens zodanig dat later een database als bron kan dienen zonder de animatie- en scenariologica opnieuw te ontwerpen.

Dit besluit verandert de bestaande demo niet onmiddellijk. De huidige code bevat nog ingebedde configuratie en proefwaarden; de migratie naar JSON is een afzonderlijke stap.

### Voorgestelde indeling

- `data/regelingen.json`: pensioenregelingen en hun parameters, zoals partnerpensioenpercentage en uitloopduur.
- `data/personages.json`: beschikbare personages, rollenonafhankelijke eigenschappen, verwijzingen naar illustraties, en gemeten ankers/maskers voor ogen, mond, nek en voeten.
- `data/animaties.json`: gedeelde bewegingstypen en instelbare standaarden, zoals ademhalingscyclus, intensiteit en knipperritme.

Bij groei kunnen deze bestanden per regeling of per personage worden opgesplitst zonder dat de semantiek verandert. Scenario's, fragmenten en voice-overselectie kunnen later hun eigen gegevensbestanden krijgen. Niet alles hoeft meteen geparametriseerd te worden: alleen betekenisvolle, stabiele instellingen, niet iedere tijdelijke programmeerconstante.

### Voorbeeldstructuur (illustratief, nog niet geïmplementeerd)

```json
{
  "schema_version": 1,
  "regelingen": [
    {
      "id": "regeling-a",
      "naam": "Fictieve regeling A",
      "partnerpensioen": {
        "percentage_pensioengevend_salaris": 40,
        "uitloop_maanden": 3
      }
    }
  ]
}
```

Voorbeeld voor een animatieconfiguratie:

```json
{
  "schema_version": 1,
  "animaties": {
    "ademhalen": {
      "cyclus_seconden": 3.7,
      "relatieve_intensiteit": 0.7
    }
  }
}
```

De voorbeelden zijn geen definitief schema. Definieer veldnamen en eenheden expliciet bij de implementatie. Scheid technische bewegingsinstellingen van pensioeninhoud.

### Regels voor onderhoudbaarheid en toekomstige database

1. **Stabiele ID's:** iedere regeling, elk personage en ieder herbruikbaar fragment krijgt een unieke, stabiele identificatie.
2. **Verwijzingen in plaats van duplicatie:** verwijs naar personages, illustraties, animatietypen en fragmenten met ID's of stabiele assetpaden.
3. **Vaste typen en eenheden:** onderscheid bijvoorbeeld percentagepunten (40), maanden (3), seconden (3.7) en fracties (0.7); documenteer de betekenis.
4. **Validatie:** controleer bij het inlezen verplichte velden, typen, toegestane waarden, unieke ID's en bestaande verwijzingen. Voeg bij voorkeur JSON Schema en automatische tests toe.
5. **Versiebeheer:** voeg `schema_version` toe en houd wijzigingen aan het gegevensformaat expliciet bij.
6. **Geen logica verstoppen in data:** JSON bevat waarden, keuzes en verwijzingen; berekeningen, animatiefuncties en validatieregels blijven in herbruikbare code.
7. **Één inleeslaag:** de applicatie krijgt gevalideerde configuratie via een centrale loader. Bij een latere databasewissel verandert primair deze gegevenslaag, niet de animatie-engine.
8. **Geen geheimen in JSON in GitHub of de webroot:** API-sleutels, tokens en privé-audio blijven buiten publieke bestanden.
9. **Geen onnodige complexiteit:** voorlopig geen database, beheerscherm, API of ingewikkelde abstractielaag bouwen uitsluitend voor mogelijke toekomstige behoeften.

### Migratiepad

1. Inventariseer de bestaande ingebedde parameters in Python/JavaScript/HTML.
2. Stel een minimaal JSON-schema op voor de eerstvolgende relevante wijziging.
3. Verplaats de betrokken waarden naar JSON en voeg validatie en tests toe.
4. Controleer dat alle vier fictieve regelingen en de personagecombinaties exact hetzelfde blijven werken.
5. Laat de applicatie daarna uitsluitend via een centrale inleeslaag configuratie ophalen.
6. Pas als een database functioneel nodig wordt, ontwerp tabellen/collecties en vervang de bron achter de inleeslaag. Complex geneste JSON hoeft niet letterlijk één-op-één een relationele tabel te worden.

### Afbakening

Deze afspraak is **documentatie en architectuurrichting**, geen bevestiging dat de JSON-bestanden al bestaan of dat de bestaande demo is omgebouwd. De publieke website en deployment blijven ongewijzigd.

## Personages en personalisatie

Datum: 21 november 2026
Status: bewegingsproef goedgekeurd op 22 november 2026.

### Doel
Animaties laten aansluiten bij verschillende doelgroepen zonder afzonderlijke films of programmacode per doelgroep te onderhouden.

### Beoogde varianten
- Drie leeftijdscategorieën: jong, middelbare leeftijd, ouder. Exacte grenzen nog te bepalen.
- Twee of drie uiterlijkvarianten; bij drie varianten en twee geslachten zijn er 18 basispersonages.
- Vier relatiecombinaties, in volgorde deelnemer/partner: man/vrouw, vrouw/man, man/man, vrouw/vrouw.
- Rollen zijn onafhankelijk van het gekozen personage.

### Architectuur
- Scheid personagebibliotheek, animatiebibliotheek, pensioenparameters en voice-over.
- Gebruik een gemeenschappelijke rig (beweegbare onderdelen, gewrichten en ankerpunten) met een consistent bewegingscontract voor alle personages.
- Programmeer scènes en bewegingen op rollen (deelnemer, partner), niet op specifieke personages of geslacht.
- Gebruik neutrale voice-overtermen zoals ‘jij’ en ‘je partner’.
- Combineer personages en bewegingen dynamisch; voorkom aparte animaties per combinatie.
- Laat eventuele toekomstige personalisatie berusten op vrijwillige keuze van de bezoeker; leid etniciteit of relatievorm niet af uit persoonsgegevens.

### Persoonlijke instellingen op de homepage

- **Mijn instellingen** opent één paneel met drie kolommen: regeling, persoonlijke situatie en personages. De regeling is verplicht. De persoonlijke situatie staat standaard op **Zeg ik liever niet** en de portretten op het eerste deelnemers- en partnerportret. Elk keuzewiel slaat het portret over dat in het andere wiel is geselecteerd.
- De beschikbare filmpjes blijven zichtbaar met een slotje tot **Bewaren**. De homepage gebruikt daarna de bevestigde keuzes voor de filmpjes. Conceptwijzigingen worden pas actief na opnieuw bewaren. De keuzes worden gedurende het huidige paginabezoek in de browser bijgehouden.
- De twee portretten rechtsboven wisselen vóór **Bewaren** om de beurt, met een fade-out en fade-in van elk één seconde. Bij een voorkeur voor minder beweging stopt de wisseling. Na **Bewaren** staan de gekozen portretten vast met de labels **Jij** en **Jouw partner**.
- De homepage haalt de gegevens voor de gepersonaliseerde filmpjes pas op wanneer de bezoeker een filmpje opent. Bij een laadfout opent de standaardversie met een melding. De homepage blijft daardoor binnen de uitrollimiet van 256 KiB.

### Goedgekeurde basisbeweging

Gebruik voor alle personages dezelfde rustige ademhaling op 70% (cyclus 3,7 seconden) en hetzelfde knipperpatroon met de sluitduur op 270%. De cyclus van 8 seconden bevat twee enkele knippers en één dubbele. Gebruik bij twee personages een faseverschil zodat ze niet synchroon knipperen. De positie en tint van de oogleden worden per illustratie ingesteld. De standaardbeweging bestaat uit ademhalen en knipperen.

### Uitdrukkingen

Elk personage krijgt een glimlachende en een neutrale variant. Geef beide afbeeldingen dezelfde uitsnede, schaal en ankerpunten. Wissel van uitdrukking wanneer het scenario daarom vraagt. Controleer bij de eerste integratie visueel of een wissel zonder verspringing oogt.

## Technische opzet van animaties

Datum: 23 november 2026
Status: documentatie van huidige POC en beproefde uitbreidingen; geen opdracht tot technische wijziging.

### 1. Kernprincipe

De website gebruikt geen vooraf gerenderde videofilms voor de personages, gebouwen en geldstromen. De browser toont stilstaande illustraties en tekent daar bewegingen overheen met HTML/SVG, CSS en JavaScript. De Python-generator bouwt het afspeelbare resultaat; de animaties worden gekoppeld aan de tijdpositie van de gesproken audio.

Scheid vier verantwoordelijkheden:
1. **Illustratie/object:** hoe een figuur, gebouw, geldsymbool of pijl eruitziet.
2. **Ankers en maskers:** waar ogen, mond, nek, voeten en bewegende delen liggen.
3. **Bewegingsfunctie:** bijvoorbeeld schalen, verplaatsen, roteren, vervagen of een ooglid sluiten.
4. **Scenario en tijdcodes:** wanneer een functie start en eindigt, welke rol/object betrokken is en welke regelingwaarden gelden.

Een animatie hoeft dus niet voor iedere combinatie van personage, partner en regeling opnieuw te worden gemaakt. Dezelfde functies kunnen op verschillende objecten worden toegepast.

### 2. Welke beweging vraagt welke afbeelding?

| Effect | Extra volledig plaatje nodig? | Extra grafisch onderdeel nodig? | Werking | Status |
|---|---|---|---|---|
| Ademhalen | Nee | Nee | Subtiele periodieke schaalverandering van bestaand lichaamsbeeld, met passend ankerpunt | Actief |
| Knipperen | Nee | Ja: getekende oogleden/maskers | Ooglid sluit over bestaande ogen en opent weer; oogpositie, vorm en kleur per personage gemeten | Actief |
| Glimlach naar neutraal | Nee | Ja: neutrale mondvariant | Alleen het mondgebied wordt met zachte maskerrand over de glimlachende basis gelegd | Actief |
| Hoofd kantelen | Nee | Niet noodzakelijk, wel een goed vervormingsgebied | Subtiele vervorming/rotatie rond nekpunt, met vloeiende aansluiting op nek en kraag | Afzonderlijke proef geslaagd, nog niet in publieke demo |
| Wenkbrauwen optrekken | Nee | Niet noodzakelijk, wel afgebakende wenkbrauwzone | Lokale verschuiving/vervorming rond wenkbrauwen met zachte overgang naar huid | Afzonderlijke proef geslaagd, nog niet in publieke demo |
| Personage verschijnen/verdwijnen | Nee | Nee | Transparantie (opacity) in de tijd veranderen | Actief |
| Object verplaatsen | Nee | Nee | Positie/transform van hetzelfde object aanpassen | Algemeen principe |
| Gebouw tonen/verbergen | Nee | Nee | Bestaande gebouwillustratie via opacity tonen of verbergen | Toegepast in scenario |
| Geld laten stromen | Niet per stap | Wel een basissymbool of vectorvorm | Hetzelfde geldsymbool hergebruiken en langs een traject verplaatsen; meerdere instanties kunnen tegelijk zichtbaar zijn | Toegepast concept; exacte vorm afhankelijk van scène |
| Geldbedrag of percentage wijzigen | Nee | Nee | Tekst/label dynamisch instellen vanuit regelingparameters | Beproefd in A–D-demo |
| Pijl/lijn animeren | Nee | Nee | SVG-lijn, zichtbaarheid, positie of lengte aanpassen | Geschikt herbruikbaar principe |
| Scèneovergang | Nee | Nee | Animatiebeeld naar zwart en terug laten vervagen | Ontworpen voor volgende iteratie, nog niet geïmplementeerd |

**Belangrijke nuance:** 'geen extra volledig plaatje' betekent niet dat iedere beweging met alleen één vlakke bitmap probleemloos werkt. Voor oogleden is aanvullende geometrie nodig; voor de mond is een tweede mondstand nodig. Bij hoofd en wenkbrauwen zijn zorgvuldig begrensde vervormingen nodig om geen lege/witte randen te tonen. Als een toekomstige beweging te groot wordt, kan het nodig zijn om lichaamsdelen in afzonderlijke lagen te tekenen. Dat is nu niet nodig voor de gekozen subtiele bewegingen.

### 3. Details per personage

#### Ademhalen
- Gebruik de bestaande basisafbeelding; schaal die heel licht in de tijd. Er is geen aparte 'ingeademde' afbeelding.
- De goedgekeurde instelling is 70% van de geteste bewegingssterkte en een cyclus van 3,7 seconden.
- Houd het voeten-/lichaamsanker stabiel zodat de figuur niet lijkt te springen of te zweven.

#### Knipperen
- Gebruik dezelfde afbeelding met open ogen.
- Teken voor ieder oog een passende ooglidvorm over het oog; laat die kort sluiten en openen.
- Per figuur worden het oogmiddelpunt, de oogbreedte/-hoogte en de ooglidkleur gemeten. Zo blijven ogen volledig bedekt en ontstaan geen witte randen.
- Het goedgekeurde ritme: twee enkele knippers en één dubbele in acht seconden; sluitduur op 270% van de oorspronkelijke proef. Gebruik een faseverschil tussen twee personages.

#### Mond en uitdrukking
- Bewaar de glimlachende basisillustratie.
- Genereer of bewerk een neutrale variant, maar gebruik daarvan **alleen het mondgebied** als overlay. Een volledige tweede personageafbeelding als geheel omschakelen is niet nodig en kan verspringen.
- Meng de mondpatch met een zachte rand; houd uitsnede, ogen, kleding en voeten exact gelijk.
- Controleer de combinatie van beide mondstanden met open en gesloten ogen.

#### Hoofd en wenkbrauwen (voorbereid, nog niet live)
- Gebruik een recht vooruit kijkend hoofd, zichtbare nek, voldoende vrije huid boven de wenkbrauwen en geen storend haar over de ogen.
- Meet het nekdraaipunt, wenkbrauwgrenzen en het gebied waar vervorming vloeiend moet afnemen.
- Beproefde richtwaarden: circa ±4 graden hoofdkanteling en circa 1% van de hoofdhoogte als wenkbrauwlift; dit zijn geen verplichte productie-instellingen.
- Controleer beide uitersten en combinaties op witte/transparante randen, naden bij de nek en verschuiving van ogen of mond.
- De proef is geaccepteerd, maar deze bewegingen zijn nog niet in de publieke demo opgenomen.

### 4. Andere objecten en attributen

**Gebouwen:** één illustratie per gebouwtype (bijvoorbeeld werkgever, pensioenfonds) is voldoende voor tonen, verdwijnen, verschuiven of subtiel schalen. Voor een ander gebouwontwerp is uiteraard een ander basisbeeld nodig; niet voor iedere bewegingsfase.

**Geld:** één geldsymbool of vectorvorm kan meerdere keren worden getekend. De animatie past de positie langs een pad aan; een geldstroom hoeft niet als een reeks plaatjes opgeslagen te worden. Een geldbedrag of percentage is bij voorkeur afzonderlijke tekst, zodat de vier fictieve regelingen A–D dezelfde beelden kunnen gebruiken.

**Pijlen en lijnen:** SVG-geometrie kan worden getekend, verborgen, verschoven of in lengte veranderd. Ook daarvoor zijn geen beeldreeksen nodig.

**Personages:** dezelfde bibliotheek van figuren werkt voor de rollen deelnemer en partner. Rol, uiterlijk, geslacht en relatiecombinatie zijn onafhankelijk van de bewegingsfunctie.

### 5. Tijdsturing en gesproken uitleg

- De audio en de bijbehorende tijdcodes bepalen waar het scenario zich bevindt.
- Bij die tijdpositie berekent de animatie-engine de toestand van elk object (zichtbaar, positie, schaal, mondstand, enzovoort).
- Bij pauzeren of terugspoelen moet de toestand opnieuw uit de tijdpositie afleidbaar zijn; de animatie mag niet afhankelijk zijn van het toevallige aantal eerder afgespeelde frames.
- Pensioenparameters beïnvloeden bedragen, labels en de relevante voice-overzinnen. De proef met vier regelingen en hergebruik van vaste audiofragmenten is geslaagd.
- Voor de geplande herbruikbare fragmenten krijgt elk fragment een eigen tijdlijn vanaf nul, maar gebruikt het dezelfde objecten en bewegingsfuncties.

### 6. Onderhoudbaarheid en grenzen

**Voordelen:** weinig illustraties, geen afzonderlijke films per regeling, één gedeelde set bewegingsfuncties, snelle wijzigingen en relatief weinig opslag.

**Randvoorwaarden:** consistente afbeeldingsmaten en ankers; per personage gemeten ogen/mond/nek; transparante achtergrond zonder zichtbare naden; test op normale grootte én ingezoomd; behoud van scheiding tussen illustratie, animatie en scenario.

**Grenzen:** grote draaibewegingen, zijaanzichten, lopen, armgebaren en complexe 3D-bewegingen zijn niet automatisch met dezelfde vlakke illustratie overtuigend te maken. Daarvoor kunnen losse lichaamsdelen, aanvullende poses of een andere animatietechniek nodig zijn. De huidige opzet is bewust gericht op subtiele, onderhoudbare 2D-beweging.
