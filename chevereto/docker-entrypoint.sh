#!/usr/bin/env bash
set -Eeuo pipefail

# Create missing directory if we don't have and give permission
[[ ! -d /var/www/html/ ]] && mkdir -p /var/www/html/
chown -R www-data:www-data /var/www/html

# Download & install chevereto if there is no index.php (it means already be installed chevereto)
if [[ ! -f /var/www/html/index.php ]]; then
  if [ -z ${CHEVERETO_RELEASE+x} ]; then
    CHEVERETO_RELEASE=$(curl -sX GET "https://api.github.com/repos/rodber/chevereto-free/releases/latest" \
    | awk '/tag_name/{print $4;exit}' FS='[""]')
  fi
  curl -o /tmp/chevereto.tar.gz -L "https://github.com/rodber/chevereto-free/archive/${CHEVERETO_RELEASE}.tar.gz"
  tar xf /tmp/chevereto.tar.gz -C /var/www/html --strip-components=1
  chown -R www-data:www-data /var/www/html
  mv /var/www/html/sync.sh /tmp/sync.sh
  composer install \
    --working-dir=/var/www/html \
    --prefer-dist \
    --no-progress \
    --classmap-authoritative \
    --ignore-platform-reqs
  mv /tmp/sync.sh /var/www/sync.sh
  chmod +x /var/www/sync.sh
fi
# [[ -f /var/www/html/installer.php ]] && chown www-data:www-data /var/www/html/installer.php

if [[ ! -f /var/www/html/app/routes/overrides/route.api.php ]]; then
  mkdir -p /var/www/html/app/routes/overrides
  mv /tmp/route.api.php /var/www/html/app/routes/overrides/
fi

# Run apache2 foreground
exec "$@"
