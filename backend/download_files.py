import requests
from read_from_google_drive import get_files_from_google_drive
import time

# def download_file(url, save_path):
#     response = requests.get(url, stream=True)
#     with open(save_path, 'wb') as f:
#         for chunk in response.iter_content(chunk_size=8192):
#             f.write(chunk)

def download_file(url, save_path, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, stream=True)
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                print(f"從{url}下載")
                print(f"下載{save_path}成功！")
            break  # 下載成功，跳出重試迴圈
        except Exception as e:
            print(f"下載檔案發生錯誤: {e}")
            retries += 1
            time.sleep(1)  # 延遲一秒後再重試
    else:
        print("無法下載檔案，超過重試次數")

if __name__ == "__main__":
    files = get_files_from_google_drive()
    for file in files:
        save_path = f"../data-process/output/{file['name']}.jpg"
        download_file(file['url'], save_path)