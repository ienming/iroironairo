import csv
import os
from pymongo import MongoClient
from get_database import get_database

db = get_database('exchange_japan')
collection = db.photos

# amount = 100
# data = collection.find().limit(amount)
data = collection.find()

output_folder_path = "../frontend/public"
csv_file_name = "data.csv"
output_file_path = os.path.join(output_folder_path, csv_file_name)

# 寫入 CSV 文件
with open(output_file_path, "w", newline="") as csvfile:
    # fieldnames = data[0].keys()
    fieldnames = ["_id", "name", "id", "type", "url", "date", "time", "url_google", "colors", "description", "iso_date", "places"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # 寫入 CSV 文件的標題行
    writer.writeheader()

    # 寫入數據行
    for document in data:
        writer.writerow(document)
        
print("CSV 文件已生成：", output_file_path)