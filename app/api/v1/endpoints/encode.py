import json

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


# 活跃状态检查
@router.get('/.well-known/live')
def live():
    return '', 204


# 准备状态检查
@router.get('/.well-known/ready')
def ready():
    # 在这里可以加上模型加载和其他准备工作的检查逻辑
    return '', 204


# 获取元信息
@router.get('/meta')
def meta():
    meta_info = {
        "model_name": "BAAI/bge-large-zh-v1.5",
        "description": "A small, efficient sentence transformer model."
    }
    # return json.dumps(meta_info, ensure_ascii=False)
    return meta_info


# 获取文本向量
@router.post('/vectors')
def get_vectors(text_data: TextData):
    sentences = text_data.text
    print(sentences)
    if not sentences:
        raise HTTPException(status_code=400, detail="No sentences provided")

    # 生成向量
    encoded_vector = embedding.embed_query(sentences)
    response = {
        "text": sentences,
        "vector": encoded_vector,
        "dim": len(encoded_vector)
    }

    return response
