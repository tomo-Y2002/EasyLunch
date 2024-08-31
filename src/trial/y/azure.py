from openai import AzureOpenAI
import yaml

with open("../../../config.yaml", "r") as f:
    config = yaml.safe_load(f)
AZURE_API_KEY = config["AZURE_API_KEY"]
AZURE_BASE_URL = config["AZURE_BASE_URL"]

# クライアントインスタンスの生成。接続先の設定。
client = AzureOpenAI(
    api_key=AZURE_API_KEY,
    api_version="2024-05-13",
    azure_endpoint=AZURE_BASE_URL,
)

# GPTモデルのインスタンス作成。API呼び出し
response = client.chat.completions.create(
    model="aoai-gpt-4o",  # モデルの名前
    messages=[
        {"role": "user", "content": "消費税について200文字以内で教えて"}
    ],  # 入力するプロンプト
    temperature=0.7,  # 出力のランダム度合い(可変)
    max_tokens=800,  # 最大トークン数(固定)
    top_p=0.95,  # 予測する単語を上位何%からサンプリングするか(可変)
    frequency_penalty=0,  # 単語の繰り返しをどのくらい許容するか(可変)
    presence_penalty=0,  # 同じ単語をどのくらい使うか(可変)
    stop=None,  # 文章生成を停止する単語を指定する(可変)
)

# GPTの出力を表示
print(response.choices[0].message.content.strip())
