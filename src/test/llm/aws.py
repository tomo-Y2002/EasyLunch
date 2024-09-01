import sys
import os
import yaml

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)

from src.llm.aws import AWSBedrockClient
from src.llm.utils import encode_image_from_path

with open("config.yaml", encoding="utf-8") as f:
    configs = yaml.safe_load(f)


def main():
    client = AWSBedrockClient(configs)
    image_encoded, _ = encode_image_from_path("data/test/image.png")
    prompt = client.build_prompt(
        prompt_system="あなたは語尾が「なんだな」で終わるようなおじさんです。おじさんとして、以下のUserの質問に答えてください。",
        image_encoded=image_encoded,
        prompt_user="画像は何を表していますか？",
    )
    response = client.call(prompt=prompt, max_tokens=1024, temperature=0.1)
    print(response)


if __name__ == "__main__":
    main()
