import json
import copy


def create_carousel(
    userId: str, stores: list, template_path="./src/line/template.json", num: int = 5
) -> str:
    """
    storesのリストをもとに、flex messageを作成する関数

    Parameters
    ----------
    stores : list
        ストアのリスト
    template_path : str, optional
        Flexメッセージのテンプレートファイルのパス。デフォルトは"./src/line/template.json"。

    Returns
    -------
    data : str
        flex message
    """
    data = {"type": "carousel", "contents": []}
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template = json.load(f)
    except FileNotFoundError:
        print(f"テンプレートファイル '{template_path}' が見つかりません。")
        raise
    except json.JSONDecodeError as e:
        print(f"JSONファイルの解析エラー: {e}")
        raise
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        raise

    for store in stores[:num]:  # numの個数に制限する
        contents_format = copy.deepcopy(template)
        if store["name"] == "":
            name = "店の名前がありません"
        else:
            name = store["name"]
        if store["photo_l"] == "":
            img = "https://imgfp.hotp.jp/IMGH/83/70/P032328370/P032328370_69.jpg"
        else:
            img = store["photo_l"]
        if store["catch"] == "":
            catch = "キャッチコピーがありません"
        else:
            catch = store["catch"]
        if store["address"] == "":
            address = "住所がありません"
        else:
            address = store["address"]
        if store["budget_name"] == "":
            price = "予算がありません"
        else:
            price = store["budget_name"]
        if store["urls"] == "":
            uri = "https://www.hotpepper.jp"
        else:
            uri = store["urls"]
        if store["id"] == "":
            id = "J001216679"
        else:
            id = store["id"]
        contents_format["header"]["contents"][0]["text"] = name
        contents_format["hero"]["url"] = img
        contents_format["body"]["contents"][1]["contents"][0]["text"] = catch
        contents_format["body"]["contents"][3]["text"] = address
        contents_format["body"]["contents"][4]["text"] = price
        contents_format["body"]["contents"][5]["contents"][0]["action"]["uri"] = uri
        contents_format["body"]["contents"][5]["contents"][1]["action"]["data"] = (
            "店のid" + id
        )

        data["contents"].append(contents_format)

    carousel = {
        # userIDを指定。
        "to": userId,
        "messages": [
            {
                "type": "flex",
                "altText": "This is a Flex Message",
                "contents": data,
            }
        ],
    }
    return carousel


# 送信されたメッセージからuserIdを取得する
def get_id(event):
    """
    送信されたメッセージからユーザーIDを取得します。

    Parameters
    ----------
    event : MessageEvent
        LINEプラットフォームから受け取ったメッセージイベント。

    Returns
    -------
    str
        メッセージを送信したユーザーのID。
    """
    return event.source.user_id
