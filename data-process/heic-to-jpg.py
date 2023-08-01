import exifread
from PIL import Image
import piexif
from pillow_heif import register_heif_opener
from PIL.ExifTags import TAGS
import os
import glob

register_heif_opener()


heic_folder = "origin"
jpeg_folder = "output"

# Open HEIF or HEIC file
heic_files = glob.iglob(os.path.join(heic_folder, '*.HEIC'), recursive=True)
for heic_file in list(heic_files):
    f = open(heic_file, 'rb')
    pic_data = exifread.process_file(f)
    # 列出所有 key
    # for d in pic_data.keys():
    #     if d not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
    #         print ("Key: %s, value %s" % (d, pic_data[d]))

    # Get original EXIF data (製作日期 and 修改日期)
    original_exif = {}
    for tag, value in pic_data.items():
        if tag in ('Image DateTime', 'EXIF DateTimeOriginal', 'EXIF DateTimeDigitized'):
            original_exif[tag] = value

    # Convert to JPEG
    with Image.open(heic_file) as image:
        # Convert to JPEG and save with original EXIF data
        file_name = os.path.splitext(os.path.basename(heic_file))[0]
        jpeg_path = os.path.join(jpeg_folder, f"{file_name}.jpg")
        
        # Get the original EXIF data as a mutable dictionary
        exif_dict = piexif.load(image.info.get('exif', b''))
        
    # Update EXIF data with original 製作日期 and 修改日期
        for tag, value in original_exif.items():
            # Map the tag names to corresponding integer tags
            if tag == 'Image DateTime':
                exif_key = 0x0132  # Integer value for 'Image DateTime' tag
            elif tag == 'EXIF DateTimeOriginal':
                exif_key = piexif.ExifIFD.DateTimeOriginal
            elif tag == 'EXIF DateTimeDigitized':
                exif_key = piexif.ExifIFD.DateTimeDigitized
            else:
                continue
                
            if exif_key in exif_dict['Exif']:
                # Convert the value to string and store it in EXIF
                exif_dict['Exif'][exif_key] = str(value)

        # Convert to JPEG and save with updated EXIF data
        exif_bytes = piexif.dump(exif_dict)
        image.convert('RGB').save(jpeg_path, exif=exif_bytes)
        print(f'JPEG file saved: {jpeg_path}')