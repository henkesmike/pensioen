# Statische releases van Pensioen Ontdekt

Stap 3 van de technische verbeterfase levert een herstelpunt voor de vier
statische pagina’s en een lokaal getest releasecommando. De bestaande VPS
gebruikt nog de oude uitrolroute.

## Herstelpunt

`releases/basis-2026-11-28/` bevat de op 28 november opgehaalde publieke HTML,
met de ingesloten media. De vier bestanden zijn byte voor byte gecontroleerd
tegen de publieke site. De release omvat deze pagina’s.

| Bestand | Herkomst |
| --- | --- |
| `index.html` | Exact gelijk aan GitHub-commit `d4356f8d10c5794b07ad6afe1c4ae20d65c9f7cd` |
| `partnerpensioen-demo.html` | Publieke build, checksum gelijk aan `deploy/site-release.json` op commit `6c3a857` |
| `scheiden-adam.html` | Publieke build, checksum gelijk aan `deploy/scheiden-request.json` op commit `8ce81cc` |
| `personageproef-nieuwe-figuren-v3.html` | Exact gelijk aan `c07850b6c6cdfbb21219ba0cddee1cf1f47ff7d6` |

De homepage verwijst nog naar vastgepinde bestanden op
`raw.githubusercontent.com` voor portretten, filmpersonalisatie en
personage-overrides. De release bewaart de exacte homepage met die
verwijzingen. De beheer-API, jobs, private bronmedia, tijdcodes en audiocache
vallen buiten deze statische bundel. Herstel van de bundel zet alleen de
statische bestanden terug.

## Een release voorbereiden en controleren

Een bundel bevat `site/` met de volledige statische websiteboom en
`manifest.json` met versie 1 en per bestand `path`, `size` in bytes en
`sha256`. Leg bundel en manifest vast op één Git-commit. Laat bij grotere
bundels Git de binaire bestanden uit de precieze commit ophalen. Het
releasecommando leest en hasht bestanden in blokken. De limieten van de
oude manifestworker gelden voor die worker. De transportlimieten van
GitHub blijven gelden bij gebruik van gewone Git-blobs.

```sh
python3 deploy/static_release.py verify releases/basis-2026-11-28
python3 deploy/static_release.py verify-http releases/basis-2026-11-28 https://pensioen.myaiprojects.nl
```

## VPS-aansluiting en herstel

Controleer eerst op de VPS de actieve Nginx-root en de systemd-diensten die
statische bestanden schrijven. Controleer ook welke bestanden door de
huidige root worden geserveerd. Vul de releasebundel aan als de VPS
aanvullende publieke bestanden heeft. Controleer de bestaande routes voor
het beheer, jobstatus en kandidaten afzonderlijk. Bewaar de bestaande
configuratie en het actieve pad als terugval voor de eenmalige omschakeling.

Na aansluiting verwijst de statische Nginx-root binnen de bestaande
Pensioen-vhost naar `/var/lib/pensioen-deploy/static/current`. Laat de
beheer-API-routes en hun gegevens op hun bestaande locaties staan. Maak
`static/` schrijfbaar voor de bestaande projectservice en leesbaar voor
Nginx. Laat alleen de nieuwe uitrolroute de actieve statische release
selecteren. Leg de te gebruiken broncommit vast in de uitrolopdracht.
Voor aansluiting is VPS-beheer nodig. De scripts in deze branch installeren
of wijzigen zelf geen Nginx- of systemd-configuratie.

```sh
python3 deploy/static_release.py activate /var/lib/pensioen-deploy/static COMMIT_ID --bundle PAD_NAAR_BUNDEL
python3 deploy/static_release.py verify-http PAD_NAAR_BUNDEL https://pensioen.myaiprojects.nl
```

De eerste opdracht controleert de bestanden, maakt een release aan in
`releases/COMMIT_ID` en vervangt de `current`-symlink in één operatie.
Ze meldt de vorige doelmap. Bewaar die versie en controleer na afloop
dezelfde publieke URL’s en de beheerroute. Bij afkeuring selecteer je de
bewaarde versie met `activate /var/lib/pensioen-deploy/static VORIGE_COMMIT_ID`
en voer je de publieke controles opnieuw uit.
