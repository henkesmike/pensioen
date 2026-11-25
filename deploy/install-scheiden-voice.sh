#!/usr/bin/env bash
set -euo pipefail

if [[ $EUID -ne 0 || ! ${1:-} =~ ^[0-9a-f]{40}$ ]]; then
  echo 'Gebruik als root: bash install-scheiden-voice.sh <volledige Git-commit>' >&2
  exit 1
fi
test -s /etc/pensioen-deploy/elevenlabs.env
test -s /etc/nginx/pensioen-preview.htpasswd
command -v ffmpeg >/dev/null
id pensioen-deploy >/dev/null
runuser -u pensioen-deploy -- test -w /var/www/pensioen
origin="https://raw.githubusercontent.com/henkesmike/pensioen/$1/deploy"
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT
for file in scheiden_voice.py scheiden-v9.html; do
  curl -fsS --max-time 30 "$origin/$file" -o "$stage/$file"
done
python3 -m py_compile "$stage/scheiden_voice.py"
install -d -m 0755 /usr/local/lib/pensioen-voice
install -m 0644 "$stage/scheiden_voice.py" "$stage/scheiden-v9.html" /usr/local/lib/pensioen-voice/
install -d -o pensioen-deploy -g pensioen-deploy -m 0700 /var/lib/pensioen-deploy/private/scheiden-adam
install -d -o pensioen-deploy -g www-data -m 2750 /var/lib/pensioen-deploy/previews/scheiden-adam
cat > /etc/systemd/system/pensioen-scheiden-voice.service <<'UNIT'
[Unit]
Description=Pensioen Ontdekt Scheiden voice-over
Wants=network-online.target
After=network-online.target
[Service]
Type=oneshot
User=pensioen-deploy
Group=pensioen-deploy
EnvironmentFile=/etc/pensioen-deploy/elevenlabs.env
ExecStart=/usr/bin/python3 /usr/local/lib/pensioen-voice/scheiden_voice.py
TimeoutStartSec=150
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
PrivateTmp=yes
ReadWritePaths=/var/lib/pensioen-deploy/private/scheiden-adam /var/lib/pensioen-deploy/previews/scheiden-adam /var/www/pensioen
UNIT
cat > /etc/systemd/system/pensioen-scheiden-voice.timer <<'UNIT'
[Unit]
Description=Check for approved Scheiden voice-over jobs
[Timer]
OnBootSec=30s
OnUnitInactiveSec=60s
[Install]
WantedBy=timers.target
UNIT
systemctl daemon-reload
systemctl enable --now pensioen-scheiden-voice.timer
systemctl is-active pensioen-scheiden-voice.timer
