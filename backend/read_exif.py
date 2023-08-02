import piexif

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
            # print(f"拍攝日期：{date_time_original}")
            exif_data['date'] = date_time_original.split()[0]
            exif_data['time'] = date_time_original.split()[1]

    return exif_data

if __name__ == "__main__":
    read_exif()