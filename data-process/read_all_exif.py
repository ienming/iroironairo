import piexif
import os
import glob

def read_exif():
    # 讀取轉存的 JPG 檔案的 EXIF 資訊
    jpg_folder = "output"
    jpg_files = glob.iglob(os.path.join(jpg_folder, '*.jpg'), recursive=True)

    for jpg_path in list(jpg_files):
        exif_dict = piexif.load(jpg_path)

        # debug print JPG file name
        print(jpg_path)

        exif_data = {}
        # 檢視 EXIF 資訊中的拍攝日期
        if 'Exif' in exif_dict:
            if piexif.ExifIFD.DateTimeOriginal in exif_dict['Exif']:
                date_time_original = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal].decode('utf-8')
                exif_data['date'] = date_time_original.split()[0]
                exif_data['time'] = date_time_original.split()[1]

        # 檢視完整的 EXIF 資訊
        print(exif_dict)
        print(exif_data)

if __name__ == "__main__":
    read_exif()