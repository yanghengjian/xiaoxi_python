from fastapi import APIRouter, HTTPException
from app.models.text import TextData
from app.core.langchain_client import embedding

router = APIRouter()
@router.post("/encode")
async def encode_text(data: TextData):
    try:
        encoded_vector = embedding.embed_query(data.inputs)
        return {"vector": encoded_vector}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
