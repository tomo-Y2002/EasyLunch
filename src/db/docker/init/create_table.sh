#!/bin/sh

CMD_MYSQL="mysql -u${MYSQL_USER} -p${MYSQL_PASSWORD} ${MYSQL_DATABASE}"

$CMD_MYSQL -e "CREATE TABLE visit_history (
    visit_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(255),
    store_id VARCHAR(255),
    visited_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"

$CMD_MYSQL -e "INSERT INTO visit_history (user_id, store_id) VALUES ('user456', 'store123');"

$CMD_MYSQL -e "CREATE TABLE chat_history (
    history_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(255),
    speaker ENUM('USER', 'BOT'),
    message TEXT,
    chatted_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"

$CMD_MYSQL -e "INSERT INTO chat_history (user_id, speaker, message) VALUES ('user456', 'USER', 'おいしいラーメン屋を教えて');"
$CMD_MYSQL -e "INSERT INTO chat_history (user_id, speaker, message) VALUES ('user456', 'BOT', 'こちらのラーメン屋はいかがでしょうか？');"
