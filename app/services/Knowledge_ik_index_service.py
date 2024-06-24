from typing import Optional

import weaviate
from langfuse.decorators import observe
from pydantic import BaseModel
from weaviate.collections.classes.grpc import HybridFusion, MetadataQuery

from app.api.weaviate.weaviate import WeaviateClient


class KnowledgeIkIndexModel(BaseModel):
    uuid: Optional[str]
    instruction: str
    output: str


class KnowledgeIkIndexService:
    client = weaviate.connect_to_local("192.168.0.139", 8080).collections.get("Knowledge_ik_index")
    # @observe()
    @classmethod
    def search_hybrid(cls, query, limit):

        response = cls.client.query.hybrid(
            query=query,
            fusion_type=HybridFusion.RELATIVE_SCORE,
            target_vector="instruction",
            # vector=self.langChain.embedding.embed_query(query),
            # query_properties=["instruction", "output"],
            return_metadata=MetadataQuery(score=True, explain_score=True),
            limit=limit,
        )
        response_list = []
        for o in response.objects:
            Knowledge_ik_index_model = KnowledgeIkIndexModel(uuid=str(o.uuid), instruction=o.properties['instruction'],
                                                             output=o.properties['output'])
            response_list.append(Knowledge_ik_index_model)
        return response_list


if __name__ == '__main__':
    knowledge_ik_index_service = KnowledgeIkIndexService()
    print(knowledge_ik_index_service.search_hybrid("墨尔本大学怎么样", 10))
