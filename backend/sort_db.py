from get_database import get_database

db = get_database("exchange_japan")
collection = db.photos
# 定義排序的日期欄位名稱
sort_field = 'iso_date'

# 進行升序排序
result = collection.find().sort(sort_field, 1)
for d in result:
    print(d)