Azure Function App sample: CSV
===

[![Build and deploy Python project to Azure Function App - function-app-sample-csv](https://github.com/yuu-eguci/function-app-sample-csv/actions/workflows/main_function-app-sample-csv.yml/badge.svg)](https://github.com/yuu-eguci/function-app-sample-csv/actions/workflows/main_function-app-sample-csv.yml)

Timer trigger で CSV を読んでログに出す Azure Functions (Python v1 プログラミングモデル) のサンプル。

- Python: 3.13!
- Linter: Ruff!
- Test: pytest!
- Azure Functions: ランタイム 4.x / azure-functions 2.x!

## Python で直接

[uv](https://docs.astral.sh/uv/) を使う。

```bash
uv sync
uv run ruff check . && uv run ruff format --check .
uv run pytest
```

依存を変えたら requirements.txt も作り直す (Azure のリモートビルドと VS Code の task はこっちを読む)。

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
    - Python プログラミングモデル v2 は、このリポジトリを作っている段階ではプレビュー。 (いまは GA。このリポジトリは v1 のまま)
- venv 環境がデフォだけど、ほかのツールに替えることができる。最初は pipenv にして、いまは uv (pyproject.toml + uv.lock)。
    - Azure 側は requirements.txt を読むので、それは `uv export` で作る。
- Python 3.13 は Linux の従量課金 (Consumption) プランでは使えない (3.12 まで)。Flex Consumption なら使える。
- CI/CD は Azure Function App 側にリソースを作るときついでに GitHub Actions を設定できるから、それでやっちゃおう。 Secrets も登録してくれて楽だよ。
    - 注意: これを有効にするにはリソースの public url を有効にする必要がある。一度 "セキュリティのため〜" とかいって無効にしたらデプロイするとき 403 が出まくった。
- Function App は App Service Plan の上にあるっぽくて、 slot を使うこともできる。
- このリポジトリでは Ruff や pytest も導入したよ。 pyproject.toml を見たら雰囲気がわかるよ。
- ローカル環境で実行するときはこんな感じ↓
    1. F5 押して Azure Tools 拡張機能をインストール
    2. Azurite 拡張機能をインストール
    3. Azurite: Start する
    4. Terminal で func start する
- ローカル環境実行の参考はここ↓
    - https://learn.microsoft.com/ja-jp/azure/storage/common/storage-use-azurite?tabs=visual-studio-code#run-azurite-from-a-command-line
