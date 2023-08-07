from datetime import datetime
from get_database import get_database

def convert_2_iso_date(date_str, time_str):
    # 將日期字串轉換成datetime物件
    date_obj = datetime.strptime(date_str, "%Y:%m:%d")

    # 將時間字串轉換成datetime物件
    time_obj = datetime.strptime(time_str, "%H:%M:%S")

    # 合併日期和時間物件成一個完整的datetime物件
    datetime_obj = datetime.combine(date_obj.date(), time_obj.time())

    # 將datetime物件轉換成ISO 8601格式的字符串
    iso_date_str = datetime_obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    print(iso_date_str)
    return iso_date_str

db = get_database('exchange_japan')
collection = db.photos
data = collection.find()
count = 1
for d in data:
    date_str = d["date"]
    time_str = d["time"]
    iso_date_str = convert_2_iso_date(date_str, time_str)
    collection.update_one(
        {"_id": d["_id"]},
        {"$set": {"iso_date": iso_date_str}}
    )
    print(f"更新{count}筆資料")
    count += 1