# Partnerpensioen v3 lokaal opnieuw opbouwen

Vereist Python 3.9 of hoger en het oorspronkelijke privébestand
`partnerpensioen-v3.html`. Voer vanaf de hoofdmap van de repository uit:

```sh
python3 poc/v3/build.py ~/Downloads/partnerpensioen-v3.html ~/Downloads/partnerpensioen-v3-fase2.html
```

Open het nieuwe HTML-bestand in de browser. De build gebruikt de ingesloten
voice-over, tijdcodes en drie afbeeldingen uit de oorspronkelijke proefversie.
De uitvoer bevat de privévoice-over en hoort buiten de repository en webroot.

- `scenario.json` bevat per gesproken regel de tekst en de wijzigingen die
  beginnen zodra die regel start. Een waarde is direct, een paar
  `[waarde, duur]` schrijft een lineaire overgang in seconden voor.
  De duur `"next"` loopt tot de volgende gesproken regel.
- `regeling.json` bevat de fictieve regeling. De build stopt als de ingevulde
  tekst afwijkt van de tekst die bij de bestaande voice-over hoort.
- `assets/scene.svg` bevat het decor en de plaatsing van de personages.
- `engine.js` gebruikt de audiotijd als klok voor scèneovergangen,
  ondertitels en beweging. Daardoor werkt ook terugspoelen.
