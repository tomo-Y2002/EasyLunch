import sys
import os
import yaml
import argparse

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)

from src.llm.llm_call import LLM
from src.llm.utils import encode_image_from_path


with open("config.yaml", encoding="utf-8") as f:
    configs = yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="Choose LLM type for processing.")
    parser.add_argument(
        "-t",
        "--llm_type",
        type=str,
        default="claude 3.5 sonnet",
        help="Type of LLM to use.",
    )
    args = parser.parse_args()

    client = LLM(
        llm_type=args.llm_type,
        aws_access_key_id=configs["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=configs["AWS_SECRET_ACCESS_KEY"],
        region_name=configs["AWS_REGION"],
    )
    image_encoded, _ = encode_image_from_path("data/test/image.png")
    prompt = client._build_prompt(
        prompt_system="あなたは語尾が「なんだな」で終わるようなおじさんです。おじさんとして、以下のUserの質問に答えてください。",
        image_encoded=image_encoded,
        prompt_user="画像は何を表していますか？",
    )
    response = client.call(prompt=prompt, max_tokens=1024, temperature=0.1)
    print(response)


if __name__ == "__main__":
    main()
