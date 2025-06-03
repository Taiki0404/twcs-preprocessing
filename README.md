# twcs preprocessing

kaggleで公開されているデータセット「[Customer Support on Twitter](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter)」
の前処理を行うためのリポジトリです。

## 主なファイル

1. `main.py`
	- `twcs.csv`ファイルから、4つのファイルを生成します。
2. `sampling.py`
	- 生成したファイルを元に、対話IDをサンプリングします。
3. `generate_plain_texts.py`
	- 対話IDに紐づくツイート文章をテキストファイルとして出力します。

## main.py

### 使い方

1. kaggleから[Customer Support on Twitter](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter)をダウンロードする。
2. `archive.zip`を解凍する。
3. `twcs.csv`を`main.py`と同じ階層に配置する。
4. `python main.py --twcs-path twcs.csv`を実行する。
5. `output`ディレクトリに4つのファイルが出力される。

### 出力されるファイルについて

#### tweet_meta.csv

ツイートのメタデータを格納しています。

| tweet_id | author_id    | inbound | created_at                     |
| -------- | ------------ | ------- | ------------------------------ |
| 119237   | 105834       | True    | Wed Oct 11 06:55:44 +0000 2017 |
| 119238   | ChaseSupport | False   | Wed Oct 11 13:25:49 +0000 2017 |

#### text.csv

ツイートごとに前処理を行ったテキストを格納しています。

| tweet_id | processed_text                                                                                               |
| -------- | ------------------------------------------------------------------------------------------------------------ |
| 119237   | causing the reply to be disregarded and the tapped notification under the keyboard is opened                 |
| 119238   | your business means a lot to us. please dm your name, zip code and additional details about your concern. rr |

#### seq.csv

対話におけるツイートの順序を格納しています。

| utterance | sequence | dialog_id |
| --------- | -------- | --------- |
| 119237    | 0        | 0         |
| 119236    | 1        | 0         |

#### dialog_meta.csv

対話のメタデータを格納しています。

| dialog_id | supporter    | n_authors | length |
| --------- | ------------ | --------- | ------ |
| 0         | ChaseSupport | 2         | 2      |

## sampling.py

### サンプリングの前提

- 対話に含まれる発話数：2~6
	- データ数の分布の関係でこの設定にしています。
- 対話に参加している話者数：2

### パラメータ

#### `--campany, -c`

サンプリングする会社を指定します。

#### `--n-samples, -n`

サンプリングする数を指定します。

### 出力

`output/{日付}/samples`ディレクトリに`{会社名}_{サンプル数}.txt`というテキストファイルが出力されます。
テキストファイルには、サンプリングした対話IDが１行ごとに記述されています。

## generate_plain_texts.py

### パラメータ

#### `--input-path`

[sampling.py](#samplingpy)で出力されたテキストファイルを指定します。

### 出力

`--input-path`で指定したファイルと同階層に`txt`ディレクトリが生成され、その中に`dialog_{対話ID}.txt`というテキストファイルが出力されます。

## 注意事項

- このリポジトリにはデータセットそのものは含まれていません。
- データセットは [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) ライセンスの下で提供されています。
- データセットを利用する場合は、元のライセンス条件を遵守してください。

## ライセンス

- このリポジトリ内のスクリプトおよび生成物も [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) ライセンスの下で公開されています。

## クレジット

- データセットの出典: [Customer Support on Twitter](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter)
- 著作者: Stuart Axelbrooke
