from datetime import datetime


def is_one_hour_passed(last_access_time):
    """
    最後の会話から1時間以上経過しているかを判定する関数
    
    Parameters
    -----------------
    last_access_time : datatime
        過去の会話の最終時刻 '{year}-{month}-{day} {hour}:{minute}:{second}'の形式
    
    Returns
    -----------------
    True/False : bool
        1時間以上経過していたらTrue
    """
    # 文字列をdatetimeオブジェクトに変換
    past_time = last_access_time
    now_time = datetime.now()
    # 時間差を計算
    time_difference = now_time - past_time
   
    # 時間差が1時間以上かどうかを判定
    # 10 = mysqlの時差9時間+1時間
    return time_difference.total_seconds() >= 3600*10
