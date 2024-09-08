from openai import AzureOpenAI


class AzureClient:
    """
    Azure上のOpenAI APIを利用するためのクライアント
    """

    def __init__(self, azure_api_key: str, azure_endpoint: str, azure_api_version: str):
        self.client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=azure_api_key,
            api_version=azure_api_version,
        )

    def build_prompt(
        self,
        prompt_system: str = "",
        image_encoded: str = "",
        prompt_user: str = "",
    ):
        """
        prompt を生成するメソッド
        Args:
            prompt_user : ユーザーのリクエスト
            prompt_system : システムプロンプト。モデルの出力の条件付けを行う
            image_encoded : 画像の base64 エンコードされたもの
        Returns:
            list形式のbody
        """
        prompt = []
        if prompt_system:
            prompt.append(
                {
                    "role": "system",
                    "content": prompt_system,
                }
            )
        message_user = {
            "role": "user",
            "content": [],
        }
        if image_encoded:
            image_url = f"data:image/png;base64,{image_encoded}"
            message_user["content"].append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                    },
                }
            )

        if prompt_user:
            message_user["content"].append(
                {
                    "type": "text",
                    "text": prompt_user,
                }
            )

        prompt.append(message_user)

        return prompt

    def call(self, prompt: list, max_tokens: int = 1024, temperature: float = 0.1):
        """
        Azure OpenAIのgpt4-o を call するメソッド
        Args:
            body (dict): API に渡す list
            self.build_prompt を通じて生成されたリスト形式のデータを受け付ける
            max_tokens (int): 生成されるトークンの最大数
            temperature (float): 出力のランダム度合い
        """
        response = self.client.chat.completions.create(
            model="aoai-gpt-4o",
            messages=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content
