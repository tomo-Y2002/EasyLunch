import sys
import os
import yaml
import json
import pickle
from pprint import pformat, pprint

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)
from src.llm.prompt import select_prompt
from src.llm.utils import build_user_prompt_extract
from src.llm.llm_call import LLM

# from src.db.access.chat import ChatDB

with open("config.yaml", encoding="utf-8") as f:
    configs = yaml.safe_load(f)

# chat_db = ChatDB(
#     host=configs["MYSQL_HOST"],
#     user=configs["MYSQL_USER"],
#     password=configs["MYSQL_PASSWORD"],
#     database=configs["MYSQL_DATABASE"],
# )
# conn = chat_db.connect()
# chat_history = chat_db.get(conn=conn, user_id="U461e74eab9cf27cc7e3f034174bc63db")
# chat_db.close(conn)
# with open("./src/test/llm/chat_history_places.pickle", "wb") as f:
#     pickle.dump(chat_history, f)


def main():
    request = "ラーメンに行きたいです"

    # chat_historyをpickleで読み込む
    with open("./src/test/llm/chat_history_places.pickle", "rb") as f:
        chat_history = pickle.load(f)
    prompt_user = build_user_prompt_extract(request, chat_history)
    client = LLM(
        llm_type="claude 3.5 sonnet",
        aws_access_key_id=configs["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=configs["AWS_SECRET_ACCESS_KEY"],
        aws_region_name=configs["AWS_REGION"],
    )
    prompt = client._build_prompt(
        prompt_system=select_prompt("extract_places"),
        image_encoded="",
        prompt_user=prompt_user,
    )
    condition = client.call_retry(mode="extract_places", prompt=prompt)

    # 会話履歴、プロンプト、抽出結果の最初の方を表示
    print("会話履歴:")
    for i, entry in enumerate(chat_history[:3]):  # 最初の3つのエントリーのみ表示
        print(
            f"[{i}] {entry[2]}: {str(entry[3])[:50]}..."
        )  # 各エントリーの最初の50文字を表示
    print("----------------------------------------")
    print("ユーザプロンプト:")
    pp_str = pformat(prompt_user, width=100, compact=True)
    lines = pp_str.split("\n")
    print("\n".join(lines[:10]) + ("\n..." if len(lines) > 10 else ""))
    print("システムプロンプト:")
    pp_str = pformat(prompt, width=100, compact=True)
    lines = pp_str.split("\n")
    print("\n".join(lines[:10]) + ("\n..." if len(lines) > 10 else ""))
    print("----------------------------------------")
    print("抽出結果:")
    pprint(json.loads(condition), width=100, indent=2)

    # print("抽出結果: ")


if __name__ == "__main__":
    main()
