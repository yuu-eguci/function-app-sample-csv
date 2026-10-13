Azure Function App sample: CSV
===

[![CI](https://github.com/yuu-eguci/function-app-sample-csv/actions/workflows/ci.yml/badge.svg)](https://github.com/yuu-eguci/function-app-sample-csv/actions/workflows/ci.yml)

タイマーで CSV を読んで、ログに出す Azure Functions のサンプル。
クラウドの設定なしで、まずは手元で動かしてみようぜ。

- Docker: 対応!
- Python: 3.13!
- Linter: Ruff!
- Test: pytest!
- Azure Functions: ランタイム 4.x / azure-functions 2.x!

## パッと実行してみたい

```bash
docker compose up --build app
```

- Azurite (ストレージエミュレータ) と Functions ホストが、インターネットに出られない閉じたネットワークで起動する。
- 1 分以内にタイマーが発火して、CSV の 3 行がログに出る。止めるときは Ctrl+C。
- Functions のイメージは amd64 のみなので、Apple Silicon ではエミュレーションで動く (起動が少し遅い)。
- 自動で起動確認して片付けるなら `scripts/smoke.sh`。失敗したら NG になる。

Lint とテストはこれ↓ (ruff + pytest。ネットワークなし)

```bash
docker compose run --rm --build check
```

## Python で直接

[uv](https://docs.astral.sh/uv/) を使う。

```bash
uv sync
uv run ruff check . && uv run ruff format --check .
uv run pytest
```

依存を変えたら requirements.txt も作り直す (Azure のリモートビルドはこっちを読む。CI で差分チェックしている)。

```bash
uv export --locked --no-dev --no-hashes --no-emit-project -o requirements.txt
```

## TIL

- Function App を作ろうっつってきみが最初に思うのは "どんなディレクトリ構成のリポジトリになるんだろう?" だよな。こうだよ↓
    - これをほーんって見ながら Azure Function App を見ると、ひとつのリソースの中に複数の functions があるのがわかるね。

```
<project_root>/
 | - .venv/
 | - .vscode/
 | - my_first_function/
 | | - __init__.py
 | | - function.json
 | | - example.py
 | - my_second_function/
 | | - __init__.py
 | | - function.json
 | - shared_code/
 | | - __init__.py
 | | - my_first_helper_function.py
 | | - my_second_helper_function.py
 | - tests/
 | | - test_my_second_function.py
 | - .funcignore
 | - host.json
 | - local.settings.json
 | - requirements.txt
 | - Dockerfile
```

参考: https://learn.microsoft.com/ja-jp/azure/azure-functions/functions-reference-python?tabs=asgi%2Capplication-level&pivots=python-mode-configuration#folder-structure

- このディレクトリ構成は Azure Functions 拡張機能で作る。 (VSC)
    - このリポジトリは Python の v1 プログラミングモデルを使う。
- 依存管理は uv (pyproject.toml + uv.lock)。
    - Azure 側は requirements.txt を読むので、それは `uv export` で作る。
- Functions のイメージ (Docker / Azure) では、依存は `.python_packages/lib/site-packages` に入れる (Dockerfile もそう)。ふつうに pip install すると、ワーカーに同梱の azure-functions のほうが先に読まれて、ロックした版にならない。ローカルの func start は .venv を使う。
- Python 3.13 は Linux の従量課金 (Consumption) プランでは使えない (3.12 まで)。Flex Consumption なら使える。
- CI は lint・テスト・Docker での起動確認だけ。Azure へのデプロイはしない。
- このリポジトリでは Ruff や pytest も導入したよ。 pyproject.toml と .github/workflows/ci.yml を見たら雰囲気がわかるよ。
- ローカル環境で実行するときはこんな感じ↓ (Docker なしでやる場合)
    1. F5 押して Azure Tools 拡張機能をインストール
    2. Azurite 拡張機能をインストール
    3. Azurite: Start する
    4. Terminal で func start する
- ローカル環境実行の参考はここ↓
    - https://learn.microsoft.com/ja-jp/azure/storage/common/storage-use-azurite?tabs=visual-studio-code#run-azurite-from-a-command-line
