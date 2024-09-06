import sys
import os
import yaml
import datetime
import json

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)
from src.llm.prompt import select_prompt
from src.llm.utils import build_user_prompt_refine
from src.llm.llm_call import LLM

with open("config.yaml", encoding="utf-8") as f:
    configs = yaml.safe_load(f)


def main():
    request = "そうではなくて、ラーメンのお店がみたいです。"
    chat = [
        (
            1,
            "user456",
            "USER",
            "美味しいご飯屋教えてください。",
            datetime.datetime(2024, 8, 31, 8, 46, 54),
        ),
        (
            2,
            "user456",
            "BOT",
            """
[
  {
    "id": "J001274557",
    "name": "御殿",
    "logo_image": "https://imgfp.hotp.jp/SYS/cmn/images/common/diary/custom/m30_img_noimage.gif",
    "name_kana": "ごてん",
    "address": "東京都文京区本郷５-24-2 グレースイマスビル1F",
    "budget_average": "ランチ700円",
    "budget_name": "3001～4000円",
    "catch": "昼はランチ、夜は居酒屋♪ お酒と相性抜群の料理充実",
    "access": "大江戸線「本郷三丁目駅」徒歩2分丸の内線「本郷三丁目駅」徒歩3分本郷三丁目駅から146m",
    "mobile_access": "本郷三丁目駅徒歩3分",
    "urls": "https://www.hotpepper.jp/strJ001274557/?vos=nhppalsa000016",
    "photo_l": "https://imgfp.hotp.jp/IMGH/63/17/P037916317/P037916317_168.jpg",
    "photo_s": "https://imgfp.hotp.jp/IMGH/63/17/P037916317/P037916317_100.jpg",
    "open": "月～金: 11:00～14:00 （料理L.O. 13:30 ドリンクL.O. 13:30）17:00～23:00 （料理L.O. 22:00 ドリンクL.O. 22:00）土: 17:00～23:00 （料理L.O. 22:00 ドリンクL.O. 22:00）",
    "close": "日、祝日"
  },
  {
    "id": "J001293289",
    "name": "つつじ屋",
    "logo_image": "https://imgfp.hotp.jp/IMGH/01/74/P039160174/P039160174_69.jpg",
    "name_kana": "つつじや",
    "address": "東京都文京区弥生１-6-4",
    "budget_average": "",
    "budget_name": "2001～3000円",
    "catch": "",
    "access": "地下鉄南北線東大前駅から徒歩4分",
    "mobile_access": "地下鉄南北線東大前駅から徒歩4分",
    "urls": "https://www.hotpepper.jp/strJ001293289/?vos=nhppalsa000016",
    "photo_l": "https://imgfp.hotp.jp/IMGH/01/75/P039160175/P039160175_168.jpg",
    "photo_s": "https://imgfp.hotp.jp/IMGH/01/75/P039160175/P039160175_100.jpg",
    "open": "月～木、土: 11:00～19:00 （料理L.O. 18:00 ドリンクL.O. 18:30）祝日: 11:00～17:00 （料理L.O. 16:00 ドリンクL.O. 16:00）",
    "close": "金、日"
  },
  {
    "id": "J000681943",
    "name": "養老乃瀧 小石川店",
    "logo_image": "https://imgfp.hotp.jp/IMGH/37/21/P023893721/P023893721_69.jpg",
    "name_kana": "ようろうのたき　こいしかわてん",
    "address": "東京都文京区小石川２-25-18　リブモール小石川102",
    "budget_average": "",
    "budget_name": "2001～3000円",
    "catch": "",
    "access": ".",
    "mobile_access": ".",
    "urls": "https://www.hotpepper.jp/strJ000681943/?vos=nhppalsa000016",
    "photo_l": "https://imgfp.hotp.jp/IMGH/62/06/P021336206/P021336206_168.jpg",
    "photo_s": "https://imgfp.hotp.jp/IMGH/62/06/P021336206/P021336206_100.jpg",
    "open": "月～土、祝日、祝前日: 17:00～翌0:00 （料理L.O. 23:30 ドリンクL.O. 23:30）",
    "close": "日"
  }
]
""",
            datetime.datetime(2024, 8, 31, 8, 46, 55),
        ),
        (
            3,
            "user456",
            "USER",
            "自分的にはラーメンのほうが好きです。",
            datetime.datetime(2024, 8, 31, 8, 46, 56),
        ),
        (
            4,
            "user456",
            "BOT",
            """
[
  {
    "id": "J001285639",
    "name": "ラーメンバル ゆきかげ",
    "logo_image": "https://imgfp.hotp.jp/IMGH/45/88/P038874588/P038874588_69.jpg",
    "name_kana": "らーめんばる　ゆきかげ",
    "address": "東京都文京区根津２-18-3",
    "budget_average": "ランチは1000円前後/ディナーは2000円～",
    "budget_name": "2001～3000円",
    "catch": "1階はカウンター お昼からハッピーアワー★",
    "access": "東京メトロ千代田線「根津」駅/出口1より徒歩1分",
    "mobile_access": "東京ﾒﾄﾛ千代田線｢根津｣駅/出口1より徒歩1分",
    "urls": "https://www.hotpepper.jp/strJ001285639/?vos=nhppalsa000016",
    "photo_l": "https://imgfp.hotp.jp/IMGH/81/47/P040238147/P040238147_168.jpg",
    "photo_s": "https://imgfp.hotp.jp/IMGH/81/47/P040238147/P040238147_100.jpg",
    "open": "月、金: 17:00～21:00 （料理L.O. 21:00 ドリンクL.O. 21:00）火: 11:00～14:00 （料理L.O. 14:00 ドリンクL.O. 14:00）17:00～21:00 （料理L.O. 21:00 ドリンクL.O. 21:00）水: 11:00～14:00 （料理L.O. 13:30 ドリンクL.O. 13:30）17:00～21:00 （料理L.O. 21:00 ドリンクL.O. 21:00）土、日、祝日: 11:00～21:00 （料理L.O. 21:00 ドリンクL.O. 21:00）",
    "close": "木"
  },
  {
    "id": "J001039795",
    "name": "IZASA",
    "logo_image": "https://imgfp.hotp.jp/SYS/cmn/images/common/diary/custom/m30_img_noimage.gif",
    "name_kana": "いざさ",
    "address": "東京都文京区本郷５－２５－１７ドミネンス本郷１０２",
    "budget_average": "750円",
    "budget_name": "1501～2000円",
    "catch": "濃厚！！鶏白湯ラーメン！ クーポンで味玉サービス♪",
    "access": "地下鉄丸の内線本郷三丁目駅、都営大江戸線本郷三丁目駅より徒歩3分",
    "mobile_access": "本郷三丁目駅より徒歩3分",
    "urls": "https://www.hotpepper.jp/strJ001039795/?vos=nhppalsa000016",
    "photo_l": "https://imgfp.hotp.jp/IMGH/05/09/P020100509/P020100509_168.jpg",
    "photo_s": "https://imgfp.hotp.jp/IMGH/05/09/P020100509/P020100509_100.jpg",
    "open": "月～土、祝日、祝前日: 11:00～21:30 （料理L.O. 21:00 ドリンクL.O. 21:00）",
    "close": "日"
  },
  {
    "id": "J001264417",
    "name": "中華料理&横浜家系ラーメン 本郷家 ",
    "logo_image": "https://imgfp.hotp.jp/SYS/cmn/images/common/diary/custom/m30_img_noimage.gif",
    "name_kana": "よこはまいえけいらーめんほんごうや",
    "address": "東京都文京区本郷４丁目1－3",
    "budget_average": "",
    "budget_name": "2001～3000円",
    "catch": "本郷三丁目駅徒歩1分 持ち帰りOK！！",
    "access": "都営大江戸線本郷三丁目駅４出口1分/丸ノ内線本郷三丁目駅１出口2分/三田線春日駅、南北線後楽園駅A2出口徒歩13分",
    "mobile_access": "大江戸線本郷三丁目駅1分/丸ﾉ内線本郷三丁目駅2分",
    "urls": "https://www.hotpepper.jp/strJ001264417/?vos=nhppalsa000016",
    "photo_l": "https://imgfp.hotp.jp/IMGH/47/41/P037424741/P037424741_168.jpg",
    "photo_s": "https://imgfp.hotp.jp/IMGH/47/41/P037424741/P037424741_100.jpg",
    "open": "月～金: 11:00～20:00 （料理L.O. 19:45 ドリンクL.O. 19:45）日: 11:00～15:00 （料理L.O. 14:45 ドリンクL.O. 14:45）",
    "close": "土"
  }
]
""",
            datetime.datetime(2024, 8, 31, 8, 46, 57),
        ),
    ]

    stores_visited = [
        {
            "id": "J001039795",
            "name": "IZASA",
            "logo_image": "https://imgfp.hotp.jp/SYS/cmn/images/common/diary/custom/m30_img_noimage.gif",
            "name_kana": "いざさ",
            "address": "東京都文京区本郷５－２５－１７ドミネンス本郷１０２",
            "budget_average": "750円",
            "budget_name": "1501～2000円",
            "catch": "濃厚！！鶏白湯ラーメン！ クーポンで味玉サービス♪",
            "access": "地下鉄丸の内線本郷三丁目駅、都営大江戸線本郷三丁目駅より徒歩3分",
            "mobile_access": "本郷三丁目駅より徒歩3分",
            "urls": "https://www.hotpepper.jp/strJ001039795/?vos=nhppalsa000016",
            "photo_l": "https://imgfp.hotp.jp/IMGH/05/09/P020100509/P020100509_168.jpg",
            "photo_s": "https://imgfp.hotp.jp/IMGH/05/09/P020100509/P020100509_100.jpg",
            "open": "月～土、祝日、祝前日: 11:00～21:30 （料理L.O. 21:00 ドリンクL.O. 21:00）",
            "close": "日",
        }
    ]
    prompt_user = build_user_prompt_refine(
        request=request,
        chat=chat,
        stores_visited=stores_visited,
    )

    print("ユーザ側のプロンプト")
    print(prompt_user)
    client = LLM(
        llm_type="claude 3.5 sonnet",
        aws_access_key_id=configs["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=configs["AWS_SECRET_ACCESS_KEY"],
        region_name=configs["AWS_REGION"],
    )
    prompt = client._build_prompt(
        prompt_system=select_prompt("refine"),
        image_encoded="",
        prompt_user=prompt_user,
    )
    data = client.call_retry(mode="refine", prompt=prompt)
    print(data)
    data = json.loads(data)
    print(f"id = {data['id']}")


if __name__ == "__main__":
    main()
