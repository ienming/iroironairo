from get_database import get_database

db = get_database()
collection = db.users

target = {"name": "Lucien"}
result=collection.find_one(target)
print(result)
# update_data = {"$set": {"age": "27"}}

# result = collection.update_one(target, update_data)

# if result.modified_count > 0:
#     print("成功更新了一個文件")
# else:
#     print("找不到符合條件的文件，沒有進行更新")