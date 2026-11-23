#!/usr/bin/env bash
set -euo pipefail

commit="$1"
[[ "$commit" =~ ^[0-9a-f]{40}$ ]]
[[ "$(id -u)" == 0 ]]
[[ "$(hostname)" == myaiprojects-server ]]

service_user=pensioen-deploy
base=/var/lib/pensioen-deploy
unit=/etc/systemd/system/pensioen-deploy.service
nginx_conf=/etc/nginx/sites-available/pensioen
auth_file=/etc/nginx/pensioen-preview.htpasswd
publish_file=/usr/local/lib/pensioen-deploy/publish.py
reference=/root/pensioen-poc/partnerpensioen-v3.html
source_cache=/root/pensioen-poc/fase3
nginx_user=$(awk '$1=="user"{gsub(/;/,"",$2); print $2; exit}' /etc/nginx/nginx.conf)

id "$service_user" >/dev/null
test -f "$reference"
test -d "$source_cache"
test -f "$unit"
test -f "$nginx_conf"
test "$nginx_user" = www-data
grep -qF 'ReadWritePaths=/var/lib/pensioen-deploy /var/www/pensioen' "$unit"

stamp=$(date -u +%Y%m%dT%H%M%SZ)
unit_backup="/root/pensioen-deploy.service.$stamp.bak"
nginx_backup="/root/pensioen-nginx.$stamp.bak"
auth_backup="/root/pensioen-preview-auth.$stamp.bak"
publish_backup="/root/pensioen-publish.$stamp.bak"
cp -a "$unit" "$unit_backup"
cp -a "$publish_file" "$publish_backup"
cp -a "$nginx_conf" "$nginx_backup"
if [[ -f "$auth_file" ]]; then cp -a "$auth_file" "$auth_backup"; fi

success=0
rollback() {
  if [[ "$success" -eq 0 ]]; then
    cp -a "$unit_backup" "$unit" 2>/dev/null || true
    cp -a "$publish_backup" "$publish_file" 2>/dev/null || true
    cp -a "$nginx_backup" "$nginx_conf" 2>/dev/null || true
    if [[ -f "$auth_backup" ]]; then
      cp -a "$auth_backup" "$auth_file" 2>/dev/null || true
    else
      rm -f "$auth_file"
    fi
    systemctl daemon-reload 2>/dev/null || true
    nginx -t 2>/dev/null && systemctl reload nginx 2>/dev/null || true
  fi
  systemctl start --now pensioen-deploy.timer 2>/dev/null || true
}
trap rollback EXIT

systemctl stop pensioen-deploy.timer pensioen-deploy.service

tmp=$(mktemp -d)
trap 'rm -rf -- "$tmp"; rollback' EXIT
curl --proto '=https' --fail --silent --show-error --max-time 30 \
  "https://raw.githubusercontent.com/henkesmike/pensioen/$commit/deploy/site_agent.py" \
  -o "$tmp/site_agent.py"
curl --fail --silent --show-error --max-time 30 "https://raw.githubusercontent.com/henkesmike/pensioen/$commit/deploy/publish.py" -o "$tmp/publish.py"
/usr/bin/python3 -m py_compile "$tmp/site_agent.py" "$tmp/publish.py"
install -m 0644 "$tmp/site_agent.py" /usr/local/lib/pensioen-deploy/site_agent.py
install -m 0644 "$tmp/publish.py" "$publish_file"

install -d -m 0700 -o "$service_user" -g "$service_user" "$base/private" "$base/private/fase3"
install -m 0600 -o "$service_user" -g "$service_user" \
  "$reference" "$base/private/partnerpensioen-v3.html"
cp -a "$source_cache/." "$base/private/fase3/"
chown -R "$service_user:$service_user" "$base/private"
find "$base/private" -type d -exec chmod 0700 {} +
find "$base/private" -type f -exec chmod 0600 {} +

install -d -m 2750 -o "$service_user" -g "$nginx_user" "$base/previews"
chown "$service_user:$nginx_user" "$base/previews"
chmod 2750 "$base/previews"
install -d -m 0750 -o "$service_user" -g "$service_user" \
  "$base/candidates" "$base/state" "$base/backups"

preview_password=""
if [[ ! -f "$auth_file" ]]; then
  preview_password=$(openssl rand -hex 18)
  preview_hash=$(printf '%s' "$preview_password" | openssl passwd -apr1 -stdin)
  printf 'mike:%s\n' "$preview_hash" > "$auth_file"
  chown root:www-data "$auth_file"
  chmod 0640 "$auth_file"
fi

python3 - "$nginx_conf" <<'PY'
import os, sys, tempfile
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text()
location = """    location ^~ /_preview/ {
        auth_basic "Pensioen preview";
        auth_basic_user_file /etc/nginx/pensioen-preview.htpasswd;
        alias /var/lib/pensioen-deploy/previews/;
        autoindex off;
        add_header X-Robots-Tag "noindex, nofollow, noarchive" always;
    }

"""
marker = "    index index.html;\n"
if "location ^~ /_preview/" not in text:
    if text.count(marker) != 1:
        raise SystemExit("Onverwachte Pensioen-vhost; previewlocatie niet geplaatst.")
    text = text.replace(marker, marker + "\n" + location, 1)
fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".pensioen-vhost.")
with os.fdopen(fd, "w") as stream:
    stream.write(text)
os.chmod(tmp, path.stat().st_mode)
os.replace(tmp, path)
PY

python3 - "$unit" <<'PY'
import os, sys, tempfile
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text()
old = "ExecStart=/usr/bin/python3 /usr/local/lib/pensioen-deploy/publish.py"
new = "ExecStart=/usr/bin/python3 /usr/local/lib/pensioen-deploy/site_agent.py"
if old in text:
    text = text.replace(old, new)
elif new not in text:
    raise SystemExit("Onverwachte ExecStart; servicebestand niet aangepast.")
text = text.replace("TimeoutStartSec=40", "TimeoutStartSec=900")
fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".pensioen-service.")
with os.fdopen(fd, "w") as stream:
    stream.write(text)
os.chmod(tmp, path.stat().st_mode)
os.replace(tmp, path)
PY

nginx -t
systemd-analyze verify "$unit"
systemctl daemon-reload
systemctl reload nginx
systemctl start --now pensioen-deploy.timer
systemctl is-active pensioen-deploy.timer
systemctl show pensioen-deploy.service -p ExecStart -p TimeoutStartUSec -p ReadWritePaths
curl --fail --silent --show-error --output /dev/null \
  --write-out 'Pensioen-homepage: HTTP %{http_code}\n' https://pensioen.myaiprojects.nl/
success=1
trap - EXIT
rm -rf -- "$tmp"
if [[ -n "$preview_password" ]]; then
  printf '\nPreview-account: mike\nPreview-wachtwoord (bewaar dit): %s\n' "$preview_password"
else
  printf '\nPreview-account bestaat al; bestaand wachtwoord is behouden.\n'
fi
printf 'Backups: %s, %s en %s\n' "$unit_backup" "$nginx_backup" "$publish_backup"
