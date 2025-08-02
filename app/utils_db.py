# app/utils_db.py
import io
import numpy as np
from app.db import AsyncSessionLocal, VoiceEmbedding
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

async def save_embedding_db(user_id: str, embedding: np.ndarray):
    # Serialize numpy array to bytes
    buf = io.BytesIO()
    np.save(buf, embedding)
    data = buf.getvalue()

    async with AsyncSessionLocal() as session:
        try:
            obj = VoiceEmbedding(user_id=user_id, embedding=data)
            session.merge(obj)   # upsert
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise

async def load_embedding_db(user_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(VoiceEmbedding).where(VoiceEmbedding.user_id == user_id)
        )
        row = result.scalar_one_or_none()
        if not row:
            return None
        return np.load(io.BytesIO(row.embedding))
