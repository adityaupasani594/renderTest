# === match_logic.py ===
import os
import torch
import timm
import numpy as np
from PIL import Image
from torchvision import transforms
from sklearn.metrics.pairwise import cosine_similarity

AM_FOLDER = "AM_OPG"

# Use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load embedding models
model1 = timm.create_model("tf_efficientnet_b1", pretrained=True, num_classes=0).to(device).eval()
model2 = timm.create_model("convnext_base", pretrained=True, num_classes=0).to(device).eval()

# Define preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])


def get_embedding(model, image):
    tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        return model(tensor).squeeze().cpu().numpy()


def get_combined_embedding(image):
    emb1 = get_embedding(model1, image)
    emb2 = get_embedding(model2, image)
    return np.concatenate([emb1, emb2])


def load_am_embeddings():
    embeddings = []
    for filename in os.listdir(AM_FOLDER):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(AM_FOLDER, filename)
            image = Image.open(path).convert('RGB')
            embedding = get_combined_embedding(image)
            embeddings.append((filename, embedding))
    return embeddings


def find_top5_matches_temp_image(pm_image):
    am_data = load_am_embeddings()
    pm_emb = get_combined_embedding(pm_image)

    similarities = []
    for name, emb in am_data:
        score = cosine_similarity([pm_emb], [emb])[0][0]
        similarities.append((name, float(score)))

    top5 = sorted(similarities, key=lambda x: x[1], reverse=True)[:5]
    return [{'filename': name, 'score': round(score, 4)} for name, score in top5]
