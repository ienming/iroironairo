from get_database import get_database
from read_from_google_drive import get_files_from_google_drive
from download_files import download_file
from read_exif import read_exif

db = get_database('exchange_japan')
collection = db.photos
files = get_files_from_google_drive()

for file in files:
    save_path = f"../data-process/output/{file['name']}.jpg"
    download_file(file['url'], save_path)
    exif_data = read_exif(file['name'])

    # 存入拍攝日期與時間
    file['date'] = exif_data['date']
    file['time'] = exif_data['time']

    query = { "name" : file['name'] }
    existing_data = collection.find_one(query)
    if existing_data:
        collection.update_one(query, {"$set": file})
        print(f"已更新資料: {file}")
    else:
        collection.insert_one(file)
        print(f"已插入資料: {file}")