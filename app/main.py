from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from app.utils import extract_embedding, save_embedding, load_embedding, cosine_similarity

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/") 
def home(request: Request): 
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/enroll-voice")
async def enroll_voice(user_id: str = Form(...), audio_file: UploadFile = Form(...)):
    audio_bytes = await audio_file.read()
    embedding = extract_embedding(audio_bytes)
    save_embedding(user_id, embedding)
    return {"message": "Enrollment successful","user_id": user_id}

@app.post("/verify-voice")
async def verify_voice(user_id: str = Form(...), audio_file: UploadFile = Form(...)):
    stored = load_embedding(user_id)
    if stored is None:
        return JSONResponse(status_code=404, content={"error":"User not enrolled"})
    audio_bytes = await audio_file.read()
    emb = extract_embedding(audio_bytes)
    sim = cosine_similarity(stored, emb)
    return {"user_id":user_id,"verified":bool(sim>=0.75),"similarity":round(float(sim),4)}
