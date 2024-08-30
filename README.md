# EasyLunch_backend
UMP-JUST 生成AI ハッカソン用 バックエンドリポジトリです。

### 初期設定
#### AWS CLIのインストール
[リンク](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/getting-started-install.html)
を参考にして、AWS CLIをインストールします。  
その後に、以下のコマンドを入力してconfigureを埋めます。
```bash
$ aws configure --profile test
AWS Access Key ID : // Access Key IDを入力
AWS Secret Access Key : // Secret Access Key
Default region name : // us-east-1を入力
Default output format : // 入力せずそのまま ReturnでOK
```

#### ホットペッパーAPIの取得
以下のサイトからAPIキーを発行します。（メアドを登録するだけで1分もかからず取得可能）  
  [リクルートwebサービス](https://webservice.recruit.co.jp/register/)  
※ リンクが不正の場合は、自分で検索し直してリトライすることが推奨されます。

#### Credentialの設定
以下のコマンドで、config.yamlを生成します。
```bash
cp config_template.yaml config.yaml
```
生成されたconfig.yamlに記述されているCredentialを埋めます。

### DBの立ち上げ
~~ to be filled ~~

### ボットサーバーの立ち上げ
以下のコマンドでLINEボットサーバーを立ち上げることが出来ます。
```bash
python src/app.py
```
