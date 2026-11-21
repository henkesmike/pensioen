# Pensioen Ontdekt — missie en einddoel

## Missie

Pensioen Ontdekt helpt deelnemers begrijpen wat hun pensioenregeling voor hen betekent, bijvoorbeeld als zij uit dienst gaan, arbeidsongeschikt worden of overlijden. De website toont per regeling begrijpelijke, interactieve informatiefilmpjes die inhoudelijk aansluiten op het pensioenreglement. Dezelfde uitleg en animatiefragmenten kunnen terugkomen bij meerdere regelingen en gebeurtenissen.

## Van pensioenreglement naar website

1. **Parameters definiëren.** Een apart analyseproject vergelijkt een aantal pensioenreglementen en stelt een vaste set parameters vast die voor de informatiefilmpjes nodig is. Per parameter worden betekenis, gegevenstype en toegestane waarden beschreven. De set kan per versie worden uitgebreid.
2. **Parameters afleiden.** Een aparte tool buiten Pensioen Ontdekt leest het volledige reglement en stelt met behulp van AI de parameterwaarden voor. De tool levert per waarde een verwijzing naar het reglement en markeert twijfelgevallen voor menselijke beoordeling.
3. **Beoordelen en uploaden.** Een beoordelaar controleert en corrigeert het voorstel. Via de beheerfunctie **Regelingparameters uploaden** importeert een beheerder de beoordeelde set. De applicatie valideert het formaat en de waarden en slaat de set met reglementsversie en ingangsdatum op in de database.
4. **Filmpjes en audio voorbereiden.** De backend bepaalt welke filmpjes en fragmenten voor de regeling van toepassing zijn. Per gekozen fragment vult de backend de gesproken tekst in en zoekt een passende bestaande opname met tijdcodes. Alleen als de ingevulde tekst voor dat fragment en de gekozen stem nog geen passende opname heeft, is nieuwe audio nodig. Een wijziging in een parameter die alleen beeld of selectie beïnvloedt, vraagt op zichzelf geen nieuwe voice-over.
5. **Regeling beschikbaar maken.** Na validatie en voorbereiding verschijnt de regeling als keuze op de website. Een beheerder kan vooraf controleren welke filmpjes en voice-overs bij de regeling horen.
6. **Uitleg per regeling samenstellen.** Parameters kunnen bepalen welke inhoud een filmpje toont, welk alternatief filmpje verschijnt of dat de website voor een onderwerp geen filmpje toont. Binnen een filmpje kunnen dezelfde korte fragmenten worden hergebruikt. Zo kan het fragment over partnerpensioen na uitdiensttreding ook op de pagina Uitdiensttreding worden gebruikt.
7. **Selectieregels gestructureerd opslaan.** Leg per regel vast voor welk onderwerp of welke gebeurtenis de regel geldt, welke voorwaarde wordt getoetst en welk filmpje of welke actie daarbij hoort. De opslag kan in een database of in versiebeheerbare configuratie. Onderstaande structuur is een voorbeeld.

| Onderwerp | Parameter | Voorwaarde | Uitkomst |
|---|---|---|---|
| Arbeidsongeschiktheid | Arbeidsongeschiktheidspensioen | Ja | Toon filmpje XYZ |
| Arbeidsongeschiktheid | Arbeidsongeschiktheidspensioen | Nee | Toon geen filmpje |
| Arbeidsongeschiktheid | Arbeidsongeschiktheidspensioen | Onbekend | Laat de beheerder dit beoordelen |

## Aandachtspunten voor het ontwerp

- **Houd versies herleidbaar.** Leg bij een gepubliceerde regelingversie vast welke bron, beoordeelde parameters en selectieregels daarvoor zijn gebruikt. Zo kan een gewijzigde regeling eerst worden voorbereid terwijl de bestaande uitleg beschikbaar blijft.
- **Hergebruik op basis van de gesproken tekst.** Dezelfde waarde kan in een andere zin voorkomen. Een opname is herbruikbaar als de volledige uitgesproken tekst van het fragment en de gekozen stem overeenkomen. Een wisseling van filmpje kan ook audio vereisen als het gekozen filmpje bestaande gesproken tekst gebruikt waarvoor nog geen opname beschikbaar is.
- **Voer het iteratief in.** Begin met de fictieve partnerpensioenregeling en één variatie, zodat de keten van parameter tot beeld en audio klein blijft. Breid daarna uit naar andere onderwerpen en regelingen.

## Wanneer is het einddoel bereikt?

Een beheerder kan een nieuwe of gewijzigde regeling toevoegen via upload van beoordeelde parameters, zonder codewijziging voor regelingen die binnen de ondersteunde parameters, selectieregels en beschikbare scenario's passen. De website toont de juiste uitleg, hergebruikt passende fragmenten en audio, en laat onderwerpen zonder toepasselijk filmpje weg.
