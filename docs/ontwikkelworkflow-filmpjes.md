# Ontwikkelworkflow voor filmpjes

## Van concept naar publicatie

1. **Lokaal maken en proberen.** Leg de volgorde van de fragmenten, het script, de gebruikte regelingparameters en de momenten voor beeld en ondertiteling vast. Bouw met dezelfde generator als in de proef en open de lokale preview. Controleer de regelingvarianten en speel herbruikbare fragmenten ook los af.
2. **Een geteste versie uploaden.** Maak een pakket met een manifest, de gewijzigde scenario's en bijbehorende media. Het manifest bevat vaste identificaties en versies, de volgorde van fragmenten en audioblokken, en verwijzingen naar de benodigde bestanden. Het pakket bevat de brononderdelen waarmee de server de uitleg kan opbouwen. Een losse HTML-preview is bedoeld om te bekijken.
3. **Privé importeren en controleren.** De backend controleert of alle verwijzingen, bestanden en tijdcodes geldig zijn. De import levert een conceptversie op die je op de server kunt bekijken. Bij een fout blijft de eerder beschikbare versie actief. Importeer hetzelfde pakket desgewenst opnieuw zonder dubbele versies of media te maken.
4. **Een versie activeren.** Na goedkeuring wijst de server de betreffende pagina of gebeurtenis naar de nieuwe versie. Bewaar de vorige versie zodat die weer geactiveerd kan worden. Voor de eerste proef volstaan een importcommando en een privépreview.

## Opslag voor de eerste versie

Voorkeur voor de pilot: SQLite voor de gegevens en koppelingen, met afbeeldingen en audiobestanden op schijf. Houd bewerkbare scenario's en het manifest in versiebeheer voor zover ze geen privémateriaal bevatten. Dezelfde gegevensstructuur kan aanvankelijk ook met een manifest en een map op schijf worden getest.

| Onderdeel | Wat wordt opgeslagen? |
|---|---|
| Filmpje | Identificatie, titel, versie en geordende verwijzingen naar fragmentversies. |
| Fragment | Identificatie, versie, eigen beginbeeld, scenario en regelingparameters. Het verwijst in afspeelvolgorde naar audioblokken. |
| Audioblok | Gesproken tekst, stem en instellingen. Een opname verwijst naar een audiobestand, speelduur en lokale tijdcodes. Dezelfde opname kan in meerdere fragmenten of regelingen terugkomen. |
| Pagina of gebeurtenis | Verwijzing naar een filmpje of zelfstandig fragment, eventueel afhankelijk van regelingparameters. |

Gebruik voor hergebruik de ingevulde tekst en steminstellingen als sleutel. Het scenario bepaalt de knip op een natuurlijke zinsgrens. De generator bewaart timing per blok en verschuift de starttijden op basis van de echte speelduur en tussenpauzes. Gebruik bij koppelingen expliciete versies, zodat een later gewijzigd fragment een bestaande publicatie niet onverwacht verandert.

De upload van een **filmpje** voegt scenario's en media toe. De upload van **regelingparameters** vult een bestaand scenario met andere waarden. Voor die tweede upload blijft gelden dat de backend zelf ontbrekende opnames opvraagt via de spraak-API en de opnames met tijdcodes opslaat. De sleutel staat op de server.

## Eerste iteratie

Gebruik het bestaande partnerpensioenfilmpje. Maak **Na uitdiensttreding** zelfstandig afspeelbaar en verwijs naar dezelfde fragmentversie vanuit de volledige uitleg en vanuit Uitdiensttreding. Maak daarna één importeerbaar pakket en toets de privépreview op de server met dezelfde fragmentversie. Begin met het bestaande beeld en de beschikbare audio. Stel een beheerinterface en de definitieve opslagkeuze uit tot de werkwijze met dit ene filmpje klopt.
