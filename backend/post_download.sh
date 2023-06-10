#!/bin/sh
exec >/tmp/script.log 2>&1
set -x
python3 -c "import requests;requests.post(\"http://localhost:8000/internal/updatedb/\", json = {})"