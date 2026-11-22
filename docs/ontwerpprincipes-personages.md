# Ontwerpprincipes – personages en personalisatie

Datum: 21 november 2026
Status: bewegingsproef goedgekeurd op 22 november 2026.

## Doel
Animaties laten aansluiten bij verschillende doelgroepen zonder afzonderlijke films of programmacode per doelgroep te onderhouden.

## Beoogde varianten
- Drie leeftijdscategorieën: jong, middelbare leeftijd, ouder. Exacte grenzen nog te bepalen.
- Twee of drie uiterlijkvarianten; bij drie varianten en twee geslachten zijn er 18 basispersonages.
- Vier relatiecombinaties, in volgorde deelnemer/partner: man/vrouw, vrouw/man, man/man, vrouw/vrouw.
- Rollen zijn onafhankelijk van het gekozen personage.

## Architectuur
- Scheid personagebibliotheek, animatiebibliotheek, pensioenparameters en voice-over.
- Gebruik een gemeenschappelijke rig (beweegbare onderdelen, gewrichten en ankerpunten) met een consistent bewegingscontract voor alle personages.
- Programmeer scènes en bewegingen op rollen (deelnemer, partner), niet op specifieke personages of geslacht.
- Gebruik neutrale voice-overtermen zoals ‘jij’ en ‘je partner’.
- Combineer personages en bewegingen dynamisch; voorkom aparte animaties per combinatie.
- Laat eventuele toekomstige personalisatie berusten op vrijwillige keuze van de bezoeker; leid etniciteit of relatievorm niet af uit persoonsgegevens.

## Goedgekeurde basisbeweging

Gebruik voor alle personages dezelfde rustige ademhaling op 70% (cyclus 3,7 seconden) en hetzelfde knipperpatroon met de sluitduur op 270%. De cyclus van 8 seconden bevat twee enkele knippers en één dubbele. Gebruik bij twee personages een faseverschil zodat ze niet synchroon knipperen. De positie en tint van de oogleden worden per illustratie ingesteld. De standaardbeweging bestaat uit ademhalen en knipperen.

## Uitdrukkingen

Elk personage krijgt een glimlachende en een neutrale variant. Geef beide afbeeldingen dezelfde uitsnede, schaal en ankerpunten. Wissel van uitdrukking wanneer het scenario daarom vraagt. Controleer bij de eerste integratie visueel of een wissel zonder verspringing oogt.

De [generatie-instructie](generatie-instructie-personages.md) bevat de herbruikbare prompts, meetpunten en controles per personage.
