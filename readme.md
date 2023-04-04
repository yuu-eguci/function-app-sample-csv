Azure Function App sample: CSV
===

🐍 :octocat: Azure Functions + Timer trigger + GitHub Actions + Python3.10 + Pipenv + Util class + Flake8 + Unittest + Csv
そんなサンプルを作ろうじゃないか!

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
    - Python プログラミングモデル v2 は、このリポジトリを作っている段階ではプレビュー。
- venv 環境がデフォだけど、そっくりそのまま pipenv に替えることができる。
- CI/CD は Azure Function App 側にリソースを作るときついでに GitHub Actions を設定できるから、それでやっちゃおう。 Secrets も登録してくれて楽だよ。
    - 注意: これを有効にするにはリソースの public url を有効にする必要がある。一度 "セキュリティのため〜" とかいって無効にしたらデプロイするとき 403 が出まくった。
- Function App は App Service Plan の上にあるっぽくて、 slot を使うこともできる。
- このリポジトリでは flake8 や unittest も導入したよ。 yml を見たら雰囲気がわかるよ。
- ローカル環境で実行するときはこんな感じ↓
    1. F5 押して Azure Tools 拡張機能をインストール
    2. Azurite 拡張機能をインストール
    3. Azurite: Start する
    4. Terminal で func start する
- ローカル環境実行の参考はここ↓
    - https://learn.microsoft.com/ja-jp/azure/storage/common/storage-use-azurite?tabs=visual-studio-code#run-azurite-from-a-command-line
