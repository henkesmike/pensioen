#!/usr/bin/env bash
set -euo pipefail

commit="${1:-}"
[[ "$commit" =~ ^[0-9a-f]{40}$ ]]
[[ "$(id -u)" == 0 ]]
[[ "$(hostname)" == myaiprojects-server ]]

service_user=pensioen-deploy
base=/var/lib/pensioen-deploy
lib=/usr/local/lib/pensioen-deploy
nginx_conf=/etc/nginx/sites-available/pensioen
key_file=/etc/pensioen-deploy/elevenlabs.env
api_unit=/etc/systemd/system/pensioen-regelingen-api.service

id "$service_user" >/dev/null
test -f "$nginx_conf"
test -d "$base/private/fase3"
test -f "$base/private/partnerpensioen-v3.html"
test -d "$base/source/repo"
test -f "$base/source/repo/.source-commit"
command -v nginx >/dev/null
command -v runuser >/dev/null

stamp=$(date -u +%Y%m%dT%H%M%SZ)
backup_dir="/root/pensioen-regelingen-install.$stamp"
install -d -m 0700 "$backup_dir"
cp -a "$nginx_conf" "$backup_dir/pensioen.nginx"
if [[ -f "$api_unit" ]]; then cp -a "$api_unit" "$backup_dir/pensioen-regelingen-api.service"; fi

tmp=$(mktemp -d)
success=0
rollback() {
  if [[ "$success" -eq 0 ]]; then
    systemctl disable --now pensioen-regelingen-api.service 2>/dev/null || true
    cp -a "$backup_dir/pensioen.nginx" "$nginx_conf" 2>/dev/null || true
    if [[ -f "$backup_dir/pensioen-regelingen-api.service" ]]; then
      cp -a "$backup_dir/pensioen-regelingen-api.service" "$api_unit" 2>/dev/null || true
    else
      rm -f "$api_unit"
    fi
    systemctl daemon-reload 2>/dev/null || true
    nginx -t 2>/dev/null && systemctl reload nginx 2>/dev/null || true
  fi
  rm -rf -- "$tmp"
}
trap rollback EXIT

curl --proto '=https' --fail --silent --show-error --max-time 30 \
  "https://raw.githubusercontent.com/henkesmike/pensioen/$commit/deploy/admin_api.py" \
  -o "$tmp/admin_api.py"
curl --proto '=https' --fail --silent --show-error --max-time 30 \
  "https://raw.githubusercontent.com/henkesmike/pensioen/$commit/deploy/site_agent.py" \
  -o "$tmp/site_agent.py"
/usr/bin/python3 -m py_compile "$tmp/admin_api.py" "$tmp/site_agent.py"

install -d -m 0755 -o root -g root "$lib"
install -m 0644 -o root -g root "$tmp/admin_api.py" "$lib/admin_api.py"
install -m 0644 -o root -g root "$tmp/site_agent.py" "$lib/site_agent.py"

# The service user must be able to create the shared build lock before source_for runs.
install -d -m 0750 -o "$service_user" -g "$service_user" "$base/admin" "$base/admin/jobs"

# Fetch and install the exact build source used by the feature branch.
runuser -u "$service_user" -- env PYTHONPATH="$lib" /usr/bin/python3 -c \
  'import sys, site_agent; site_agent.source_for(sys.argv[1])' "$commit"

if [[ ! -f "$key_file" ]]; then
  read -r -s -p 'Plak hier eenmalig de ElevenLabs API-sleutel (invoer blijft verborgen): ' api_key </dev/tty
  printf '\n'
  if [[ ${#api_key} -lt 20 || "$api_key" == *$'\n'* || "$api_key" == *$'\r'* ]]; then
    unset api_key
    echo 'De API-sleutel lijkt onvolledig; er is niets geïnstalleerd.' >&2
    exit 1
  fi
  install -d -m 0700 -o root -g root "$(dirname "$key_file")"
  printf 'ELEVENLABS_API_KEY=%s\n' "$api_key" > "$tmp/elevenlabs.env"
  unset api_key
  install -m 0600 -o root -g root "$tmp/elevenlabs.env" "$key_file"
fi
chown root:root "$key_file"
chmod 0600 "$key_file"

install -d -m 2750 -o "$service_user" -g www-data "$base/previews"
install -d -m 0750 -o "$service_user" -g "$service_user" "$base/candidates"
install -d -m 0700 -o "$service_user" -g "$service_user" "$base/private"
if [[ ! -f "$base/private/aanvullende-regelingen.json" ]]; then
  printf '{"schema_version":1,"regelingen":[]}\n' > "$tmp/aanvullende-regelingen.json"
  install -m 0600 -o "$service_user" -g "$service_user" \
    "$tmp/aanvullende-regelingen.json" "$base/private/aanvullende-regelingen.json"
fi

cat > "$tmp/pensioen-regelingen-api.service" <<'UNIT'
[Unit]
Description=Publieke invoer voor fictieve Pensioen Ontdekt-regelingen
After=network.target

[Service]
Type=simple
User=pensioen-deploy
Group=pensioen-deploy
WorkingDirectory=/usr/local/lib/pensioen-deploy
EnvironmentFile=/etc/pensioen-deploy/elevenlabs.env
Environment=PENSIOEN_SCHEME_DAILY_LIMIT=2
Environment=PENSIOEN_TTS_DAILY_LIMIT=4
Environment=PENSIOEN_IP_HOURLY_LIMIT=2
ExecStart=/usr/bin/python3 /usr/local/lib/pensioen-deploy/admin_api.py
Restart=on-failure
RestartSec=5
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
PrivateTmp=yes
UMask=0027
ReadWritePaths=/var/lib/pensioen-deploy/private /var/lib/pensioen-deploy/admin /var/lib/pensioen-deploy/previews /var/lib/pensioen-deploy/candidates
TimeoutStartSec=30

[Install]
WantedBy=multi-user.target
UNIT
install -m 0644 "$tmp/pensioen-regelingen-api.service" "$api_unit"

python3 - "$nginx_conf" <<'PY'
import os, sys, tempfile
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text()
locations = '''    location = /api/regelingen {
        proxy_pass http://127.0.0.1:8765;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_connect_timeout 5s;
        proxy_read_timeout 360s;
    }

    location ^~ /api/regelingen/jobs/ {
        proxy_pass http://127.0.0.1:8765;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_connect_timeout 5s;
        proxy_read_timeout 10s;
    }

    location ^~ /_candidate/ {
        alias /var/lib/pensioen-deploy/previews/;
        autoindex off;
        add_header X-Robots-Tag "noindex, nofollow, noarchive" always;
        add_header X-Content-Type-Options "nosniff" always;
    }

'''
if "location = /api/regelingen {" not in text:
    marker = "    index index.html;\n"
    if text.count(marker) != 1:
        raise SystemExit("Onverwachte Pensioen-vhost; API-locaties niet geplaatst.")
    text = text.replace(marker, marker + "\n" + locations, 1)
fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".pensioen-vhost.")
with os.fdopen(fd, "w") as stream:
    stream.write(text)
os.chmod(tmp, path.stat().st_mode)
os.replace(tmp, path)
PY

nginx -t
systemd-analyze verify "$api_unit"
systemctl daemon-reload
systemctl enable --now pensioen-regelingen-api.service
systemctl restart pensioen-deploy.timer
if ! systemctl is-active --quiet pensioen-regelingen-api.service; then
  systemctl status pensioen-regelingen-api.service --no-pager -l >&2 || true
  journalctl -u pensioen-regelingen-api.service -n 30 --no-pager >&2 || true
  exit 1
fi
echo active
api_status=""
for attempt in {1..30}; do
  api_status=$(curl --silent --output /dev/null --write-out '%{http_code}' \
    --max-time 2 http://127.0.0.1:8765/api/regelingen/jobs/invalid || true)
  [[ "$api_status" == 404 ]] && break
  sleep 1
done
if [[ "$api_status" != 404 ]]; then
  echo "De API antwoordde niet op localhost (HTTP-status: ${api_status:-geen})." >&2
  journalctl -u pensioen-regelingen-api.service -n 30 --no-pager >&2 || true
  exit 1
fi
systemctl reload nginx
curl --fail --silent --show-error --output /dev/null \
  --write-out 'Pensioen-homepage: HTTP %{http_code}\n' https://pensioen.myaiprojects.nl/

success=1
trap - EXIT
rm -rf -- "$tmp"
printf 'Beheer-API geïnstalleerd; nginx-configuratie en homepage gecontroleerd.\n'
printf 'Back-up: %s\n' "$backup_dir"
