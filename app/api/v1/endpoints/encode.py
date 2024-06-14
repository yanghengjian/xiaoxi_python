from fastapi import APIRouter, HTTPException
from app.models.text import TextData
from app.services.vectorizer import vectorizer

router = APIRouter()

@router.post("/encode")
async def encode_text(data: TextData):
    try:
        encoded_vector = vectorizer.encode(data.text)
        return {"vector": encoded_vector.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
