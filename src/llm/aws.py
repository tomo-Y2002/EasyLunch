import boto3
import json
from botocore.exceptions import ClientError


class AWSBedrockClient:
    """
    AWS Bedrock API をcall するクライアントクラス
    現状 Claude 3.5 Sonnet のみに対応している。
    """

    def __init__(
        self, aws_access_key_id: str, aws_secret_access_key: str, aws_region_name: str
    ):
        self.session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region_name,
        )
        self.client = self.session.client(service_name="bedrock-runtime")
        self.model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"

    def build_prompt(
        self,
        prompt_system: str,
        image_encoded: str,
        prompt_user: str,
    ):
        """
        prompt を生成するメソッド
        Args:
            prompt_user : ユーザーのリクエスト
            prompt_system : システムプロンプト。モデルの出力の条件付けを行う
            prompt_image : 画像の base64 エンコードされたもの
        Returns:
            json形式のbody
        """
        prompt = {
            "anthropic_version": "bedrock-2023-05-31",
        }
        if prompt_system:
            prompt["system"] = prompt_system

        messages = []
        user_message = {
            "role": "user",
            "content": [],
        }
        if image_encoded:
            user_message["content"].append(
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_encoded,
                    },
                }
            )
        if prompt_user:
            user_message["content"].append(
                {
                    "type": "text",
                    "text": prompt_user,
                }
            )
        messages.append(user_message)
        prompt["messages"] = messages
        return prompt

    def call(self, prompt: dict, max_tokens: int = 1024, temperature: float = 0.1):
        """
        AWS Bedrock API を call するメソッド
        Args:
            body (dict): API に渡す json
            self.build_prompt を通じて生成された辞書型のデータを受け付ける
            max_tokens (int): 生成されるトークンの最大数
            temperature (float): 出力のランダム度合い
        """
        prompt["max_tokens"] = max_tokens
        prompt["temperature"] = temperature
        body = json.dumps(prompt)
        try:
            response = self.client.invoke_model(modelId=self.model_id, body=body)
        except (ClientError, Exception) as e:
            print(f"ERROR: Can't invoke '{self.model_id}'. Reason: {e}")
            exit(1)
        response_body = json.loads(response.get("body").read())
        return response_body["content"][0]["text"]
