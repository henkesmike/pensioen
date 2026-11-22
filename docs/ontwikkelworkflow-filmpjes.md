# Ontwikkelworkflow voor filmpjes

## OTAP op één VPS

Gebruik GitHub voor scenario's, regelingconfiguratie en code. Gebruik de bestaande VPS om releases te bouwen, privé te bekijken en te publiceren. De Mac is je werkplek en browser. Lokaal bouwen blijft mogelijk voor snelle experimenten. De gebruikelijke route loopt via een build op de VPS.

| Stap | Waar | Wat gebeurt er? |
|---|---|---|
| Ontwikkeling | GitHub-branch | Pas scenario's, fragmenten en regelingwaarden aan. Koppel elke bouw aan een concrete Git-commit. |
| Test | VPS, vóór de preview | Eén opdracht bouwt een release. Controleer het manifest, media, tijdcodes en de vier regelingvarianten. Bij een fout stopt de bouw en blijft de publieke versie beschikbaar. |
| Acceptatie | Privépreview op dezelfde VPS | Bekijk en beluister de geteste release via een afgeschermde URL. Gebruik in de eerste proef een preview op localhost met SSH-tunnel. De normale acceptatie is het bekijken van de gerenderde release. |
| Productie | Bestaande website | Na akkoord maakt één publicatieopdracht exact die release beschikbaar. Wijs de publieke route in één stap naar de nieuwe release en bewaar de vorige voor terugzetten. Controleer de publieke URL na publicatie. |

Bouw één keer en gebruik dezelfde bestanden voor acceptatie en productie. Een release krijgt een vaste versie en een checksum. Bewaar kandidaat-releases en bronmedia buiten de publieke webroot. De publicatieopdracht kopieert uitsluitend de geteste, te publiceren webbestanden naar een eigen release-directory. Tag of registreer de versie die actief is. De sleutel voor de spraakservice blijft op de VPS. De generator gebruikt bestaande audioblokken uit de cache en vraagt ontbrekende opnames op als de bouw ze nodig heeft.

Start met twee opdrachten: één voor bouwen en privé bekijken, één voor publiceren. Houd de publicatiestap expliciet. Als beide stappen betrouwbaar werken, kunnen ze achter een knop of een handmatig gestarte workflow komen. Test en Acceptatie delen in deze eerste opzet dezelfde VPS met gescheiden releasepaden.

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

Gebruik het bestaande partnerpensioenfilmpje met A, B, C en D. De HTML met echte audio is al op de VPS gebouwd. Registreer die als eerste kandidaat-release met een klein manifest en checksum, open hem via de privépreview en controleer alle vier varianten. Publiceer daarna dezelfde release onder een eigen URL, zodra de audio voor publiek gebruik is vrijgegeven. Controleer de URL en leg vast hoe de vorige versie kan worden teruggezet of hoe de route bij de eerste publicatie weer kan worden uitgezet.

Daarna doorlopen we de route opnieuw met een kleine wijziging vanuit Git. Dan toetsen we ook de automatische bouw en testen. Het opsplitsen van het filmpje en de database volgen na deze eerste deploymentproef.
