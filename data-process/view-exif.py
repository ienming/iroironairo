import piexif

# 讀取轉存的 JPG 檔案的 EXIF 資訊
jpeg_path = "./output/F26CC8AC-CFB8-44CE-8EA9-3AD7D64B88A4.jpg"
exif_dict = piexif.load(jpeg_path)

# 檢視 EXIF 資訊中的拍攝日期
if 'Exif' in exif_dict:
    if piexif.ExifIFD.DateTimeOriginal in exif_dict['Exif']:
        date_time_original = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal].decode('utf-8')
        print(f"拍攝日期：{date_time_original}")

# 檢視完整的 EXIF 資訊
# print(exif_dict)