# === main.py ===
from PIL import Image
from flask import Flask, request, jsonify
from match_logic import find_top5_matches_temp_image
from supabase_utils import sync_images

app = Flask(__name__)

# Public Supabase bucket URL (ending with a slash)
SUPABASE_BUCKET_URL = "https://nnrrarkbbpaotasmxwhq.supabase.co/storage/v1/object/public/am-opg/"

@app.route('/match', methods=['POST'])
def match_image():
    """Endpoint to upload a PM image and return top 5 AM matches."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    try:
        img = Image.open(file.stream).convert('RGB')
    except Exception as e:
        return jsonify({'error': f'Invalid image file: {e}'}), 400

    # Ensure AM images are synced (no duplicates if already downloaded)
    sync_images(SUPABASE_BUCKET_URL)

    # Run similarity matching
    results = find_top5_matches_temp_image(img)
    return jsonify({'results': results})


if __name__ == '__main__':
    # Run on 0.0.0.0 to allow access from other devices on LAN
    app.run(host='0.0.0.0', port=5000, debug=True)
