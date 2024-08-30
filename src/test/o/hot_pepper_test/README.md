## ホットペッパーAPI動かしてみた

### 参考にしたサイト
[pythonでホットペッパーのAPIを叩いてみた](https://web-tweets.com/python/hotpepper-api/)  
[Pythonで簡単に始める！ホットペッパーグルメAPI活用ガイド](https://zenn.dev/shintaro/articles/053fe2ca8b3430)

### コードを動かすのに必要なこと
- pip install requests
- 以下のサイトからAPIキーを発行する（メアドを登録するだけで1分もかからず取得可能）  
  [リクルートwebサービス](https://webservice.recruit.co.jp/register/)

### リクエストの基本構造
```python
import requests

url = "https://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
params = {
    "key": "YOUR_API_KEY",
    "large_area": "Z011",
    "format": "json"
}

response = requests.get(url, params=params)
data = response.json()
print(data)
```
### hot pepper api で検索クエリを実行するのに指定しなければいけないもの
以下のうち最低一つ
- id,name,name_kana,name_any,tel
- special
- special_or
- large_service_area,service_area,large_area,middle_area,small_area
- keyword
- lat,lng,range

### 指定した方がいいもの
- JSON形式でデータが欲しいならformat
- データ取得件数を指定するならcount(初期値は10, Min1, MAX100)
  
### データの抽出例
```python
for shop in data['results']['shop']:
    name = shop['name']
    address = shop['address']
    print(f"店名: {name}, 住所: {address}")
```
レスポンスデータは階層構造になっている。詳細は公式のAPIリファレンスを参照  
[リクルートwebサービス APIリファレンス](https://webservice.recruit.co.jp/doc/hotpepper/reference.html)

### エラーハンドリングのサンプルコード
```python
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    # 正常にデータを取得した場合の処理
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```
