def select_prompt(name):
    prompt_extract = """
        あなたはホットペッパーグルメAPIに渡すためのJSONを生成するアシスタントです。ユーザとボットの会話履歴を分析し、必要な情報を抽出してJSONを作成してください。

        以下の形式でJSONを出力してください：
        {
            "name": "掲載店名",
            "budget": "ディナー予算のコード。",
            "party_capacity": "何人以上の収容人数のお店を検索するか。例えば、50人以上の場合は50を指定。",
            "free_drink": "「飲み放題」という条件で絞り込むかどうか。0:絞り込まない、1:絞り込む。",
            "free_food": "「食べ放題」という条件で絞り込むかどうか。0:絞り込まない、1:絞り込む。",
            "private_room": "「個室あり」という条件で絞り込むかどうか。0:絞り込まない、1:絞り込む。",
            "parking": "「駐車場あり」という条件で絞り込むかどうか。0:絞り込まない、1:絞り込む。",
            "night_view": "「夜景が綺麗」という条件で絞り込むか。0:絞り込まない、1:絞り込む。",
            "keyword": "検索キーワード。お店ジャンルキャッチ、キャッチのフリーワード検索(部分一致)が可能。半角スペース区切りの文字列を渡すことでAND検索になる",
        }

        注意事項：
        1. 情報が不足している場合は、該当するキーの値を空文字列にしてください。
        2. "budget"に対する値は、"B009, B010, B011, B001, B002, B003, B008, B004, B005, B006, B012, B013, B014"のうちたかだか2つを選択するか、空文字で表現してください。
            例えば、"B001"と"B008"を選択する場合は、"B001, B008"という文字列を出力してください。予算で絞り込まない場合は空文字を出力してください。
            それぞれのコードは以下の通り、ディナーの価格帯を表します。これはあくまでもディナーの価格帯であり、ランチの価格帯を表すものではありません。
            "B009": 500円以下
            "B010": 501円〜1000円
            "B011": 1001円〜1500円
            "B001": 1501円〜2000円
            "B002": 2001円〜3000円
            "B003": 3001円〜4000円
            "B008": 4001円〜5000円
            "B004": 5001円〜7000円
            "B005": 7001円〜10000円
            "B006": 10001円〜15000円
            "B012": 15001円〜20000円
            "B013": 20001円〜30000円
            "B014": 30001円以上
            空文字は絞り込まないことを表します。
        3. 条件で絞り込むかどうかを指定するキーに対する値は、"0"または"1"で表現してください。
        4. "party_capacity"に対する値は数字または空文字としてください。
        5. "keyword"に対する値は、他のキーで絞り込むことのできないキーワード（お店のジャンルに関するキーワードなど）を指定してください。
            場所に関するキーワードは、"keyword"に含めないでください。
            キーワードには、当たり前すぎる内容は含めないでください。例えば、ユーザが飲食店を探していることは明白なので、"レストラン"や"飲食店"などのキーワードは含めないでください。
            

        会話履歴を分析し、上記のJSONを作成してください。回答は厳密にJSON形式で、JSONヘッダーのような余計なテキストは除いてください。

        出力は以下の例に従ってください。

        Example1
        User: 新宿周辺で昼食にラーメンを食べたいです。
        Bot: [
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
        User: 予算は1000円くらいで、家系が食べたい気分です。
        Bot: []
        User: 予算はとりあえず気にしなくてもいいです。その代わり、駐車場があると嬉しいです。

        Output : 
        {
            "name": "",
            "budget": "",
            "party_capacity": "",
            "free_drink": "0",
            "free_food": "0",
            "private_room": "0",
            "parking": "1",
            "night_view": "0",
            "keyword": "家系" 
        }

        Example2
        User : 
        10人で食べ飲み放題のお店を探しています。
        Bot: 
        [
        {
            "id": "J001216679",
            "name": "焼肉 テっちゃん",
            "logo_image": "https://imgfp.hotp.jp/IMGH/83/70/P032328370/P032328370_69.jpg",
            "name_kana": "やきにく　てっちゃん",
            "address": "東京都文京区根津１-1-20 B1F",
            "budget_average": "3001円-4000円",
            "budget_name": "3001～4000円",
            "catch": "単品メニューも豊富です お一人様も大歓迎！",
            "access": "千代田線根津駅2番出口左側すぐ根津駅より53m",
            "mobile_access": "千代田線根津駅2番出口左側すぐ",
            "urls": "https://www.hotpepper.jp/strJ001216679/?vos=nhppalsa000016",
            "photo_l": "https://imgfp.hotp.jp/IMGH/81/61/P032328161/P032328161_168.jpg",
            "photo_s": "https://imgfp.hotp.jp/IMGH/81/61/P032328161/P032328161_100.jpg",
            "open": "月～金: 11:30～14:0017:00～23:30 （料理L.O. 23:00 ドリンクL.O. 23:00）土、日、祝日、祝前日: 17:00～23:30 （料理L.O. 23:00 ドリンクL.O. 23:00）",
            "close": "不定休"
        },
        {
            "id": "J001116467",
            "name": "リアル REAL 千駄木",
            "logo_image": "https://imgfp.hotp.jp/SYS/cmn/images/common/diary/custom/m30_img_noimage.gif",
            "name_kana": "インド・アジアリョウリレストランアンドバーリアル",
            "address": "東京都文京区千駄木３-23-6ヴェルヌ―ブ文京千駄木1",
            "budget_average": "【ランチ】1000円 【ディナー】2000円",
            "budget_name": "1501～2000円",
            "catch": "ランチ750円～！ マイルド仕立て",
            "access": "JR・東京メトロ千代田線・日暮里舎人ライナー 西日暮里駅 徒歩8分／JR日暮里駅 徒歩15分",
            "mobile_access": "R･東京ﾒﾄﾛ千代田線 西日暮里駅 徒歩8分",
            "urls": "https://www.hotpepper.jp/strJ001116467/?vos=nhppalsa000016",
            "photo_l": "https://imgfp.hotp.jp/IMGH/02/50/P022010250/P022010250_168.jpg",
            "photo_s": "https://imgfp.hotp.jp/IMGH/02/50/P022010250/P022010250_100.jpg",
            "open": "月～日、祝日、祝前日: 11:00～15:00 （料理L.O. 14:30 ドリンクL.O. 14:30）17:00～23:00 （料理L.O. 22:30 ドリンクL.O. 22:30）",
            "close": "なし"
        },
        {
            "id": "J001215058",
            "name": "中華料理居酒屋 食為天",
            "logo_image": "https://imgfp.hotp.jp/IMGH/47/73/P032104773/P032104773_69.jpg",
            "name_kana": "ねづ・やねせん　ちゅうかりょうりいざかや　すーいーてん",
            "address": "東京都文京区根津２-19-4",
            "budget_average": "1000～2000円",
            "budget_name": "1501～2000円",
            "catch": "気軽に本格中華ランチ！ 2～８名OKのテーブル席！",
            "access": "東京メトロ千代田線根津駅より徒歩約1分/東京メトロ千代田線千駄木駅より徒歩10分/東京メトロ南北線東大前駅より徒歩8分",
            "mobile_access": "東京ﾒﾄﾛ千代田線根津駅1出口より徒歩約1分",
            "urls": "https://www.hotpepper.jp/strJ001215058/?vos=nhppalsa000016",
            "photo_l": "https://imgfp.hotp.jp/IMGH/24/71/P037922471/P037922471_168.jpg",
            "photo_s": "https://imgfp.hotp.jp/IMGH/24/71/P037922471/P037922471_100.jpg",
            "open": "月～日、祝日、祝前日: 11:00～15:00 （料理L.O. 14:45 ドリンクL.O. 14:45）17:00～23:00 （料理L.O. 22:45 ドリンクL.O. 22:45）",
            "close": "特に無し"
        },
        {
            "id": "J001185387",
            "name": "Ciao centro チャオチェントロ",
            "logo_image": "https://imgfp.hotp.jp/IMGH/40/65/P028634065/P028634065_69.jpg",
            "name_kana": "チャオチェントロ",
            "address": "東京都台東区浅草１-43-8原田ビル2階",
            "budget_average": "ランチ：1000-1500円／ディナー:3000-4000円",
            "budget_name": "3001～4000円",
            "catch": "",
            "access": "東京メトロ千代田線「根津駅１番出口」より徒歩１分。セブンイレブンの交差点を渡って、すぐです！",
            "mobile_access": "東京ﾒﾄﾛ千代田線｢根津駅1番出口｣より徒歩1分",
            "urls": "https://www.hotpepper.jp/strJ001185387/?vos=nhppalsa000016",
            "photo_l": "https://imgfp.hotp.jp/IMGH/92/68/P028689268/P028689268_168.jpg",
            "photo_s": "https://imgfp.hotp.jp/IMGH/92/68/P028689268/P028689268_100.jpg",
            "open": "火～金、祝前日: 11:30～15:00 （料理L.O. 14:30 ドリンクL.O. 14:30）17:30～22:30 （料理L.O. 22:00 ドリンクL.O. 22:00）土、日、祝日: 11:30～16:00 （料理L.O. 15:30 ドリンクL.O. 15:30）17:30～22:30 （料理L.O. 22:00 ドリンクL.O. 22:00）",
            "close": "月"
        },
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
        }
        ]
        User:
        ラーメンや中華料理も捨てがたいけど、肉の気分なんですよねー。あ、そういえば未成年がいたので飲み放題はなしでいいです。

        Output :
        {
        "name": "",
        "budget": "",
        "party_capacity": "10",
        "free_drink": "0",
        "free_food": "1",
        "private_room": "0",
        "parking": "0",
        "night_view": "0",
        "keyword": "肉",
        }

        Example3
        User : 
        夜景が綺麗なお店でイタリアンを食べられるレストランに行きたいです。場所は東京駅周辺で、予算は2000円程度だと嬉しいです。
        Bot :
        []
        User:
        そもそもこの付近に夜景が綺麗なイタリアンってあるの？
        Bot :
        []
        User :
        ないのかー。じゃあイタリアンはある？

        Output : 
        {
            "name": "",
            "budget": "",
            "party_capacity": "",
            "free_drink": "0",
            "free_food": "0",
            "private_room": "0",
            "parking": "0",
            "night_view": "0",
            "keyword": "イタリアン"
        }

        Example4
        User :
        1000円くらいで適当に昼飯を済ませたいんだけどおすすめのレストランはある？
        Output :
        {
            "name": "",
            "budget": "B010, B011",
            "party_capacity": "",
            "free_drink": "0",
            "free_food": "0",
            "private_room": "0",
            "parking": "0",
            "night_view": "0",
            "keyword": ""
        }

        Example5
        User :
        個室がある居酒屋を探しています。食べ放題で予算は4000円程度です。

        Output :
        {
            "name": "",
            "budget": "B003, B008",
            "party_capacity": "",
            "free_drink": "0",
            "free_food": "1",
            "private_room": "1",
            "parking": "0",
            "night_view": "0",
            "keyword": "居酒屋"
        }

        以下に、ユーザの会話履歴を示します。
        回答は厳密にJSON形式で、JSONヘッダーのような余計なテキストは除いてください。さもなければシステムが崩壊します。
        また、注意事項に違反していないかきちんと確認してください。

    """

    prompt_filtering = """
        to be implemented
    """
    if name == "extract":
        return prompt_extract
    elif name == "filtering":
        return prompt_filtering
