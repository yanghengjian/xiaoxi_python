import asyncio
import weaviate
from datetime import datetime
from weaviate.classes.config import Property, DataType, Configure
from weaviate.classes.query import HybridFusion, Filter, MetadataQuery, Move, Rerank

from app.common.utils.weaviate_utils import migrate_data
from app.models.knowledge.KnowledgeVo import KnowledgeData, build_query_filters
from app.models.utils.AjaxResult import AjaxResult
from pydantic import root_validator
from fastapi import APIRouter, HTTPException
from app.core.config import settings

router = APIRouter()

# 类名称
collections_name = 'knowledge_class'
client = weaviate.connect_to_local(settings["weaviate"]["url"], settings["weaviate"]["port"])

# Weaviate 客户端懒加载
class WeaviateClient:
    _client = None

    @classmethod
    async def get_client(self):
        if self._client is None:
            self._client = weaviate.connect_to_local(settings["weaviate"]["url"], settings["weaviate"]["port"])
        return self._client


@router.get("/weaviate/createCollection")
async def create_collection2():
    client.collections.create(
        collections_name,
        properties=[
            Property(name="content", data_type=DataType.TEXT),
            Property(name="dataType", data_type=DataType.INT),
            Property(name="data_id", data_type=DataType.INT),
            Property(name="k_class", data_type=DataType.TEXT_ARRAY),
            Property(name="k_countryIds", data_type=DataType.NUMBER_ARRAY),
            Property(name="k_schoolIds", data_type=DataType.NUMBER_ARRAY),
            Property(name="m_course_start_time", data_type=DataType.DATE),
            Property(name="m_education_gpa", data_type=DataType.NUMBER),
            Property(name="m_education_period_id", data_type=DataType.INT),
            Property(name="m_education_school_name_zh", data_type=DataType.TEXT),
            Property(name="m_education_school_type_name", data_type=DataType.TEXT),
            Property(name="m_offer_college_id", data_type=DataType.INT),
            Property(name="m_offer_college_rank", data_type=DataType.INT),
            Property(name="m_offer_country_id", data_type=DataType.INT),
            Property(name="m_offer_degree_level_id", data_type=DataType.INT),
            Property(name="m_offer_type", data_type=DataType.INT),
            Property(name="realtime", data_type=DataType.DATE),
            Property(name="title", data_type=DataType.TEXT),

        ],
        vectorizer_config=[
            # Set a named vector
            Configure.NamedVectors.text2vec_transformers(
                name="instruction",
                source_properties=["content"],
                vector_index_config=Configure.VectorIndex.hnsw(),
            )
        ],
    )


@router.get("/weaviate/createknowledgeIkIndex")
async def create_collection2():
    client.collections.create(
        "knowledge_ik_index",
        properties=[
            Property(name="instruction", data_type=DataType.TEXT),
            Property(name="input", data_type=DataType.TEXT),
            Property(name="output", data_type=DataType.TEXT),
            Property(name="data_id", data_type=DataType.TEXT),
        ],
        vectorizer_config=[
            # Set a named vector
            Configure.NamedVectors.text2vec_transformers(
                name="instruction",
                source_properties=["content", "input", "output"],
                vector_index_config=Configure.VectorIndex.hnsw(),
            )
        ],
    )


@router.post("/weaviate/query")
async def query(data: KnowledgeData):
    query_filters = build_query_filters(data)
    page = data.page if data.page is not None else 0
    pageNum = data.pageNum if data.pageNum is not None else 10
    jeopardy = client.collections.get(collections_name)

    response = jeopardy.query.hybrid(
        query=data.content if data.content else " ",
        query_properties=["k_class^0.35", "title^0.2", "content^0.15"],
        alpha=1,
        filters=(
            Filter.all_of(query_filters)
        ) if query_filters else None,
        return_metadata=MetadataQuery(distance=True, score=True),
    )
    total_count = len(response.objects) if len(response.objects) is not None else 0;
    # 对每个结果进行加权分数计算和时间衰减
    for obj in response.objects:
        final_score = apply_time_decay(obj.metadata.score, obj.properties.get('releastime', '1970-01-01'))
        obj.properties['final_score'] = final_score
    # 根据最终分数进行排序
    sorted_objects = sorted(response.objects, key=lambda x: x.properties['final_score'], reverse=True)[
                     page * pageNum:page * pageNum + pageNum]

    # 获取分页后的数据
    properties_list = [o.properties for o in sorted_objects]
    return AjaxResult.success("查询成功", properties_list).put("total", total_count).to_response()


@router.get("/weaviate/deleteKnowledgeInfoById")
async def deleteKnowledgeInfoById(id: int):
    jeopardy = client.collections.get(collections_name)
    query_filters = []
    query_filters.append(Filter.by_property("dataType").less_than(3), )
    query_filters.append(Filter.by_property("data_id").equal(id), )
    response = jeopardy.query.fetch_objects(
        filters=(
            Filter.all_of(query_filters)
        )
    )
    ids = [o.uuid for o in response.objects]  # These can be lists of strings, or `UUID` objects
    if len(ids) > 0:
        jeopardy.data.delete_many(
            where=Filter.by_id().contains_any(ids)  # Delete the 3 objects
        )
    return AjaxResult.success().to_response()


@router.get("/weaviate/getKnowledgeById")
async def query(id: int):
    jeopardy = client.collections.get(collections_name)
    query_filters = []
    query_filters.append(Filter.by_property("dataType").less_than(3), )
    query_filters.append(Filter.by_property("data_id").equal(id), )
    response = jeopardy.query.fetch_objects(
        filters=(
            Filter.all_of(query_filters)
        ) if query_filters else None,
        return_properties=["data_id"]
    )
    uuid_list = [o.uuid for o in response.objects]
    if len(response.objects) > 0:
        return AjaxResult.success(uuid_list).to_response()
    else:
        return AjaxResult.error().to_response()


@router.get("/weaviate/getKnowledgePromptBy")
async def query(name: str):
    jeopardy = client.collections.get(collections_name)
    query_filters = []
    query_filters.append(Filter.by_property("dataType").equal(1), )
    response = jeopardy.query.hybrid(
        query=name,
        limit=10,
        offset=0,
        filters=(
            Filter.all_of(query_filters)
        ) if query_filters else None,
        return_properties=["title"],
    )
    properties_list = [o.properties.get("title") for o in response.objects]
    if len(response.objects) > 0:
        return AjaxResult.success(properties_list).to_response()
    else:
        return AjaxResult.success().put("data", None).to_response()


def calculate_weighted_score(item):
    weights = {
        'k_class': 0.35,
        'title': 0.2,
        'content': 0.15,
        'vectorized_content': 0.3
    }
    k_class_score = item.get('k_class', 0) * weights['k_class']
    title_score = item.get('title', 0) * weights['title']
    content_score = item.get('content', 0) * weights['content']
    vectorized_content_score = item.get('vectorized_content', 0) * weights['vectorized_content']
    return k_class_score + title_score + content_score + vectorized_content_score


def apply_time_decay(score, release_time_str):
    now = datetime.now()
    release_time = datetime.strptime(release_time_str, '%b %d, %Y %I:%M:%S %p')
    days_diff = (now - release_time).days

    if days_diff <= 30:
        return score * 1.2
    elif 30 < days_diff <= 90:
        return score * 1.1
    elif 90 < days_diff <= 365:
        return score * 1.0
    else:
        return score * 0.4


@router.get("/weaviate/migrateData")
async def weaviate_migrate_data():
    client_src = weaviate.connect_to_local("192.168.0.139", 8080)
    client_tgt = weaviate.connect_to_local(settings["weaviate"]["url"], settings["weaviate"]["port"])
    migrate_data(client_src, client_tgt, collections_name, include_vector=True)
    return AjaxResult.success().to_response()
