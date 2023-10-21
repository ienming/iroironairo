from pymongo import MongoClient
from get_database import get_database

# 設定 MongoDB 連接
db = get_database('exchange_japan')
source_collection = db.photos
target_collection = db['photos_backup']  # 將 'your_target_collection_name' 替換為新集合的名稱

# 使用 $out 操作複製整個集合
pipeline = [
    {"$out": target_collection.name}  # 將結果輸出到新集合
]
source_collection.aggregate(pipeline)

print("Collection copied.")


# 檢查兩個 collection 的資料筆數相同
# source_count = source_collection.count_documents({})
# target_count = target_collection.count_documents({})

# if source_count == target_count:
#     print(f"Document count matches: {source_count} documents in both collections.")
# else:
#     print("Document count does not match. Please check the copy process.")


# 隨機選擇一個文檔進行比對
# source_document = source_collection.find_one()
# target_document = target_collection.find_one()
# if source_document == target_document:
#     print("Randomly selected document content matches.")
# else:
#     print("Document content does not match. Please check the copy process.")


# 驗證索引相同
# source_indexes = source_collection.index_information()
# target_indexes = target_collection.index_information()
# if source_indexes == target_indexes:
#     print("Indexes in source and target collections match.")
# else:
#     print("Indexes do not match. Please check the index definitions.")