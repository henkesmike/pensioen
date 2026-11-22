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

## Gemeten proefwaarden voor de man met het blauwe overshirt

Deze waarden horen bij het proefbeeld van 725 × 2170 px en vormen een voorbeeld voor het registreren van een nieuw figuur.

| Onderdeel | Middelpunt x, y | Halve breedte × halve hoogte |
|---|---|---|
| Oog links in beeld | 301, 283 | 37 × 33 px |
| Oog rechts in beeld | 425, 283 | 37 × 33 px |
| Mondmasker | 364, 402 | 95 × 57 px |

De mondblend is volledig dekkend tot 74% van de straal en vervaagt daarna. De gekozen ooglidvorm dekte het gedetecteerde oogwit in de bronpixels. Visuele beoordeling in het filmpje volgt bij integratie.
