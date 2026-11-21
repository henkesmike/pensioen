# Pensioen Ontdekt — missie en einddoel

## Missie

Pensioen Ontdekt helpt deelnemers begrijpen wat hun pensioenregeling voor hen betekent, bijvoorbeeld als zij uit dienst gaan, arbeidsongeschikt worden of overlijden. De website toont per regeling begrijpelijke, interactieve informatiefilmpjes die inhoudelijk aansluiten op het pensioenreglement. Dezelfde uitleg en animatiefragmenten kunnen terugkomen bij meerdere regelingen en gebeurtenissen.

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

## Aandachtspunten voor het ontwerp

- **Houd versies herleidbaar.** Leg bij een gepubliceerde regelingversie vast welke bron, beoordeelde parameters en selectieregels daarvoor zijn gebruikt. Zo kan een gewijzigde regeling eerst worden voorbereid terwijl de bestaande uitleg beschikbaar blijft.
- **Hergebruik op basis van de gesproken tekst.** Dezelfde waarde kan in een andere zin voorkomen. Een opname is herbruikbaar als de volledige uitgesproken tekst van het audioblok en de gekozen stem overeenkomen. Een wisseling van filmpje kan ook audio vereisen als het gekozen filmpje bestaande gesproken tekst gebruikt waarvoor nog geen opname beschikbaar is.
- **Voer het iteratief in.** Begin met de fictieve partnerpensioenregeling en één variatie, zodat de keten van parameter tot beeld en audio klein blijft. Breid daarna uit naar andere onderwerpen en regelingen.

## Voice-over per zin variëren

Gebruik standaard de hele zin als dynamisch audioblok. Daarmee kan de stem het getal natuurlijk uitspreken met de klemtoon en intonatie van de zin. Aaneengesloten vaste zinnen mogen één audioblok vormen. Als een overgang hoorbaar onnatuurlijk blijft, neem dan een kort blok van meerdere samenhangende zinnen op.

Voorbeeld met tien zinnen en een percentage in zin 5:

| Audioblok | Inhoud | Verwerking bij een nieuw percentage |
|---|---|---|
| Vaste intro | Zinnen 1 tot en met 4 | Hergebruik |
| Variabele zin | Je partner ontvangt dertig, veertig of vijftig procent van je pensioengevend salaris, met precies één percentage per opname | Hergebruik de opname voor de ingevulde zin en stem, of genereer alleen die zin als de opname ontbreekt |
| Vaste afsluiting | Zinnen 6 tot en met 10 | Hergebruik |

De backend bepaalt dit automatisch na upload. Hij haalt de bestaande audioblokken op en stuurt alleen de tekst van ontbrekende blokken naar de tekst-naar-spraak-API. Vervolgens voegt hij de opnames in scriptvolgorde samen op natuurlijke pauzes. Voor ondertiteling en animatie telt hij bij de lokale tijdcodes van elk blok de werkelijke duur van alle voorgaande blokken en tussenpauzes op. Daardoor blijft de synchronisatie kloppen als de variant langer of korter duurt.

Een audiovisueel fragment zoals **Na uitdiensttreding** kan uit meerdere audioblokken bestaan. Het blijft als zelfstandig fragment bruikbaar op verschillende pagina's.

## Wanneer is het einddoel bereikt?

Een beheerder kan een nieuwe of gewijzigde regeling toevoegen via upload van beoordeelde parameters, zonder codewijziging voor regelingen die binnen de ondersteunde parameters, selectieregels en beschikbare scenario's passen. De website toont de juiste uitleg, hergebruikt passende fragmenten en audio, en laat onderwerpen zonder toepasselijk filmpje weg.
