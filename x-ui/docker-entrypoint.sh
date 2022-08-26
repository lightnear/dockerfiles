#!/usr/bin/env bash
set -eux

[[ ! -d /app/x-ui ]] && mkdir -p /app/x-ui
if [[ ! -f /app/x-ui/bin/xray-linux-* ]]; then
  latest_version=$(curl -sX GET "https://api.github.com/repos/FranzKafkaYu/x-ui/releases/latest" | \
    awk '/tag_name/{print $4;exit}' FS='[""]')
  arch=$(arch)
  if [[ $arch == "x86_64" || $arch == "x64" || $arch == "amd64" ]]; then
    arch="amd64"
  elif [[ $arch == "aarch64" || $arch == "arm64" ]]; then
    arch="arm64"
  else
    arch="amd64"
  fi
  curl -o /tmp/x-ui-linux-${arch}.tar.gz -L "https://github.com/FranzKafkaYu/x-ui/releases/download/${latest_version}/x-ui-linux-${arch}.tar.gz"
  tar zxvf /tmp/x-ui-linux-${arch}.tar.gz -C /app
  chmod +x /app/x-ui/x-ui /app/x-ui/bin/xray-linux-* /app/x-ui/x-ui.sh
fi

exec "$@"
