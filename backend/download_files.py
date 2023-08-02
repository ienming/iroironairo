import requests
from read_from_google_drive import get_files_from_google_drive

def download_file(url, save_path):
    response = requests.get(url, stream=True)
    with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

if __name__ == "__main__":
    files = get_files_from_google_drive()
    for file in files:
        save_path = f"../data-process/output/{file['name']}.jpg"
        download_file(file['url'], save_path)