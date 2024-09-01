import yaml

from src.llm.aws import AWSBedrockClient

with open("config.yaml", encoding="utf-8") as f:
    configs = yaml.safe_load(f)


class LLM:
    """
    LLM のクライアントクラス
    aws bedrock, cotomi, azure openai に対応予定
    """

    def __init__(self, llm_type: str):
        if llm_type == "claude 3.5 sonnet":
            self.client = AWSBedrockClient(configs)
        else:
            raise ValueError("Invalid type")

    def _build_prompt(
        self,
        prompt_system: str,
        image_encoded: str,
        prompt_user: str,
    ):
        """
        clientに適したprompt を生成するwrapperメソッド
        Args:
            prompt_user : ユーザーのリクエスト
            prompt_system : システムプロンプト。モデルの出力の条件付けを行う
            prompt_image : 画像の base64 エンコードされたもの
        Returns:
            dict形式のprompt
        """
        return self.client.build_prompt(prompt_system, image_encoded, prompt_user)

    def call(self, prompt: dict, max_tokens: int = 1024, temperature: float = 0.1):
        """
        cilent のcallメソッドを呼び出すwrapperメソッド
        Args:
            prompt : self._build_prompt の返り値として整形されたdict
            max_tokens : 最大トークン数
            temperature : 出力のランダム度合い
        """
        return self.client.call(
            prompt=prompt, max_tokens=max_tokens, temperature=temperature
        )
