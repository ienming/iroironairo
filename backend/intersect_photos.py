import os
import glob
import shutil
from pymongo import MongoClient
from get_database import get_database

# DB 裡的資料
db = get_database('exchange_japan')
collection = db.photos
data = collection.find()
mongodb_names = [document['name'] for document in data]

# 未壓縮的 jpg 檔案
folder_path = '../../iroironairo-data-backup/photos_jpg_full'
jpg_files = glob.iglob(os.path.join(folder_path, '*.[Jj][Pp][Gg]'))
jpg_files = list(jpg_files)
jpg_file_names = [os.path.basename(jpg_file) for jpg_file in jpg_files]
# print(jpg_file_names)
jpg_file_names_without_sub = [os.path.splitext(os.path.basename(jpg_file))[0] for jpg_file in jpg_files]
# print(jpg_file_names_without_sub)
# jpg_file_count = len(jpg_file_names_without_sub)
# print(f'JPG 檔案的數量：{jpg_file_count}')

# 交集
found_files = [name for name in jpg_file_names_without_sub if name in mongodb_names]
# print(len(found_files))
target_folder = '../../iroironairo-data-backup/intersection_photos'

# 複製檔案到目標資料夾
for found_file in found_files:
    # 找出具有相同名稱的檔案（包含副檔名）
    matching_files = [file for file in jpg_file_names if file.startswith(found_file)]
    if matching_files:
        for matching_file in matching_files:
            source_path = os.path.join(folder_path, matching_file)
            target_path = os.path.join(target_folder, matching_file)
            try:
                if os.path.exists(source_path):
                    shutil.copy(source_path, target_path)
                    print(f"已複製 '{matching_file}' 到目標資料夾")
                else:
                    print(f"找不到源檔案 '{matching_file}'")
            except Exception as e:
                print(f"複製檔案時發生錯誤：{str(e)}")
    else:
        print(f"找不到相符的檔案 '{found_file}'")