## ディレクトリ構造

```bash
├─api
├─db
│  ├─access
│  └─docker
├─line
├─line
├─llm
├─test
└─trial
```
- ディレクトリ構造
    - src
        - db
            - docker
                - Dockerfileとかがここに置かれる
                - DBの立て方に関してのコードを置く
            - access
                - DBに対するアクセスのコードをここに置く
        - llm
            - llm関連のクラスを置く
            - prompt.pyのようなプロンプトをまとめたコードもここにおく
        - api
            - hotpepperへのアクセス等のクラスを置く
        - line
            - LINE Message API 関連のコードをここに置く
        - trial
            - メンバー(o or y) が動作確認のために書いたコードを置く
        - test
            - apiアクセス, DBアクセス, LINE アクセスのそれぞれの単体の機能を確認するためのtestコードを置く
        - app.py
            - サーバーの動作をする
            - 全てをまとめた動作をする