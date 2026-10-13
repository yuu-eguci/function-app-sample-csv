#!/usr/bin/env bash
# app を起動し、タイマーが CSV を読んだログ ("Loaded 3 rows") が出るまで待つ。最後に片付ける。
# 待ち時間は SMOKE_TIMEOUT 秒 (既定 150)。関数の実行が失敗するか app コンテナが止まったら、その時点で NG。
set -euo pipefail
cd "$(dirname "$0")/.."

timeout="${SMOKE_TIMEOUT:-150}"
trap 'docker compose down -v' EXIT

ng() {
  docker compose logs app
  echo "smoke: NG ($1)" >&2
  exit 1
}

docker compose up -d --build app
for ((waited = 0; waited < timeout; waited += 5)); do
  logs="$(docker compose logs app || true)"
  if [[ "$logs" == *"Loaded 3 rows"* ]]; then
    echo "$logs"
    echo "smoke: OK (${waited}s)"
    exit 0
  fi
  if [[ "$logs" == *"Executed 'Functions.sample_csv_function' (Failed"* ]]; then
    ng "関数の実行が失敗した (${waited}s)"
  fi
  if [[ -z "$(docker compose ps --status running -q app || true)" ]]; then
    ng "app コンテナが止まった (${waited}s)"
  fi
  sleep 5
done
ng "'Loaded 3 rows' が ${timeout} 秒以内に出なかった"
