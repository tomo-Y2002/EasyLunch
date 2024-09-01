## ディレクトリの説明
**aws.py**  
aws bedrockを使用してLLM(claude 3.5 sonnet)に問い合わせるクラス```AWSBedrockClient```を持つ。

**llm_call.py**  
使用したいモデルに応じてクライアントを選択して問い合わせをするクラス```LLM```を持つ。
現在 aws.pyに存在する ```AWSBedrockClinet``` のみ選択可能。

**utils.py**  
画像をbase64エンコーディングするなどの汎用的関数を保存してある。

**prompt.py**  
LLMに問い合わせるプロンプトのテンプレートを将来置く。