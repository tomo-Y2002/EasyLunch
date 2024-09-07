import json

from src.llm.aws import AWSBedrockClient
from src.llm.azure import AzureClient
from src.llm.utils import check_parse_extract, check_parse_refine, check_parse_filter


class LLM:
    """
    LLM のクライアントクラス
    aws bedrock, cotomi, azure openai に対応予定
    """

    def __init__(
        self,
        llm_type: str,
        aws_access_key_id: str = "",
        aws_secret_access_key: str = "",
        aws_region_name: str = "",
    ):
        if llm_type == "claude 3.5 sonnet":
            if (
                aws_access_key_id == ""
                or aws_secret_access_key == ""
                or aws_region_name == ""
            ):
                raise ValueError("Invalid args")
            self.client = AWSBedrockClient(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                aws_region_name=aws_region_name,
            )
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

    def _check_parse(self, mode: str, response: str):
        """
        llmのjsonの形式が正しいのかをmodeに応じてチェックする
        Args:
            mode : チェックするモード。"extract", "refine", "filter" のいずれか
            reponse : llmの出力
        Returns:
            bool : 正しい形式の場合はTrue, それ以外はFalse
        """
        if mode == "extract":
            data = json.loads(response)
            return check_parse_extract(data)
        elif mode == "refine":
            data = json.loads(response)
            return check_parse_refine(data)
        elif mode == "filter":
            data = json.loads(response)
            return check_parse_filter(data)
        else:
            raise ValueError("Invalid mode")

    def call_retry(
        self, mode: str, prompt: str, max_tokens: int = 1024, temperature: float = 0.1
    ):
        """
        callメソッドがjson出力に失敗する場合にリトライを行うようにする
        Args:
            mode : チェックするモード。"extract", "refine", "filter" のいずれか
            prompt : llmに入力するprompt
        Returns:
            response : llmの出力
        """
        while True:
            response = self.call(
                prompt=prompt, max_tokens=max_tokens, temperature=temperature
            )

            try:
                if self._check_parse(mode, response):
                    break
                else:
                    print("Parsed json is invalid. Retrying...")
            except Exception as e:
                print(e)
                print("Failed to parse json. Retrying...")
        return response
