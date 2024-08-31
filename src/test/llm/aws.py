import sys
import os
import yaml

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)

from src.llm.aws import AWSBedrockClient

with open("config.yaml", encoding="utf-8") as f:
    configs = yaml.safe_load(f)


def main():
    client = AWSBedrockClient(configs)
    body = client.build_prompt(
        prompt_system="あなたは語尾が「なんだな」で終わるようなおじさんです。おじさんとして、以下のUserの質問に答えてください。",
        image_encoded=None,
        prompt_user="おじさん、今日は何を食べましたか？",
    )
    response = client.call(body)
    print(response)


if __name__ == "__main__":
    main()
