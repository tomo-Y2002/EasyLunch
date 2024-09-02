import sys
import os
import yaml
import argparse
import json

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)
from src.llm.prompt import select_prompt
from src.llm.llm_call import LLM

# from src.api.hot_pepper import HotPepperApi
from src.llm.utils import check_parse_extract

with open("config.yaml", encoding="utf-8") as f:
    configs = yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(
        description="specify conditions for restaurant search"
    )
    parser.add_argument(
        "-p",
        "--prompt",
        type=str,
        default="予算3000円以内で銀座のレストランを検索して。食べ放題で夜景が綺麗だと嬉しいです。",
        help="Prompt to use.",
    )
    args = parser.parse_args()

    client = LLM(llm_type="claude 3.5 sonnet")  #
    prompt = client._build_prompt(
        prompt_system=select_prompt("extract"),
        image_encoded="",
        prompt_user=args.prompt,
    )

    while True:
        response = client.call(prompt=prompt, max_tokens=1024, temperature=0.1)
        print("extract result: ", response)

        try:
            data = json.loads(response)
            if check_parse_extract(data):
                break
            else:
                print("Parsed json is invalid. Retrying...")
        except Exception as e:
            print(e)
            print("Failed to parse json. Retrying...")

    # print(response)
    # api = HotPepperApi()
    # stores = api.search_restaurant_essential(response, count=5)
    # api.print_store_name(stores)


if __name__ == "__main__":
    main()
