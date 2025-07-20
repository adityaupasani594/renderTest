import os
import requests


def sync_images(bucket_url, local_dir="AM_OPG"):
    os.makedirs(local_dir, exist_ok=True)

    print(f"[INFO] Listing images from {bucket_url}")
    try:
        response = requests.get(bucket_url)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Error fetching file list: {e}")
        return

    # Extract file links from the HTML or JSON response (assuming public bucket listing)
    # This works if your bucket URL returns a directory listing (e.g., GitHub-style or S3-style)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    image_links = [a['href'] for a in soup.find_all('a', href=True)
                   if a['href'].lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not image_links:
        print("⚠️ No image links found.")
        return

    for link in image_links:
        filename = os.path.basename(link)
        local_path = os.path.join(local_dir, filename)
        if os.path.exists(local_path):
            continue

        full_url = f"{bucket_url.rstrip('/')}/{filename}"
        print(f"[INFO] Downloading {filename} from {full_url}")
        img_response = requests.get(full_url)
        if img_response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(img_response.content)
            print(f"✅ Saved {filename}")
        else:
            print(f"❌ Failed to download {filename} (status {img_response.status_code})")
