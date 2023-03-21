#!/usr/bin/env bash

[[ ! -n "$XUI_USER" && ! -n "$XUI_PASS" ]] && /usr/local/x-ui/x-ui setting -username ${XUI_USER} -password ${XUI_PASS}
[[ ! -n "$XUI_PORT" ]] && /usr/local/x-ui/x-ui setting -port ${XUI_PORT}

cd /usr/local/x-ui/
exec "$@"
