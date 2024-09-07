## コードの説明
以下の説明は、全てリポジトリ直下にて実行してください。

### hot_pepper
**search_restaurant_essential_test.py**
```bash
python ./src/test/hot_pepper/search_restaurant_essential_test.py
```
ホットペッパーグルメのAPIを叩いた結果が表示されます。

**match_condition.py**
```bash
python ./src/test/hot_pepper/match_condition.py
```
指定した店舗idが条件に一致するかどうかを確認します。

**change_if_match.py**
```bash
python ./src/test/hot_pepper/change_if_match.py
```
現状は来店履歴店舗idのリスト  
(ex,`["J001232494", "J001194791", "J001052469"]`)  
を順に見ていって、その中に条件に合うものがあったら都度5つ目の要素をその店舗と変更するように実装しています。

### google_places
**search_essential.py**
```bash
python ./src/test/google_places/search_essential.py
```
検索クエリを元に、Google Places APIを叩いた結果が表示されます。
また、店舗idを指定して、Google Places APIを叩いた結果が表示されます。

### llm
**aws.py**
```bash
python ./src/test/llm/aws.py
```
画像入力, system prompt, user prompt のすべてを使用したテスト結果が表示されます。

**llm_call.py**
```bash
python ./src/test/llm/llm_call.py -t "モデル名"
```
-t 以降に使用したいモデル名を指定することで、モデルに応じたクライアントが(aws bedrock, cotomi, azure) から選択されます。  
画像入力, system prompt, user prompt のすべてを使用したテスト結果が表示されます。  
現在 ```"モデル名"```　の箇所は "claude 3.5 sonnet" のみ対応しています。

**extract_info.py**
```bash
python ./src/test/llm/extract_info.py
```
chat_history.pickle に保存された会話履歴を使用して、ユーザプロンプトを作成し、ユーザが飲食店に対し求めている条件を抽出します。  

### line
**send_flex.py**
```bash
ngrok http --domain=<your-domein-name> <your-port-number>
python ./src/test/line/send_flex.py
```
hotpepperAPIを叩いた結果をフレックスメッセージで返信します。

**send_text.py**
```bash
ngrok http --domain=<your-domein-name> <your-port-number>
python ./src/test/line/send_text.py
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
来店履歴DBにアクセスして、UserIDを用いた来店履歴の取得と追加を行います。

**chat.py**
src/db/docker/README.md の指示に従ってdockerでDBを立ち上げた後に、以下のコマンドを実行します。
```bash
python ./src/test/db/chat.py
```
会話履歴DBにアクセスして、UserIDを用いた会話の追加・取得・削除を行います。

