from PIL import Image, ImageCms
import os
import glob

def compress_image_to_png(input_path, output_path, max_size=300, dpi=72):
    # Open the image
    img = Image.open(input_path)

    # Set the DPI
    img.info["dpi"] = (dpi, dpi)

    # Convert to sRGB color space if needed
    if img.mode != "RGB":
        img = img.convert("RGB")
    if "icc_profile" in img.info:
        try:
            ImageCms.getOpenProfile(img.info["icc_profile"])
            img = ImageCms.profileToProfile(img, img.info["icc_profile"], "sRGB")
        except Exception as e:
            print(f"Invalid ICC profile: {e} in {input_path}")

    # Compress the image and resize if needed
    img.thumbnail((max_size, max_size))
    img.save(output_path, format="PNG", optimize=True)

# 測試
origin_folder = "googleDrive"
jpg_files = glob.iglob(os.path.join(origin_folder, '*.jpg'), recursive=True)

count = 0
for jpg_path in list(jpg_files):
    jpg_name = os.path.splitext(os.path.basename(jpg_path))[0]
    compress_image_to_png(f"googleDrive/{jpg_name}.jpg", f"compressed/{jpg_name}.jpg", 800)
    # print(jpg_name)
    print(f"已壓縮{count}張照片")
    count += 1