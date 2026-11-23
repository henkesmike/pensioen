# Automatische uitrol van de homepage

De productie-uitrol leest `deploy/productie.json` van branch
`uitrol-productie`. Op die branch staat alleen het uitrolverzoek.
Het JSON-bestand bevat `commit` (de volledige Git-commit-id) en
`sha256` (de checksum van de exacte bytes van `index.html` in die commit).
Een commit op main activeert geen release. De timer controleert ongeveer
elke minuut. Het toevoegen of wijzigen van het productie-verzoek is de
expliciete publicatiehandeling.

Eenmalige installatie op de bestaande VPS als root met
`bash install.sh VOLLEDIGE_COMMIT_ID`. Gebruik de commit-id waaruit ook
het installatiebestand is opgehaald. Het script bewaart de bestaande
homepage in `/var/lib/pensioen-deploy/index.voor-automatisering.html`
en koppelt de bestaande publieke homepage aan de door de service beheerde
kopie. Andere pagina's en de Nginx-configuratie wijzigen niet.

Controleer met `systemctl status pensioen-deploy.timer` en
`journalctl -u pensioen-deploy.service -n 30 --no-pager`.
De homepage-uitrol ondersteunt alleen `index.html`. Een eerdere
Git-versie activeer je met een nieuw verzoek dat naar die commit en checksum
verwijst. De direct voorafgaande kopie staat ook in
`/var/lib/pensioen-deploy/public/previous.html`. Stop bij handmatig herstel
eerst de timer en de service zodat het bestaande verzoek niet opnieuw wordt
uitgevoerd.

De repository is openbaar. De VPS haalt de bestanden via HTTPS op.
De uitrol heeft geen GitHub- of ElevenLabs-sleutel nodig.
