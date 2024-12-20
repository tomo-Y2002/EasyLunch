def select_prompt(name):
    prompt_extract = """
あなたはホットペッパーグルメAPIに渡すためのJSONを生成するアシスタントです。
ユーザとボットの会話履歴が与えられるので、それを分析し、ユーザの希望を所定の形式で抽出してJSONを作成してください。

以下の形式でJSONを出力してください：
{
    "thoughts": "チャット履歴からなぜそのような抽出条件を設定したかを述べる。",
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

[Input]
Chat History :
[0] User: 新宿周辺で昼食にラーメンを食べたいです。
[1] Bot: [
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
[2] User: 家系が食べたい気分です。あと個室があるとありがたいのですが条件を満たすお店はある？
[3] Bot: []

--------------------------------
Latest User Request :
ないですか。家系で駐車場のある店はある？予算は1000円くらいで。

[Output]
{
    "thoughts": "ユーザは昼食に駐車場付きのラーメン屋で1000円程度の価格帯の家系を食べたいと思っている。budgetはディナーの価格帯であり昼食には関係ない。したがって"parking":1と"keyword":家系のみを指定すれば良い。",
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

[Input]
Chat History :
[0] User : 
10人で食べ飲み放題のお店を探しています。
[1] Bot: 
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

--------------------------------
Latest User Request :
ラーメンや中華料理も捨てがたいけど、肉の気分なんですよねー。あ、そういえば未成年がいたので飲み放題はなしでいいです。

Output :
{
"thoughts": "ユーザは10人で食べ放題のお店で、肉を提供してくれるお店を探している。そのため、"party_capacity":"10"、"free_food":"1"、"keyword":"肉"と指定する。",
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

[Input]
Chat History :
[0] User : 
夜景が綺麗なお店でイタリアンを食べられるレストランに行きたいです。場所は東京駅周辺で、予算は2000円程度だと嬉しいです。
[1] Bot :
[]
[2] User:
そもそもこの付近に夜景が綺麗なイタリアンってあるの？
[3] Bot :
[]

--------------------------------
Latest User Request :
ないのかー。じゃあイタリアンはある？

[Output] 
{
    "thoughts": "ユーザは初め2000円程度の夜景が綺麗なイタリアンを食べたいと思っていたが、最終的にはイタリアンのみを指定している。そのため、"keyword":"イタリアン"を指定する。",
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
[Input]
Chat History :

--------------------------------
Latest User Request :
1000円くらいで適当に昼飯を済ませたいんだけどおすすめのレストランはある？
Output :
{
    "thoughts": "ユーザは1000円で昼食を済ませたいと思っている。"budget"はディナーの価格帯なので、昼食の価格帯を絞り込むのには使えない。また、"レストラン"をキーワードにすることは注意事項に反しているので、何も条件を絞り込まない。",
    "name": "",
    "budget": "",
    "party_capacity": "",
    "free_drink": "0",
    "free_food": "0",
    "private_room": "0",
    "parking": "0",
    "night_view": "0",
    "keyword": ""
}

Example5
[Input]
Chat History :

--------------------------------
Latest User Request :
個室がある居酒屋を探しています。食べ放題で予算は4000円程度です。

Output :
{
    "thoughts": "ユーザは4000円で食べ放題で個室がある居酒屋を探している。居酒屋を利用するのはだいたい夜なので、"budget"でB003, B008を指定する。また食べ放題、個室があることを指定するために"free_food"と"private_room"を"1"に指定し、"keyword"に"居酒屋"を指定する。",
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
    prompt_extract_places = """
あなたはGoogle Places APIのText Search (New)に入力するクエリを生成するためのアシスタントです。
以下にユーザとボットの会話履歴が与えられます。ユーザは飲食店を問う質問をし、botはその条件にあった店を推薦しています。
あなたはその会話履歴を分析し、ユーザの希望を所定の形式で抽出してJSONを作成してください。

以下の形式でJSONを出力してください：
{
"thoughts": "チャット履歴からなぜそのような抽出条件を設定したかを述べる。",
"keyword": "検索キーワード。料理のジャンルや店名、その他ユーザの希望を表すキーワードを指定する。"
}

注意事項：
1. あなたが出力するキーワードを元に検索を行うGoogle Places APIのText Search (New)は、飲食店のみを検索の対象となるように設定しているので、"keyword"に"レストラン"や"飲食店"といった自明なキーワードは指定しないでください。
2. "keyword"には、曖昧すぎるワードは使用しないでください。例えば、ユーザが「夏っぽいものを食べたい」と言っていたとしても、"keyword"に"夏"や"夏っぽい"などの言葉は使用せず、"冷やし中華"や"そうめん"などのより具体的な言葉を使用してください
以下の会話履歴を分析し、上記のJSONを作成してください。回答は厳密にJSON形式で、JSONヘッダーのような余計なテキストは除いてください。

出力は以下の例に従ってください。

Example1

[Input]
Chat History :
[0] User: 昼食にラーメンを食べたいです。
[1] Bot: [
{
"id": "J001039795",
"name": "IZASA",
"latitude": 35.7123,
"longitude": 139.7456,
"rating": 4.2,
"urls": "https://www.hotpepper.jp/strJ001039795/?vos=nhppalsa000016",
"price_level": "PRICE_LEVEL_INEXPENSIVE",
"photo": "https://imgfp.hotp.jp/IMGH/05/09/P020100509/P020100509_168.jpg"
},
{
"id": "J001264417",
"name": "中華料理&横浜家系ラーメン 本郷家 ",
"latitude": 35.7098,
"longitude": 139.7601,
"rating": 3.8,
"urls": "https://www.hotpepper.jp/strJ001264417/?vos=nhppalsa000016",
"price_level": "PRICE_LEVEL_MODERATE",
"photo": "https://imgfp.hotp.jp/IMGH/47/41/P037424741/P037424741_168.jpg"
}
]
[2] User: 家系が食べたい気分です。あと個室があるとありがたいのですが条件を満たすお店はある？
[3] Bot: []

--------------------------------
Latest User Request :
ないですか。家系で駐車場のある店はある？

[Output]
{
"thoughts": "ユーザは昼食に駐車場付きのラーメン屋でを食べたいと思っている。したがって「家系　駐車場あり」を指定する。",
"keyword": "家系　駐車場あり" 
}

Example2

[Input]
Chat History :
[0] User : 
10人で食べ飲み放題のお店を探しています。
[1] Bot: 
[
{
"id": "J001216679",
"name": "焼肉 テっちゃん",
"latitude": 35.7201,
"longitude": 139.7654,
"rating": 4.0,
"urls": "https://www.hotpepper.jp/strJ001216679/?vos=nhppalsa000016",
"price_level": "PRICE_LEVEL_MODERATE",
"photo": "https://imgfp.hotp.jp/IMGH/81/61/P032328161/P032328161_168.jpg"
},
{
"id": "J001215058",
"name": "中華料理居酒屋 食為天",
"latitude": 35.7189,
"longitude": 139.7612,
"rating": 3.9,
"urls": "https://www.hotpepper.jp/strJ001215058/?vos=nhppalsa000016",
"price_level": "PRICE_LEVEL_INEXPENSIVE",
"photo": "https://imgfp.hotp.jp/IMGH/24/71/P037922471/P037922471_168.jpg"
},
{
"id": "J001285639",
"name": "ラーメンバル ゆきかげ",
"latitude": 35.7176,
"longitude": 139.7598,
"rating": 4.1,
"urls": "https://www.hotpepper.jp/strJ001285639/?vos=nhppalsa000016",
"price_level": "PRICE_LEVEL_INEXPENSIVE",
"photo": "https://imgfp.hotp.jp/IMGH/81/47/P040238147/P040238147_168.jpg"
}
]

--------------------------------
Latest User Request :
ラーメンや中華料理も捨てがたいけど、肉の気分なんですよねー。あ、そういえば未成年がいたので飲み放題はなしでいいです。

Output :
{
"thoughts": "ユーザは10人で食べ放題のお店で、肉を提供してくれるお店を探している。そのため、「肉　食べ放題　大人数」を指定する。",
"keyword": "肉　食べ放題　大人数"
}

Example3

[Input]
Chat History :
[0] User : 
何か重たくない系の食べ物が食べたいな。
[1] Bot : 
[
{
"id": "J001280485",
"name": "粥や　佐藤",
"latitude": 35.7189,
"longitude": 139.6612,
"rating": 3.9,
"urls": "https://www.hotpepper.jp/strJ001280485/?vos=nhppalsa000016",
"price_level": "PRICE_LEVEL_INEXPENSIVE",
"photo": "https://imgfp.hotp.jp/IMGH/24/71/P037922471/P037922471_168.jpg"
},
{
"id": "J001280485",
"name": "たない粥",
"latitude": 35.7189,
"longitude": 139.7612,
"rating": 4.1,
"urls": "https://www.hotpepper.jp/strJ001280485/?vos=nhppalsa000016",
"price_level": "PRICE_LEVEL_INEXPENSIVE",
"photo": "https://imgfp.hotp.jp/IMGH/24/71/P037922471/P037922471_168.jpg"
}
]



--------------------------------
Latest User Request :
他におすすめない？

[Output] 
{
"thoughts": "ユーザは「重たくない」という抽象度の高い希望を持っている。「重たくない」とは、消化に良く、胃にもたれにくい食材や料理を指すことが多い。会話履歴を見ると、botは「粥」というキーワードで前回推薦をしたようだが、ユーザは気に入っていないようだ。そこで、今回は消化によく、胃にもたれにくい「うどん」を指定することにする。",
"keyword": "うどん"
}

Example4
[Input]
Chat History :

--------------------------------
Latest User Request :
二日酔いに良い食べ物が食べたいです。
Output :
{
"thoughts": "「二日酔いに良い」というのも抽象度が高い。「二日酔いに良い」というのは、二日酔いによる脱水や栄養不足を補い、消化に優しく胃腸に負担をかけにくいものだと考えられるので、そのような料理が何か考えると、定食や粥などが思い浮かぶ。そこで、「粥」を指定する。",
"keyword": "粥"
}

Example5
[Input]
Chat History :

--------------------------------
Latest User Request :
個室がある食べ放題の居酒屋を探しています。

Output :
{
"thoughts": "ユーザは食べ放題で個室がある居酒屋を探している。そこで、「食べ放題　個室　居酒屋」を指定する。",
"keyword": "居酒屋　個室　居酒屋"
}

以下に、ユーザの会話履歴を示します。
回答は厳密にJSON形式で、JSONヘッダーのような余計なテキストは除いてください。さもなければシステムが崩壊します。
また、注意事項に違反していないかきちんと確認してください。

"""

    prompt_filter = """
        to be implemented
    """

    prompt_refine = """
あなたはユーザーが来店した飲食店の履歴をもとに、現在のユーザのリクエストにあった飲食店を進めるアシスタントです。
入力として、
1. ユーザーが来店した飲食店の情報
2. ユーザと飲食店オススメBOTの会話履歴
3. ユーザの最新のリクエスト
を受け取り、ユーザの最新リクエストに合致するような飲食店が、来店履歴の中にある場合は、その飲食店の情報を出力してください。

以下の形式でJSONを出力してください。
{
    "thought": "ユーザの好みをユーザの発言から分析し、その好みに合致する飲食店を抽出するに至る思考過程を述べる。",
    "id": "飲食店のID。ユーザが来店した飲食店の情報から抜き出したものを記入する。もしユーザのリクエストに合致する飲食店が来店履歴にない場合は空文字列を記入する。",
}

回答は厳密にJSON形式で、JSONヘッダーのような余計なテキストは除いてください。

出力は以下の例に従ってください。

Example 1

[Input]
Visited Stores :
Store 1
 {
  "id": "J001039795",
  "name": "IZASA",
  "latitude": 35.7077,
  "longitude": 139.7621,
  "ratings": 4.2,
  "urls": "https://www.example.com/izasa",
  "price_level": "PRICE_LEVEL_INEXPENSIVE",
  "photo": "https://example.com/photos/izasa.jpg"
}

--------------------------------
Chat History : 
[0] USER : 
美味しいご飯屋教えてください。
[1] BOT : 
[
  {
    "id": "J001274557",
    "name": "御殿",
    "latitude": 35.7079,
    "longitude": 139.7618,
    "ratings": 4.0,
    "urls": "https://www.example.com/goten",
    "price_level": "PRICE_LEVEL_MODERATE",
    "photo": "https://example.com/photos/goten.jpg"
  },
  {
    "id": "J001293289",
    "name": "つつじ屋",
    "latitude": 35.7156,
    "longitude": 139.7598,
    "ratings": 3.8,
    "urls": "https://www.example.com/tsutsujiya",
    "price_level": "PRICE_LEVEL_INEXPENSIVE",
    "photo": "https://example.com/photos/tsutsujiya.jpg"
  }
]


--------------------------------
Latest User Request : 
そうではなくて、ラーメンのお店がみたいです。 

[Output]
{
    "thought": "BOTによる和食系のお店の提案を断り、ラーメンが食べたいとユーザは思っている。またこれまでにユーザは IZASAというラーメン店に行ったことがあり、鶏白湯ラーメンが好きだと分析できる。つまり、来店履歴からはIZASAのid = J001039795を推薦する。",
    "id": "J001039795",
}

Example 2

[Input]
Visited Stores :

--------------------------------
Chat History : 
[0] USER : 
1000円くらいのランチが食べたいです。
[1] BOT : 
[
 {
    "id": "J001295205",
    "name": "ハミングバードCafe",
    "latitude": 35.7185,
    "longitude": 139.7628,
    "ratings": 4.1,
    "urls": "https://www.example.com/hummingbird",
    "price_level": "PRICE_LEVEL_INEXPENSIVE",
    "photo": "https://example.com/photos/hummingbird.jpg"
  },
  {
    "id": "J001280485",
    "name": "ミステリーカフェ 謎屋珈琲店 文京根津店",
    "latitude": 35.7192,
    "longitude": 139.7635,
    "ratings": 3.9,
    "urls": "https://www.example.com/mysterycafe",
    "price_level": "PRICE_LEVEL_INEXPENSIVE",
    "photo": "https://example.com/photos/mysterycafe.jpg"
  }
]


--------------------------------
Latest User Request : 
イタリアン系のものはありますか？

[Output]
{
    "thought": "ユーザは、BOTのカフェ系の提案を断り、イタリアン系の飲食店を探している。ユーザは、カフェ系の飲食店には興味がないと分析できる。来店履歴にはイタリアン系の飲食店はないため、空文字列を出力する。",
    "id": "",
}

Example 3

[Input]
Visited Stores :
Store 1
 {
    "id": "J001101024",
    "name": "スペインバル カリエンテ",
    "latitude": 35.7075,
    "longitude": 139.7605,
    "ratings": 4.3,
    "urls": "https://www.example.com/caliente",
    "price_level": "PRICE_LEVEL_MODERATE",
    "photo": "https://example.com/photos/caliente.jpg"
  }
Store 2
  {
    "id": "J003532879",
    "name": "中国菜 道 dao",
    "latitude": 35.7214,
    "longitude": 139.7668,
    "ratings": 4.5,
    "urls": "https://www.example.com/dao",
    "price_level": "PRICE_LEVEL_MODERATE",
    "photo": "https://example.com/photos/dao.jpg"
  },

--------------------------------
Chat History : 
[0] USER : 
うまそうな中華のみせ教えてください。
[1] BOT : 
[
  {
    "id": "J003599409",
    "name": "星宿飯店",
    "latitude": 35.7072,
    "longitude": 139.7684,
    "ratings": 4.0,
    "urls": "https://www.example.com/seishuku",
    "price_level": "PRICE_LEVEL_INEXPENSIVE",
    "photo": "https://example.com/photos/seishuku.jpg"
  },
  {
    "id": "J003624462",
    "name": "福龍 李家菜館",
    "latitude": 35.7118,
    "longitude": 139.7738,
    "ratings": 4.2,
    "urls": "https://www.example.com/fukuryu",
    "price_level": "PRICE_LEVEL_MODERATE",
    "photo": "https://example.com/photos/fukuryu.jpg"
  },
  {
    "id": "J001234441",
    "name": "香港傳奇 湯島店",
    "latitude": 35.7079,
    "longitude": 139.7701,
    "ratings": 3.9,
    "urls": "https://www.example.com/hongkongdenki",
    "price_level": "PRICE_LEVEL_INEXPENSIVE",
    "photo": "https://example.com/photos/hongkongdenki.jpg"
  },
]


--------------------------------
Latest User Request :
もっと他に候補ないですか？

[Output]
{
    "thought": "ユーザは、中華料理のお店をさらに探している。BOTが提案したお店以外の中華料理屋は、来店履歴に1店舗だけある。その店舗である、中国菜 道 dao (id = J003532879)を推薦する。",
    "id": "J003532879",
}

以下に、
1. ユーザーが来店した飲食店の情報
2. ユーザと飲食店オススメBOTの会話履歴
3. ユーザの最新のリクエスト
を示します。
回答は厳密にJSON形式で、JSONヘッダーのような余計なテキストは除いてください。さもなければシステムが崩壊します。
"""
    if name == "extract":
        return prompt_extract
    elif name == "filter":
        return prompt_filter
    elif name == "refine":
        return prompt_refine
    elif name == "extract_places":
        return prompt_extract_places
