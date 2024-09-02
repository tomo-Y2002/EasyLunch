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
