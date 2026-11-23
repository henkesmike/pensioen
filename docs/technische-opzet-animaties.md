# Technische opzet van animaties en afbeeldingen

Datum: 23 november 2026
Status: documentatie van huidige POC en beproefde uitbreidingen; geen opdracht tot technische wijziging.

## 1. Kernprincipe

De website gebruikt geen vooraf gerenderde videofilms voor de personages, gebouwen en geldstromen. De browser toont stilstaande illustraties en tekent daar bewegingen overheen met HTML/SVG, CSS en JavaScript. De Python-generator bouwt het afspeelbare resultaat; de animaties worden gekoppeld aan de tijdpositie van de gesproken audio.

Scheid vier verantwoordelijkheden:
1. **Illustratie/object:** hoe een figuur, gebouw, geldsymbool of pijl eruitziet.
2. **Ankers en maskers:** waar ogen, mond, nek, voeten en bewegende delen liggen.
3. **Bewegingsfunctie:** bijvoorbeeld schalen, verplaatsen, roteren, vervagen of een ooglid sluiten.
4. **Scenario en tijdcodes:** wanneer een functie start en eindigt, welke rol/object betrokken is en welke regelingwaarden gelden.

Een animatie hoeft dus niet voor iedere combinatie van personage, partner en regeling opnieuw te worden gemaakt. Dezelfde functies kunnen op verschillende objecten worden toegepast.

## 2. Welke beweging vraagt welke afbeelding?

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

## 3. Details per personage

### Ademhalen
- Gebruik de bestaande basisafbeelding; schaal die heel licht in de tijd. Er is geen aparte 'ingeademde' afbeelding.
- De goedgekeurde instelling is 70% van de geteste bewegingssterkte en een cyclus van 3,7 seconden.
- Houd het voeten-/lichaamsanker stabiel zodat de figuur niet lijkt te springen of te zweven.

### Knipperen
- Gebruik dezelfde afbeelding met open ogen.
- Teken voor ieder oog een passende ooglidvorm over het oog; laat die kort sluiten en openen.
- Per figuur worden het oogmiddelpunt, de oogbreedte/-hoogte en de ooglidkleur gemeten. Zo blijven ogen volledig bedekt en ontstaan geen witte randen.
- Het goedgekeurde ritme: twee enkele knippers en één dubbele in acht seconden; sluitduur op 270% van de oorspronkelijke proef. Gebruik een faseverschil tussen twee personages.

### Mond en uitdrukking
- Bewaar de glimlachende basisillustratie.
- Genereer of bewerk een neutrale variant, maar gebruik daarvan **alleen het mondgebied** als overlay. Een volledige tweede personageafbeelding als geheel omschakelen is niet nodig en kan verspringen.
- Meng de mondpatch met een zachte rand; houd uitsnede, ogen, kleding en voeten exact gelijk.
- Controleer de combinatie van beide mondstanden met open en gesloten ogen.

### Hoofd en wenkbrauwen (voorbereid, nog niet live)
- Gebruik een recht vooruit kijkend hoofd, zichtbare nek, voldoende vrije huid boven de wenkbrauwen en geen storend haar over de ogen.
- Meet het nekdraaipunt, wenkbrauwgrenzen en het gebied waar vervorming vloeiend moet afnemen.
- Beproefde richtwaarden: circa ±4 graden hoofdkanteling en circa 1% van de hoofdhoogte als wenkbrauwlift; dit zijn geen verplichte productie-instellingen.
- Controleer beide uitersten en combinaties op witte/transparante randen, naden bij de nek en verschuiving van ogen of mond.
- De proef is geaccepteerd, maar deze bewegingen zijn nog niet in de publieke demo opgenomen.

## 4. Andere objecten en attributen

**Gebouwen:** één illustratie per gebouwtype (bijvoorbeeld werkgever, pensioenfonds) is voldoende voor tonen, verdwijnen, verschuiven of subtiel schalen. Voor een ander gebouwontwerp is uiteraard een ander basisbeeld nodig; niet voor iedere bewegingsfase.

**Geld:** één geldsymbool of vectorvorm kan meerdere keren worden getekend. De animatie past de positie langs een pad aan; een geldstroom hoeft niet als een reeks plaatjes opgeslagen te worden. Een geldbedrag of percentage is bij voorkeur afzonderlijke tekst, zodat de vier fictieve regelingen A–D dezelfde beelden kunnen gebruiken.

**Pijlen en lijnen:** SVG-geometrie kan worden getekend, verborgen, verschoven of in lengte veranderd. Ook daarvoor zijn geen beeldreeksen nodig.

**Personages:** dezelfde bibliotheek van figuren werkt voor de rollen deelnemer en partner. Rol, uiterlijk, geslacht en relatiecombinatie zijn onafhankelijk van de bewegingsfunctie.

## 5. Tijdsturing en gesproken uitleg

- De audio en de bijbehorende tijdcodes bepalen waar het scenario zich bevindt.
- Bij die tijdpositie berekent de animatie-engine de toestand van elk object (zichtbaar, positie, schaal, mondstand, enzovoort).
- Bij pauzeren of terugspoelen moet de toestand opnieuw uit de tijdpositie afleidbaar zijn; de animatie mag niet afhankelijk zijn van het toevallige aantal eerder afgespeelde frames.
- Pensioenparameters beïnvloeden bedragen, labels en de relevante voice-overzinnen. De proef met vier regelingen en hergebruik van vaste audiofragmenten is geslaagd.
- Voor de geplande herbruikbare fragmenten krijgt elk fragment een eigen tijdlijn vanaf nul, maar gebruikt het dezelfde objecten en bewegingsfuncties.

## 6. Onderhoudbaarheid en grenzen

**Voordelen:** weinig illustraties, geen afzonderlijke films per regeling, één gedeelde set bewegingsfuncties, snelle wijzigingen en relatief weinig opslag.

**Randvoorwaarden:** consistente afbeeldingsmaten en ankers; per personage gemeten ogen/mond/nek; transparante achtergrond zonder zichtbare naden; test op normale grootte én ingezoomd; behoud van scheiding tussen illustratie, animatie en scenario.

**Grenzen:** grote draaibewegingen, zijaanzichten, lopen, armgebaren en complexe 3D-bewegingen zijn niet automatisch met dezelfde vlakke illustratie overtuigend te maken. Daarvoor kunnen losse lichaamsdelen, aanvullende poses of een andere animatietechniek nodig zijn. De huidige opzet is bewust gericht op subtiele, onderhoudbare 2D-beweging.

## 7. Bronnen en relatie met andere documenten

- [Ontwerpprincipes personages](ontwerpprincipes-personages.md): gedeelde bewegingen, rollen, personalisatie en acceptatie.
- [Generatie-instructie personages](generatie-instructie-personages.md): illustratieprompts, mondpatch, oog- en nekankers en visuele controles.
- [Ontwikkelworkflow filmpjes](ontwikkelworkflow-filmpjes.md): bouwen, testen, accepteren en publiceren.
- [Projectstatus](../PROJECT_STATUS.md): wat daadwerkelijk getest, geaccepteerd en gepubliceerd is.

Dit document beschrijft zowel de gerealiseerde werking als de expliciet als 'proef', 'ontwerp' of 'algemeen principe' gemarkeerde mogelijkheden. Het introduceert geen nieuwe implementatie.
