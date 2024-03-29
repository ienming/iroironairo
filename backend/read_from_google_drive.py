from googleapiclient.discovery import build
from google.oauth2 import service_account
import os

# API_KEY = "AIzaSyCNHtgh8KrjRg8FXVRbB39JFpOZdiZ3QKw"
SERVICE_ACCOUNT_FILE = "../key/iroironairo-087af1abad0e.json"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/drive"]  # 設定所需的 API 權限
)

def get_files_from_google_drive():
    # 建立 Google Drive API 的 service 物件
    # service = build("drive", "v3", developerKey=API_KEY)
    service = build("drive", "v3", credentials=credentials)

    # 要取得資料的 Google Drive 資料夾 ID（這裡使用根目錄的 ID）
    folder_id = "1kg5sdAeTw5alEIpxO9tK1mH_dYkmBYcn"
    query = f"'{folder_id}' in parents and trashed=false"

    # 取得資料夾下的所有檔案
    page_token = None
    all_files = []
    while True:
        results = service.files().list(q=query,
                                        fields="nextPageToken, files(id, name, mimeType, webViewLink)",
                                        pageToken=page_token).execute()
        files = results.get('files', [])
        # 測試，隨機取得兩個檔案
        # files = random.sample(results.get('files', []), 2)
        
        if not files:
            print("找不到任何檔案.")
        else:
            print("找到以下檔案:")
            for file in files:
                download_url = f"https://drive.google.com/uc?id={file['id']}"
                dict = {
                    "name": os.path.splitext(file['name'])[0],
                    "id": file['id'],
                    "type": file['mimeType'],
                    "url_google": download_url
                }
                all_files.append(dict)
                print(dict)
                # print(f"檔案名稱: {file['name']}, 檔案 ID: {file['id']}, MIME 類型: {file['mimeType']}")
                # print(f"下載連結: {download_url}")
        page_token = results.get('nextPageToken')
        if not page_token:
            break

    return all_files

if __name__ == "__main__":
    files = get_files_from_google_drive()
    print(F"從 Google Drive 取得 {len(files)} 筆資料")