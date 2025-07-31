import io
import torch
import torchaudio
import numpy as np
import os
from scipy.spatial.distance import cosine

# Ensure torchaudio uses the correct backend
torchaudio.set_audio_backend("soundfile")  # Avoids missing sox_io errors

# Load ECAPA-TDNN model
from speechbrain.pretrained import EncoderClassifier
encoder = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_model")

EMBED_DIR = "embeddings"
os.makedirs(EMBED_DIR, exist_ok=True)

def extract_embedding(audio_bytes):
    waveform, sr = torchaudio.load(io.BytesIO(audio_bytes))
    if sr != 16000:
        resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)
        waveform = resampler(waveform)
    embedding = encoder.encode_batch(waveform)
    return embedding.squeeze().detach().cpu().numpy()

def save_embedding(user_id, embedding):
    path = os.path.join(EMBED_DIR, f"{user_id}.npy")
    np.save(path, embedding)

def load_embedding(user_id):
    path = os.path.join(EMBED_DIR, f"{user_id}.npy")
    if os.path.exists(path):
        return np.load(path)
    return None

def cosine_similarity(v1, v2):
    return 1 - cosine(v1, v2)
