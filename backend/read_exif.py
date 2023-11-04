import piexif
from datetime import datetime

def read_exif(name):
    # 讀取轉存的 JPG 檔案的 EXIF 資訊
    jpg_path = f"../data-process/output/{name}.jpg"

    exif_dict = piexif.load(jpg_path)

    # debug print JPG file name
    print(name)

    exif_data = {}
    # 檢視 EXIF 資訊中的拍攝日期
    if 'Exif' in exif_dict:
        if piexif.ExifIFD.DateTimeOriginal in exif_dict['Exif']:
            date_time_original = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal].decode('utf-8')
            print(f"拍攝日期：{date_time_original}")
            exif_data['date'] = date_time_original.split()[0]
            exif_data['time'] = date_time_original.split()[1]

            # 使用 datetime 模組解析日期時間字串
            exif_date = datetime.strptime(date_time_original, "%Y:%m:%d %H:%M:%S")

            # 將日期時間轉換為 ISO 8601 格式
            iso_date_str = exif_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

            print(iso_date_str)

    # print(exif_data)
    return exif_data

if __name__ == "__main__":
    read_exif('IMG_9133')