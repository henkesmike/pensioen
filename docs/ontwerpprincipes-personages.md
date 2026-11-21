# Ontwerpprincipes – personages en personalisatie

Datum: 21 november 2026
Status: akkoord; uitbreiding uitgesteld tot na de pilot.

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

## Pilot
Gebruik uitsluitend de twee reeds goedgekeurde personageontwerpen. Houd bij de technische opbouw rekening met bovenstaande principes. Bouw nog geen aanvullende personages, selectie-interface of doelgroepfunctionaliteit. De exacte categorieën, uiterlijkvarianten en technische rig-uitwerking volgen iteratief.
