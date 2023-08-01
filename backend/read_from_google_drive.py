from googleapiclient.discovery import build
from google.oauth2 import service_account

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

    # 取得資料夾下的所有檔案
    results = service.files().list(q=f"'{folder_id}' in parents and trashed=false",
                                   fields="files(id, name, mimeType)").execute()
    files = results.get('files', [])


    files_list = []
    if not files:
        print("找不到任何檔案.")
    else:
        print("找到以下檔案:")
        for file in files:
            download_url = f"https://drive.google.com/uc?id={file['id']}"
            dict = {
                "name": file['name'],
                "id": file['id'],
                "type": file['mimeType'],
                "url": download_url
            }
            files_list.append(dict)
            # print(f"檔案名稱: {file['name']}, 檔案 ID: {file['id']}, MIME 類型: {file['mimeType']}")
            # print(f"下載連結: {download_url}")
    return files_list

if __name__ == "__main__":
    get_files_from_google_drive()