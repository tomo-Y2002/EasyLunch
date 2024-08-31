import boto3
import json
from botocore.exceptions import ClientError


class AWSBedrockClient:
    """
    AWS Bedrock API をcall するクライアントクラス
    現状 Claude 3.5 Sonnet のみに対応している。
    """

    def __init__(self, configs):
        self.session = boto3.Session(
            aws_access_key_id=configs["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=configs["AWS_SECRET_ACCESS_KEY"],
            region_name=configs["AWS_REGION"],
        )
        self.client = self.session.client(service_name="bedrock-runtime")
        self.modelId = "anthropic.claude-3-5-sonnet-20240620-v1:0"

    def build_prompt(
        self,
        prompt_system: str,
        image_encoded: str,
        prompt_user: str,
        max_tokens: int = 1024,
        temperature: float = 0.1,
    ):
        """
        prompt を生成するメソッド
        Args:
            prompt_user : ユーザーのリクエスト
            prompt_system : システムプロンプト。モデルの出力の条件付けを行う
            prompt_image : 画像の base64 エンコードされたもの
            max_tokens : 生成するトークンの最大数
            temperature : 生成時のランダム性
        Returns:
            json形式のbody
        """
        prompt = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if prompt_system:
            prompt["system"] = prompt_system

        messages = []
        if image_encoded:
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_encoded,
                            },
                        }
                    ],
                }
            )

        if prompt_user:
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_user,
                        }
                    ],
                }
            )

        prompt["messages"] = messages
        return json.dumps(prompt)

    def call(self, body: json):
        """
        AWS Bedrock API を call するメソッド
        Args:
            body (json): API に渡す json
            self.build_prompt を通じて生成された辞書型のデータを受け付ける
        """
        try:
            response = self.client.invoke_model(modelId=self.modelId, body=body)
        except (ClientError, Exception) as e:
            print(f"ERROR: Can't invoke '{self.modelId}'. Reason: {e}")
            exit(1)
        response_body = json.loads(response.get("body").read())
        return response_body["content"][0]["text"]
