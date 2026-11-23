# Deployment voor Pensioen Ontdekt

## Bestaande homepage-uitrol

De bestaande route blijft werken via `deploy/productie.json` op branch
`uitrol-productie`. Die route publiceert alleen `index.html` vanuit de
aangewezen Git-commit.

## Eenmalige site-agent

`install_site_agent.sh <commit>` installeert de extra route op de bestaande VPS
als root. Gebruik de volledige commit-id van de branch waarop dit script staat.
De installatie:

- installeert de agent onder `/usr/local/lib/pensioen-deploy`;
- kopieert de privébron-HTML en de bestaande audiocache uit
  `/root/pensioen-poc` naar de afgeschermde projectmap;
- voegt alleen in de Pensioen-vhost een met Basic Auth beveiligde
  `/_preview/`-route toe;
- laat de service als `pensioen-deploy` draaien, met schrijfrechten binnen
  `/var/www/pensioen` en `/var/lib/pensioen-deploy`;
- behoudt de bestaande homepage-uitrol.

De installer toont een eenmalig previewwachtwoord als er nog geen wachtwoord is.
Bewaar het. De service krijgt geen rootrechten en kan geen andere website of
Nginx-configuratie aanpassen.

## Preview bouwen

Een expliciete opdracht op branch `uitrol-preview` start een offline build:

```json
{
  "commit": "<40-teken Git-commit-id>",
  "request_id": "preview-001"
}
```

Bestand: `deploy/preview.json`.

De agent haalt de genoemde bronbestanden op uit die commit en draait de generator
met `--offline`. Ontbreekt audio in de cache, dan stopt de build zonder een
ElevenLabs-aanroep. Na een geslaagde build verschijnt de preview onder
`https://pensioen.myaiprojects.nl/_preview/<commit>/partnerpensioen-demo.html`.
De agent publiceert alleen technische status, commit en SHA-256 in
`/deployment-status.json`; de preview zelf vereist Basic Auth.

## Publiceren na akkoord

Voor terugzetten naar de voorafgaande demo gebruikt dezelfde bestandsnaam
`deploy/site-release.json` de actie `rollback`. `candidate_commit` verwijst dan
naar de release waarvan de backup moet worden teruggezet en `sha256` bevat de
checksum van die opgeslagen backup. Ook terugzetten is daarmee expliciet en
controleerbaar.

Na akkoord op de preview kan een expliciete opdracht op branch
`uitrol-productie` dezelfde kandidaat publiceren:

```json
{
  "action": "publish",
  "candidate_commit": "<dezelfde 40-teken Git-commit-id>",
  "sha256": "<SHA-256 uit deployment-status.json>",
  "target": "partnerpensioen-demo.html"
}
```

Bestand: `deploy/site-release.json`.

De server controleert kandidaat, checksum en toegestane bestemming, bewaart de
vorige demo onder `/var/lib/pensioen-deploy/backups` en vervangt het bestand
atomair. De bestaande homepage-uitrol blijft onafhankelijk beschikbaar.

De eerste versie van deze extra route publiceert de gegenereerde
Partnerpensioen-demo. De projectservice heeft bredere schrijfrechten voor de
Pensioen-site, maar andere releasebestemmingen moeten expliciet aan de
publicatieregels worden toegevoegd.
