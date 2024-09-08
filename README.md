# EasyLunch_backend
UMP-JUST 生成AI ハッカソン用 バックエンドリポジトリです。

### 動作例
https://github.com/user-attachments/assets/350fc850-d593-4578-9053-d464f614d429

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

#### DBのクレデンシャルの設定
src/db/docker/README.mdの指示に従って、データベース用のクレデンシャル設定を行います。

### DBの立ち上げ
src/db/docker/README.mdの指示に従って、データベースの立ち上げを行います。

### ボットサーバーの立ち上げ
まず、config.yamlを編集して
```yaml
MYSQL_HOST: "localhost"
```
と編集します。
以下のコマンドでLINEボットサーバーを立ち上げることが出来ます。
```bash
python src/app.py
```
config.yaml(or 環境変数)の```LLM_TYPE```は現在```claude 3.5 sonnet```と```gpt-4o```の二つのversionに対応してあります。  
これらを編集することで、BOTがアクセスするLLMのタイプを編集することができます。

### Docker環境での立ち上げ
まず、config.yamlを編集して
```yaml
MYSQL_HOST: "db"
```
と編集します。
次に以下のコマンドでDockerコンテナを立ち上げます。
```bash
docker compose up -d
```
最後に以下のコマンドでログをターミナルに流すようにします。
```bash
docker logs -f easylunch_server
```

### Google Cloud でのデプロイ
config.yamlを編集して、
```yaml
IS_GOOGLE_CLOUD: true
...
MY_SQL_HOST: "デプロイしたSQLサーバのunix(...)の中身..."
```
となるようにして行う。
