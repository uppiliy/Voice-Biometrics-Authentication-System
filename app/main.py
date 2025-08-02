from pathlib import Path
from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from app.utils import extract_embedding, cosine_similarity
from app.utils_db import save_embedding_db, load_embedding_db
from app.db import Base, engine
import logging

logging.basicConfig(level=logging.INFO)

# Determine the base directory relative to this file
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    # Create the table if it doesn’t exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Mount static files using a path relative to this module
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

# Configure Jinja2 templates with a module-relative path
templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.api_route("/", methods=["GET", "HEAD"])
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/enroll-voice")
async def enroll_voice(
    user_id: str = Form(...),
    audio_file: UploadFile = Form(...),
):
    audio_bytes = await audio_file.read()
    embedding = extract_embedding(audio_bytes)
    # Save embedding to PostgreSQL
    await save_embedding_db(user_id, embedding)
    return {"message": "Enrollment successful", "user_id": user_id}

@app.post("/verify-voice")
async def verify_voice(
    user_id: str = Form(...),
    audio_file: UploadFile = Form(...),
):
    logging.info(f"🔍 Verify called for user_id={user_id}")
    # Load embedding from PostgreSQL
    stored = await load_embedding_db(user_id)
    if stored is None:
        logging.warning(f"⚠️ No embedding found for user {user_id}")
        return JSONResponse(status_code=404, content={"error": "User not enrolled"})

    try:
        audio_bytes = await audio_file.read()
        logging.info(f"📥 Received {len(audio_bytes)} bytes for verification")

        emb = extract_embedding(audio_bytes)
        sim = cosine_similarity(stored, emb)
        logging.info(f"✅ Cosine similarity: {sim:.4f}")

        return {
            "user_id": user_id,
            "verified": bool(sim >= 0.75),
            "similarity": round(float(sim), 4),
        }
    except Exception as e:
        logging.exception("❌ Error in /verify-voice")
        return JSONResponse(status_code=500, content={"error": str(e)})
