
from get_database import get_database

db = get_database('exchange_japan')
collection = db.photos
all_documents = collection.find()

# 迭代所有文檔
count = 1
for doc in all_documents:
    # 獲取原本的 URL
    old_url = doc['url']

    # 根據你的本機路徑結構，將 URL 轉換成本地路徑
    local_path = f"../assets/photos/{doc['name']}.jpg"

    # 更新 URL
    doc['url'] = local_path

    # 執行更新操作
    query = {'_id': doc['_id']}
    collection.update_one(query, {'$set': {'url': local_path}})
    print(f"已經更新{count}個檔案")
    count+=1