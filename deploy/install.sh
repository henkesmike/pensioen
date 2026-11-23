#!/usr/bin/env bash
set -euo pipefail

commit="${1:?Vaste GitHub-commit vereist}"
[[ $commit =~ ^[0-9a-f]{40}$ ]]
[[ $(id -u) == 0 ]]

site=/var/www/pensioen/index.html
base=/var/lib/pensioen-deploy
public=$base/public
active=$public/index.html
worker=/usr/local/lib/pensioen-deploy/publish.py
service_user=pensioen-deploy

if [[ -L $site ]]; then
    [[ $(readlink "$site") == "$active" && -f $active ]]
else
    [[ -f $site ]]
fi

temp=$(mktemp -d)
trap 'rm -rf -- "$temp"' EXIT
curl --proto '=https' --fail --silent --show-error --max-time 30 \
    "https://raw.githubusercontent.com/henkesmike/pensioen/$commit/deploy/publish.py" \
    -o "$temp/publish.py"
/usr/bin/python3 -m py_compile "$temp/publish.py"

if ! id "$service_user" >/dev/null 2>&1; then
    useradd --system --user-group --home-dir "$base" --shell /usr/sbin/nologin "$service_user"
fi
install -d -m 0755 "$base" /usr/local/lib/pensioen-deploy
install -d -m 0755 -o "$service_user" -g "$service_user" "$public"
install -m 0644 "$temp/publish.py" "$worker"

cat > /etc/systemd/system/pensioen-deploy.service <<'UNIT'
[Unit]
Description=Ververs de goedgekeurde homepage van Pensioen Ontdekt
After=network-online.target

[Service]
Type=oneshot
User=pensioen-deploy
Group=pensioen-deploy
ExecStart=/usr/bin/python3 /usr/local/lib/pensioen-deploy/publish.py
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
PrivateTmp=yes
ReadWritePaths=/var/lib/pensioen-deploy/public
TimeoutStartSec=40
UNIT

cat > /etc/systemd/system/pensioen-deploy.timer <<'UNIT'
[Unit]
Description=Controleer op een goedgekeurde homepage-uitrol

[Timer]
OnActiveSec=30s
OnUnitInactiveSec=60s
AccuracySec=5s

[Install]
WantedBy=timers.target
UNIT

if [[ ! -L $site ]]; then
    install -m 0600 "$site" "$base/index.voor-automatisering.html"
    install -m 0644 -o "$service_user" -g "$service_user" "$site" "$active"
    link_dir=$(mktemp -d /var/www/pensioen/.pensioen-link.XXXXXX)
    ln -s "$active" "$link_dir/index.html"
    mv -T "$link_dir/index.html" "$site"
    rmdir "$link_dir"
fi

systemctl daemon-reload
systemctl enable --now pensioen-deploy.timer
systemctl is-active pensioen-deploy.timer
