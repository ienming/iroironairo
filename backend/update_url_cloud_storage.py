import base64
import os
from pymongo import MongoClient
from get_database import get_database

# 连接到MongoDB数据库
db = get_database('exchange_japan')
collection = db.photos

# 获取MongoDB集合中的所有数据
all_data = collection.find()
# limit_data = collection.find().limit(10)

# 遍历每条数据
for data in all_data:
    # 获取name字段
    name = data.get("name")
    
    # 构建 Google Cloud Storage 的 URL（此处以存储桶名为 your-bucket-name 为例）
    google_storage_url = f"https://storage.googleapis.com/iroironairo.appspot.com/photos_jpg_full/{name}.jpg"

    # 更新 'url_google' 字段
    collection.update_one({"name": name}, {"$set": {"url_google": google_storage_url}})
    print(f"'url_google' field updated for {name}.")

# 关闭MongoDB连接
db.client.close()