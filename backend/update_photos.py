from get_database import get_database
from read_from_google_drive import get_files_from_google_drive

db = get_database('test')
collection = db.photos
files = get_files_from_google_drive()

for file in files:
    query = { "name" : file['name'] }
    existing_data = collection.find_one(query)
    if existing_data:
        collection.update_one(query, {"$set": file})
        print(f"已更新資料: {file}")
    else:
        collection.insert_one(file)
        print(f"已插入資料: {file}")