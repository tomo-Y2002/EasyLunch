## 準備
### データベース用クレデンシャルの設定
以下のコマンドで、```.env_mysql```を生成します。
```bash
cp .env_mysql_template .env_mysql
```
```bash
MYSQL_DATABASE=easylunch_database
MYSQL_ROOT_PASSWORD=
MYSQL_USER=easylunch_user
MYSQL_PASSWORD=
```
上記の```MYSQL_ROOT_PASSWORD```, ```MYSQL_PASSWORD```を自分で設定して```.env_mysql```に埋めます。

### docker networkの確認
以下のコマンドでdocker networkの確認を行います。
```bash
$> docker network ls
NETWORK ID     NAME      DRIVER    SCOPE
46e52a054be8   bridge    bridge    local
4f2587d39f11   host      host      local
e8c147e7b689   none      null      local
```
上記のような表示になるかと思います。ここでNAMEの欄に```easylunch```がない場合は、
以下のコマンドでdocker networkに追加します。
```bash
docker network create easylunch
```
追加が行えたら、以下のような表示なるはずです。
```bash
$> docker network ls
NETWORK ID     NAME        DRIVER    SCOPE
46e52a054be8   bridge      bridge    local
f2ea8321f731   easylunch   bridge    local
4f2587d39f11   host        host      local
e8c147e7b689   none        null      local
```

### docker volumeの確認
以下のコマンドでdocker volumeの確認を行います。
```bash
$> docker volume ls
DRIVER    VOLUME NAME
```
上記のような表示になるかと思います。ここでNAMEの欄に```easylunch-volume```がない場合は、
以下のコマンドでdocker volumeに追加します。
```bash
docker volume create easylunch-volume
```
追加が行えたら、以下のような表示なるはずです。
```bash
$> docker volume ls
DRIVER    VOLUME NAME
local     easylunch-volume
```

## データベースの立ち上げ
src/db/docker にて、以下のコマンドでdbサーバーが立ち上がります。
```bash
docker-compose up -d 
```

続いて、以下のコマンドでコンテナの内部に入ります。
```bash
docker compose exec db sh
```
そのあとに、以下のコマンドをひとつずつ入力してsqlに入ります。
```sql
$> mysql -u root -p
Enter password: # MYSQL_ROOT_PASSWORD の中身を記述
```
最後に、以下のような表示が得られたら成功です。
```sql
mysql> use easylunch_database; # MYSQL_DATABASE と同じです
mysql> show tables;
+------------------------------+
| Tables_in_easylunch_database |
+------------------------------+
| chat_history                 |
| visit_history                |
+------------------------------+
2 rows in set (0.00 sec)

mysql> select * from visit_history;
+----------+---------+----------+---------------------+
| visit_id | user_id | store_id | visited_on          |
+----------+---------+----------+---------------------+
|        1 | user456 | store123 | 2024-08-31 07:59:32 |
+----------+---------+----------+---------------------+
1 row in set (0.00 sec)

mysql> select * from chat_history;
+------------+---------+---------+-----------------------------------------------------------+---------------------+
| history_id | user_id | speaker | message                                                   | chatted_on          |
+------------+---------+---------+-----------------------------------------------------------+---------------------+
|          1 | user456 | USER    | おいしいラーメン屋を教えて                                | 2024-08-31 07:59:32 |
|          2 | user456 | BOT     | こちらのラーメン屋はいかがでしょうか？                    | 2024-08-31 07:59:32 |
+------------+---------+---------+-----------------------------------------------------------+---------------------+
2 rows in set (0.01 sec)
```

## データベースの終了
src/db/docker にて以下のコマンドを打ち込むことで、コンテナを停止することが出来ます。
```bash
docker-compose down
```


