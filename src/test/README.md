## コードの説明
以下の説明は、全てリポジトリ直下にて実行してください。

### hot_pepper
**search_restaurant_essential_test.py**
```bash
python .\src\test\hot_pepper\search_restaurant_essential_test.py
```
ホットペッパーグルメのAPIを叩いた結果が表示されます。

### llm
**aws.py**
```bash
python .\src\test\llm\aws.py
```
画像入力, system prompt, user prompt のすべてを使用したテスト結果が表示されます。

**llm_call.py**
```bash
python .\src\test\llm\llm_call.py -t "モデル名"
```
-t 以降に使用したいモデル名を指定することで、モデルに応じたクライアントが(aws bedrock, cotomi, azure) から選択されます。  
画像入力, system prompt, user prompt のすべてを使用したテスト結果が表示されます。  
現在 ```"モデル名"```　の箇所は "claude 3.5 sonnet" のみ対応しています。

### line
**send_flex_msg.py**
```bash
ngrok http --domain=<your-domein-name> <your-port-number>
python ./src/test/line/send_flex_msg.py
```
```config.yaml```にて設定したラインアカウントに任意のメッセージを送ると、```template.json```で定義されたflex messageが返信されます。

**send_text_msg.py**
```bash
ngrok http --domain=<your-domein-name> <your-port-number>
python ./src/test/line/send_text_msg.py
```
```config.yaml```にて設定したラインアカウントに任意のメッセージを送ると、ユーザのidが返信されます。


### db
**connector.py**
src/db/docker/README.md の指示に従ってdockerでDBを立ち上げた後に、以下のコマンドを実行します。
```bash
python ./src/test/db/connector.py
```
データベースにアクセスして、CRUDの各機能を確認した結果が返ってきます。

**visit.py**
src/db/docker/README.md の指示に従ってdockerでDBを立ち上げた後に、以下のコマンドを実行します。
```bash
python ./src/test/db/visit.py
```
来店履歴DBにアクセスして、UseIDを用いた来店履歴の取得と追加を行います。
