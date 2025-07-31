import numpy as np, io, os, torch, torchaudio
from scipy.spatial.distance import cosine
from speechbrain.inference import EncoderClassifier

clf = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")
def extract_embedding(audio_bytes):
    wav, sr = torchaudio.load(io.BytesIO(audio_bytes))
    if wav.shape[0]>1: wav=torch.mean(wav,0,keepdim=True)
    emb = clf.encode_batch(wav)
    return emb.squeeze().cpu().detach().numpy()
def cosine_similarity(a,b): return 1-cosine(a,b)
def save_embedding(uid, emb, folder="embeddings"):
    os.makedirs(folder,exist_ok=True); np.save(os.path.join(folder,f"{uid}.npy"),emb)
def load_embedding(uid, folder="embeddings"):
    p=os.path.join(folder,f"{uid}.npy"); return np.load(p) if os.path.exists(p) else None
