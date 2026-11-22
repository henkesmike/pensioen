# Generatie-instructie voor 2D-personages

## 1. Glimlachende basis maken

Gebruik een goedgekeurd personage als stijlreferentie. Vul de velden tussen blokhaken in.

> Maak een volledig 2D-cartoonpersonage in de stijl van de referentie. Het nieuwe personage heeft [uiterlijk, leeftijd en kleding]. Recht van voren, ogen open, hoofd recht, armen ontspannen naast het lichaam. Toon het hele figuur met schoenen. Gebruik een transparante achtergrond. Geef het figuur een vriendelijke, rustige glimlach. Maak de ogen iets kleiner en laat de oogcontouren vrij van haar en harde schaduw. Gebruik eenvoudige, iets kleinere wenkbrauwen met vrije huid erboven. Laat iets meer natuurlijke nek zien met een lage of open kraag. Houd de uitsnede en de ankerpunten van de referentie zo goed mogelijk aan.

## 2. Neutrale uitdrukking maken

Gebruik de goedgekeurde glimlachende afbeelding als invoer voor een lokale bewerking.

> Maak de lippen zacht gesloten met bijna horizontale mondhoeken. Wijzig alleen de mond en de directe omgeving. Laat ogen, hoofd, haar, kleding, houding, uitsnede en transparantie op dezelfde plek.

Plaats in de afspeelproef alleen het neutrale mondgebied over het basisbeeld, met een zachte rand. Daarmee blijven de rest van het beeld en de oogankers exact op hun plaats, ook als de beeldgenerator elders kleine verschillen heeft gemaakt.

## 3. Parameters en controle per personage

- Gebruik één canvas voor beide uitdrukkingen en meet de ankers op de uiteindelijke afbeelding. Noteer canvasbreedte en -hoogte, voetenanker, nekpunt, per oog het middelpunt, breedte en hoogte van het gesloten ooglid en de ooglidkleur. Noteer voor de mond het middelpunt, de afmetingen en de zachte rand van het masker. Coördinaten lopen vanaf linksboven.
- Gebruik gemeten maten voor de animatie. Promptmaten zijn richtwaarden. Herschaal coördinaten en afbeeldingen samen als de export kleiner wordt.
- Controleer beide mondstanden met open en gesloten ogen. Kijk of het oogwit volledig bedekt is en of de mondwissel geen lijn of verspringing geeft. Bekijk het figuur vergroot en op de gebruikelijke grootte in het filmpje.
- De gedeelde bewegingsinstellingen blijven zoals vastgelegd in de [ontwerpprincipes](ontwerpprincipes-personages.md#goedgekeurde-basisbeweging).

## Voorwaarden voor latere beweging van wenkbrauwen en hoofd

- **Ogen en wenkbrauwen.** Beide ogen zijn volledig zichtbaar en vrij van haar en harde slagschaduw. De wenkbrauwen zijn compact en eenvoudig, met vrije huid erboven. Meet per oog de volledige contour, inclusief de ooghoeken. Leg per wenkbrauw het middelpunt en de boven-, onder- en zijgrenzen vast. Meet na export.
- **Hoofd en nek.** Recht van voren, zonder kanteling in het basisbeeld. Kies een natuurlijk iets langere, duidelijk zichtbare nek en een open of lage kraag. Houd haar, sieraden en kleding zo veel mogelijk vrij van de overgang tussen kaak en nek. Leg het draaipunt in de nek en de zone waarin de beweging naar de kraag vloeiend afneemt vast.
- **Uitdrukkingen en uitlijning.** Gebruik de glimlachende basis als bron voor de neutrale mond. Houd het canvas, de voeten, de hoofdstand en de ankers gelijk. Meng alleen het mondgebied met een zachte rand als de generator elders pixels heeft veranderd.
- **Acceptatie per figuur.** Test open en gesloten ogen, beide mondstanden, maximale subtiele wenkbrauwlift, hoofdkanteling naar links en rechts en de combinatie van beide. Controleer op volledig bedekt oogwit, witte of transparante randen en verspringing, zowel ingezoomd als op speelgrootte. Voor de beweging benutten we vloeiende vervorming van het beeld rond de wenkbrauwen en nek. Een generatieresultaat is pas gevalideerd als de gemeten ankers en visuele proef kloppen.
- Begin voor de technische proef rond ±4 graden hoofdkanteling en circa 1% van de hoofdhoogte aan wenkbrauwlift. Dit zijn instelbare testgrenzen. De twee bewegingen zijn voorbereid voor later gebruik.

## Gemeten proefwaarden voor de man met het blauwe overshirt

Deze waarden horen bij het proefbeeld van 725 × 2170 px en vormen een voorbeeld voor het registreren van een nieuw figuur.

| Onderdeel | Middelpunt x, y | Halve breedte × halve hoogte |
|---|---|---|
| Oog links in beeld | 301, 283 | 37 × 33 px |
| Oog rechts in beeld | 425, 283 | 37 × 33 px |
| Mondmasker | 364, 402 | 95 × 57 px |

De mondblend is volledig dekkend tot 74% van de straal en vervaagt daarna. De gekozen ooglidvorm dekte het gedetecteerde oogwit in de bronpixels. Visuele beoordeling in het filmpje volgt bij integratie.
