# python-docker-template

DevContainerでPythonの開発環境を作るためのテンプレート

Pythonのパッケージ管理にはpoetryを使用

※ [Poetryの公式ドキュメント](https://python-poetry.org/docs/configuration#virtualenvscreate) では仮想環境の作成が推奨されているため、このテンプレートでもDockerコンテナ内で仮想環境を作成し、依存関係を分離する

## Extensions

以下の拡張機能を導入（主な用途）

- [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) - AIコード補完
- [GitHub Copilot Chat](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat) - AIによるコードレビュー・サポート
- [Git Graph](https://marketplace.visualstudio.com/items?itemName=mhutchie.git-graph) - Git履歴の可視化
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) - Python開発環境
- [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) - Jupyter Notebookのサポート
- [Mypy Type Checker](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker) - 型チェック（Mypy）
- [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) - PythonのLinter・フォーマッター

## Usage

1. [Docker Hub](https://hub.docker.com/_/python/) からPythonのタグ（バージョン）を選択
2. 選択したタグを `Dockerfile` に記入
3. VSCodeで `Reopen in Container` を実行（DevContainer環境を起動）
4. コンテナ内で `poetry init` を実行し、プロジェクトをセットアップ
5. 必要なパッケージを `poetry add <package-name>` で追加
