from django.conf import settings
import os
import numpy as np
import torch
import clip
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity

datasetDir = os.path.join(settings.MEDIA_ROOT, "apis")
validExts = (".jpg", ".jpeg", ".png")

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

embeddings = []
paths = []


def getEmbedding(imgPath):
    img = Image.open(imgPath).convert("RGB")
    imgPreprocessed = preprocess(img).unsqueeze(0).to(device)
    with torch.no_grad():
        imgFeatures = model.encode_image(imgPreprocessed)
    imgFeatures /= imgFeatures.norm(dim=-1, keepdim=True)
    return imgFeatures.cpu().numpy()


def getTextEmbedding(caption: str):
    textTokens = clip.tokenize([caption]).to(device)
    with torch.no_grad():
        textFeatures = model.encode_text(textTokens)
    textFeatures /= textFeatures.norm(dim=-1, keepdim=True)
    return textFeatures.cpu().numpy()


def findSimilar(queryEmb, k=3, results=[]):
    sims = cosine_similarity(queryEmb, embeddings)[0]
    idx = np.argsort(-sims)[:k]
    for i in idx:
        if float(sims[i]) >= 0.2170:
            results.append({"path": paths[i], "score": float(sims[i])})

    return results


def buildIndex():
    global embeddings, paths
    embeddings = []
    paths = []

    if not os.path.exists(datasetDir):
        print(f"Media directory {datasetDir} not found")
        return

    for file in os.listdir(datasetDir):
        path = os.path.join(datasetDir, file)
        if os.path.isfile(path) and file.lower().endswith(validExts):
            try:
                emb = getEmbedding(path)
                embeddings.append(emb)

                relative_path = os.path.relpath(path, settings.MEDIA_ROOT).replace(
                    "\\", "/"
                )
                url_path = f"{settings.MEDIA_URL}{relative_path}"
                paths.append(url_path)

            except Exception as e:
                print(f"Skipping {path}: {e}")

    if embeddings:
        embeddings = np.vstack(embeddings)


buildIndex()
