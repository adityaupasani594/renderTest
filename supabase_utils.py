import os
import requests

# List of known filenames uploaded to your Supabase bucket
KNOWN_IMAGES = [
    "Kau_AM.png",
    "Manav_AM.png",
    "Mansi_AM.png",
    "Maya_AM.png",
    "MB_AM.png",
    "Mehak_AM.png",
    "MK_AM.png",
]

def sync_images(bucket_url, local_dir="AM_OPG"):
    """
    Downloads images from a public Supabase bucket given known filenames.

    Args:
        bucket_url (str): Base URL of your Supabase public bucket (without trailing slash).
        local_dir (str): Local directory to store downloaded images.
    """
    os.makedirs(local_dir, exist_ok=True)
    print(f"[INFO] Syncing images from Supabase bucket: {bucket_url}")

    for filename in KNOWN_IMAGES:
        full_url = f"{bucket_url.rstrip('/')}/{filename}"
        local_path = os.path.join(local_dir, filename)

        if os.path.exists(local_path):
            print(f"✔️ Already exists: {filename}")
            continue

        try:
            response = requests.get(full_url)
            response.raise_for_status()
            with open(local_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Downloaded: {filename}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to download {filename}: {e}")
