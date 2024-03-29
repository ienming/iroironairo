from get_database import get_database
# from read_from_google_drive import get_files_from_google_drive
from read_exif import read_exif
import os
import glob

# db = get_database('exchange_japan')
# collection = db.photos
# files = get_files_from_google_drive()
# print(F"從 Google Drive 取得 {len(files)} 筆資料")

# count = 0
# for file in files:
    # exif_data = read_exif(file['name'])

    # # 存入拍攝日期與時間
    # file['date'] = exif_data['date']
    # file['time'] = exif_data['time']

    # query = { "name" : file['name'] }
    # existing_data = collection.find_one(query)
    # if existing_data:
    #     collection.update_one(query, {"$set": file})
    #     print(f"已更新資料: {file}")
    # else:
    #     collection.insert_one(file)
    #     print(f"已插入資料: {file}")
    # print(f"目前已經儲存／更新{count}筆資料")
    # count+=1

if __name__ == "__main__":
    db = get_database('exchange_japan')
    collection = db.photos
    files = get_files_from_google_drive()
    print(F"從 Google Drive 取得 {len(files)} 筆資料")

    count = 0
    for file in files:
        query = {'id': file['id']}
        # collection.update_one(query, {'$set': {'url_google': file['url_google']}})
        print(f"已經更新{count}個檔案")
        count+=1