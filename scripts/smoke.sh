#!/usr/bin/env bash
# app を起動し、タイマーが CSV を読んだログ ("Loaded 3 rows") が出るまで待つ。最後に片付ける。
# 待ち時間は SMOKE_TIMEOUT 秒 (既定 150)。
set -euo pipefail
cd "$(dirname "$0")/.."

timeout="${SMOKE_TIMEOUT:-150}"
trap 'docker compose down -v' EXIT

docker compose up -d --build app
for ((waited = 0; waited < timeout; waited += 5)); do
  logs="$(docker compose logs app || true)"
  if [[ "$logs" == *"Loaded 3 rows"* ]]; then
    echo "$logs"
    echo "smoke: OK (${waited}s)"
    exit 0
  fi
  sleep 5
done
docker compose logs app
echo "smoke: NG ('Loaded 3 rows' が ${timeout} 秒以内に出なかった)" >&2
exit 1
