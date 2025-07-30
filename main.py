# === main.py ===
from PIL import Image
from flask import Flask, request, jsonify

from match_logic import find_top5_matches_temp_image
from supabase_utils import sync_images

app = Flask(__name__)

# Supabase Public Bucket URL (replace this with your actual URL)
SUPABASE_BUCKET_URL = "https://nnrrarkbbpaotasmxwhq.supabase.co/storage/v1/object/public/am-opg/"


@app.route('/match', methods=['POST'])
def match_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    img = Image.open(file.stream).convert('RGB')

    # Download AM images (cached locally after first download)
    sync_images(SUPABASE_BUCKET_URL)

    # Run matching
    results = find_top5_matches_temp_image(img)
    return jsonify({'results': results})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
