# app/db.py
import io
import numpy as np
from sqlalchemy import Column, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class VoiceEmbedding(Base):
    __tablename__ = "voice_embeddings"
    user_id   = Column(String, primary_key=True, index=True)
    embedding = Column(LargeBinary, nullable=False)

# Async engine & session factory
import os
DATABASE_URL = os.getenv("DATABASE_URL")
engine       = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
