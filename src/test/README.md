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
