import os
import base64
from typing import Optional
from typing import Union
import json


def encode_image_from_path(image_path: str, mime_type: Optional[str] = None) -> str:
    """
    Encode an image file to base64 string.
    :param image_path: The path of the image file.
    :param mime_type: The mime type of the image.
    :return:
        encoded_image: The base64 encoded image string.
        mime_type: The mime type of the image.
    """
    import mimetypes

    file_name = os.path.basename(image_path)
    mime_type = (
        mime_type if mime_type is not None else mimetypes.guess_type(file_name)[0]
    )
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("ascii")

    if mime_type is None or not mime_type.startswith("image/"):
        print(
            "Warning: mime_type is not specified or not an image mime type. Defaulting to png."
        )
        mime_type = "image/png"

    return encoded_image, mime_type


def check_parse_extract(condition: Union[dict, str]) -> bool:
    """
    LLMで情報抽出した結果が正しいJSONかをチェックする
    """
    try:
        if isinstance(condition, str):
            condition = json.loads(condition)
        if (
            "name" in condition
            and "budget" in condition
            and "party_capacity" in condition
            and "free_drink" in condition
            and "free_food" in condition
            and "private_room" in condition
            and "parking" in condition
            and "night_view" in condition
            and "keyword" in condition
        ):
            if (
                condition["free_drink"] in ["0", "1"]
                and condition["free_food"] in ["0", "1"]
                and condition["private_room"] in ["0", "1"]
                and condition["parking"] in ["0", "1"]
                and condition["night_view"] in ["0", "1"]
            ):
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        print(e)
        return False


def check_parse_refine(data: json):
    """
    来店履歴を用いた検索候補のrefineに関するllmのjson出力が正しいのかをチェックする
    """
    try:
        if "thought" in data and "id" in data:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def check_parse_filter(data: dict):
    """
    問い合わせのフィルタリングに関するllmのjson出力が正しいのかをチェックする
    """
    pass


def build_user_prompt_refine(
    request: str, chat: list, stores_visited: list, num_chat: int = 2
):
    """
    来店履歴のなかから、ユーザの要求に合致する店舗があれば抽出する動作のためのuser promptを生成する
    プロンプトの肥大化を
    Args:
        request : ユーザの最新の発話
        chat : ユーザとBOTの会話履歴
        例) [(1, 'user456', 'USER', '家系が食べたいです。', datetime.datetime(2024, 8, 31, 8, 46, 54))]
        stores : グルメAPIからの検索結果の店舗情報
        stores_visited : 来店履歴DBから取得したstore_idを用いて、グルメAPIで取得した店舗情報 (storesと同じ構造)
    Returns:
        prompt : LLMに入力するprompt
    """
    chat_formed = ""
    for idx, remark in enumerate(chat[:num_chat]):  # 会話履歴の最新2つを取得
        if remark[2] == "USER":
            chat_formed += f"[{idx}] USER : \n{remark[3]}\n"
        elif remark[2] == "BOT":
            # BOT発言における、不要な情報削除の部分は To Do
            chat_formed += f"[{idx}] BOT : {remark[3]}\n"

    stores_visited_formed = ""
    for idx, store in enumerate(stores_visited):
        stores_visited_formed += (
            f"Store {idx+1}\n {json.dumps(store, ensure_ascii=False, indent=2)}\n"
        )

    prompt = f"""
Visited Stores :
{stores_visited_formed}
--------------------------------
Chat History : 
{chat_formed}
--------------------------------
Latest User Request : 
{request} 
"""
    return prompt
