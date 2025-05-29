# twcs preprocessing

kaggleで公開されているデータセット「[Customer Support on Twitter](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter)」
の前処理を行うためのリポジトリ

## 使い方

1. kaggleから[Customer Support on Twitter](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter)をダウンロード
2. `archive.zip`を解凍
3. `twcs.csv`を`main.py`と同じ階層に配置
4. `python main.py --twcs-path twcs.csv`を実行する
5. `output`ディレクトリに4つのファイルが出力される

## 出力されるファイルについて

### tweet_meta.csv

ツイートのメタデータを格納している

| tweet_id | author_id    | inbound | created_at                     |
| -------- | ------------ | ------- | ------------------------------ |
| 119237   | 105834       | True    | Wed Oct 11 06:55:44 +0000 2017 |
| 119238   | ChaseSupport | False   | Wed Oct 11 13:25:49 +0000 2017 |

### text.csv

ツイートごとに前処理を行ったテキストを格納している

| tweet_id | processed_text                                                                                               |
| -------- | ------------------------------------------------------------------------------------------------------------ |
| 119237   | causing the reply to be disregarded and the tapped notification under the keyboard is opened                 |
| 119238   | your business means a lot to us. please dm your name, zip code and additional details about your concern. rr |

### seq.csv

対話におけるツイートの順序を格納している

| utterance | sequence | dialog_id |
| --------- | -------- | --------- |
| 119237    | 0        | 0         |
| 119236    | 1        | 0         |

### dialog_meta.csv

対話のメタデータを格納している

| dialog_id | supporter    | n_authors | length |
| --------- | ------------ | --------- | ------ |
| 0         | ChaseSupport | 2         | 2      |

## 注意事項

- このリポジトリにはデータセットそのものは含まれていません。
- データセットは [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) ライセンスの下で提供されています。
- データセットを利用する場合は、元のライセンス条件を遵守してください。

## ライセンス

- このリポジトリ内のスクリプトおよび生成物も [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) ライセンスの下で公開されています。

## クレジット

- データセットの出典: [Customer Support on Twitter](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter)
- 著作者: Stuart Axelbrooke
