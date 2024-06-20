
import json

import weaviate
from weaviate.classes.config import Property, DataType, Configure
from weaviate.classes.query import HybridFusion, Filter, MetadataQuery, Move, Rerank
from pydantic import root_validator
from agi.xiaoxi.large_scale_model.bge_embedding import BgeEmbedding

client = weaviate.connect_to_local()

#
# client = weaviate.connect_to_custom(
#     http_host="192.168.0.139",
#     http_port=8080,
#     http_secure=False,
#     grpc_host="localhost",
#     grpc_port=50051,
#     grpc_secure=False,
#     headers={"X-Huggingface-Api-Key": "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"}
#
# )

data = [
    {
        "title": "Famine",
        "body": "From the Latin for \"hunger\", it's a period when food is extremely scarce"
    },
    {
        "title": "Tofu",
        "body": "A popular health food, this soybean curd is used to make a variety of dishes & an ice cream substitute"
    },
    {
        "title": "gastronomy",
        "body": "This word for the art & science of good eating goes back to Greek for \"belly\""
    },
    {
        "title": "devour flour",
        "body": "Voraciously eat an \"all-purpose\" baking ingredient"
    },
    {
        "title": "food stores (supermarkets)",
        "body": "This type of retail store sells more shampoo & makeup than any other"
    },
    {
        "title": "cake",
        "body": "Devil's food & angel food are types of this dessert"
    },
    {
        "title": "honey",
        "body": "The primary source of this food is the Apis mellifera"
    },
    {
        "title": "Giraffe",
        "body": "Acacia leaves are the favorite food of this tallest mammal"
    }
]
school = [
    {
        "title": "澳洲-悉尼大学",
        "body": "悉尼大学国际生学费悉尼大学国际生学费：https://www.sydney.edu.au/study/fees-and-loans/international-student-tuition-fees.html"
    },
    {
        "title": "澳洲-悉尼大学",
        "body": "悉尼大学国际生学费悉尼大学国际生学费：https://www.sydney.edu.au/study/fees-and-loans/international-student-tuition-fees.html"
    },
    {
        "title": "澳洲-悉尼大学",
        "body": "question: 悉尼大学住宿费用 answer: 校内住宿，需要有无条件offer有条件offer可以申请的如下，费用较贵第三方运营的，条件offer即可申请"
    },
    {
        "title": "澳洲-悉尼大学",
        "body": "question: 悉尼大学学费缴纳时间 answer: 学费是一个学期一个学期交的，具体缴费时间细节需要入学后和student&nbsp;center确认"
    },
    {
        "title": "澳洲-悉尼大学",
        "body": "question: 悉尼大学申请截止时间 answer: 悉尼大学申请截止时间可以参考官网说明<a href=\"https://www.sydney.edu.au/study/applying/application-dates.html\" _src=\"https://www.sydney.edu.au/study/applying/application-dates.html\">https://www.sydney.edu.au/study/applying/application-dates.html</a>"
    },
    {
        "title": "澳洲-悉尼大学",
        "body": "question: 悉尼大学院校申请费自行付费流程指导 answer: 悉尼大学院校申请费有3种付费方式：1、提供信用卡信息，网申时直接扣费2、发送付费链接自行支付，完成后提交付费成功的截图（付费流程见付费指导）3、汇款至小希指定账户代付（账户信息请联系对接支持老师）备注：悉尼大学院校申请费154.2澳币"
    }
]
knoledge = [
    {'instruction': '澳大利亚 悉尼大学 老师，现在悉尼大学有免申请费活动吗？',
     'output': '学生可以参加5月20日的免申请费活动专属报名链接如下：https://international-events.sydney.edu.au/online-open-day/?utm_source=Aoji'},
    {'instruction': '澳洲 悉尼大学 悉尼大学博士可以参加免申请费活动吗',
     'output': '套瓷成功就可以'},
    {'instruction': '澳大利亚 悉尼大学 悉尼5月份有减免申请费活动吗',
     'output': '悉尼大学5月减免申请费活动通知：悉尼大学将于5月20日举办国际在线开放日，报名参加活动且符合申请条件的学生可获得申请费减免。本次线上活动亮点：专门为本科、研究生课程和研究型高等学位国际学生设计的在线信息会议，为国际学生提供一个很好的机会来解答问题，同时了解更多关于在悉尼大学学习的信息。专属报名链接如下：https://international-events.sydney.edu.au/online-open-day/?utm_source=Aoji报名截至时间：5月19日15:00注意事项：此次活动需在系统上提交学生申请材料，备注参加悉尼大学减免活动进行预约，同时需要通过上述专属链接报名并按时参加活动。重要！！！！报名注册邮箱务必和提供的申请邮箱保持一致，后台会根据学生注册邮箱统计学生是否参加活动。'},
    {'instruction': '澳洲 悉尼大学 请问悉尼大学什么时候可以申请免学分？',
     'output': '递交申请的时候，就可以开通免学分端口，另外递交免学分的申请；但是通常要等拿到无条件录取uncon后，学校才审核免学分'},
    {'instruction': '澳大利亚 悉尼科技大学 UTS是否免申请费？',
     'output': '目前不免，AUD50（UTS付款链接www.uts.edu.au/internationaladmissionpayments，页面默认100，需要自己手动填写申请费50澳币）'},
    {'instruction': '澳洲 悉尼科技大学学院 UTS college 是否免申请费呢？',
     'output': ' UTS college是免申请费的。'},
    {'instruction': '澳洲 悉尼大学 悉尼大学博士申请是否可以参加减免申请费活动？',
     'output': '学生有套词成功的话，可以申请参加减免活动。'},
    {'instruction': '澳洲 澳大利亚国立大学 请问澳国立大学申请24年7月和25年2月有免申请费活动吗？',
     'output': '目前还没有得到院校的相关通知。'},
    {'instruction': '澳洲 悉尼科技大学 UTS本科申请硕士是否免申请费？',
     'output': '不需要的，直接全bankcheck递交就可以了。'},
    {'instruction': '澳洲 悉尼大学 悉尼Master of Computer Science (advanced entry)这个课程是否可以参加免申请费活动呀',
     'output': 'quota课程不可以、目前这个课程还不是quota、但是估计很快会加上quota'}]
# client = weaviate.connect_to_local(
#     host="192.168.0.139",
#     headers={
#         "X-HuggingFace-Api-Key": "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",
#     }
# )
bgeEmbedding = BgeEmbedding()

# collections_name = 'text2vecHuggingfaceBAAI'
# collections_name = 'text2vecHuggingfaceBAAI2'  # 模块版本
# collections_name = 'text2vecHuggingfaceBAAI3'  # 对象边向量
collections_name = 'AiKnowledge'
# collections_name = 'knoledge'
# collections_name = 'la1'
query = "请问悉尼大学什么时候可以申请免学分"
jeopardy = client.collections.get(collections_name)


# 获取所有集合
def collections_list_all():
    collections = client.collections.list_all()
    for collection in collections:
        print(collection)
    return collections


# 获取集合配置
def get_collection_config():
    articles_config = jeopardy.config.get()
    print(articles_config)


# 删除集合
def delete_collection():
    collections = client.collections.list_all()
    for collection in collections:
        client.collections.delete(collection)


# 删除集合
def delete_collection_name(collection_name):
    client.collections.delete(collection_name)


# 创建集合
def create_collection():
    client.collections.create(
        collections_name,
        vector_index_config=Configure.VectorIndex.hnsw(),
        properties=[  # properties configuration is optional
            Property(name="instruction", data_type=DataType.TEXT),
            Property(name="output", data_type=DataType.TEXT),
        ]
    )


# 创建集合
def create_collection2():
    # D:\LLM\BAAI\bge-large-zh-v1.5
    model_path = "D:/LLM/BAAI/bge-large-zh-v1.5"
    model = "BAAI/bge-large-zh-v1.5"
    client.collections.create(
        collections_name,
        properties=[  # Define properties
            Property(name="instruction", data_type=DataType.TEXT),
            Property(name="output", data_type=DataType.TEXT),
        ],

        vectorizer_config=[
            # Set a named vector
            Configure.NamedVectors.text2vec_transformers(  # Set the vectorizer
                name="instruction",  # Set a named vector
                source_properties=["instruction","output"],  # Set the source property(ies)
                # model=model,  # Set the model,可以不写
                # inference_url = 'http://192.168.16.141:8000',
                # query_inference_url = 'http://192.168.16.141:8000',
                # passage_inference_url = 'http://192.168.16.141:8000',
                vector_index_config=Configure.VectorIndex.hnsw(),  # Set the vector index configuration（default）
            )
        ],
    )


# 插入数据
def insert_data_batch(aiKnowledgeDictList):
    # 返回uuid列表
    uuid_list = list()
    for item in aiKnowledgeDictList:
        uuid = jeopardy.data.insert(
            properties=item,
            # vector=bgeEmbedding.sentence_vec(json.dumps(item)).tolist()
        )
        uuid_list.append(uuid)
    return uuid_list


def insert_data(data, vecs):
    # 返回uuid列表
    return jeopardy.data.insert(properties=data, vector=vecs)


def insert_data_cs():
    # 返回uuid列表
    return jeopardy.data.insert(properties={

        "title": "澳洲-悉尼大学",
        "body": "悉尼大学国际生学费悉尼大学国际生学费：https://www.sydney.edu.au/study/fees-and-loans/international-student-tuition-fees.html"
    }, vector=[0.12345] * 1536
    )


# 查询数据
def query_data(qq):
    response = jeopardy.query.hybrid(
        query=qq,
        fusion_type=HybridFusion.RELATIVE_SCORE,
        target_vector="instruction",
        # vector=bgeEmbedding.sentence_vec(query).tolist(),
        query_properties=["instruction", "output"],
        return_metadata=MetadataQuery(score=True, explain_score=True),
        limit=10,
    )
    i = 10
    keyword_search_results = []
    for o in response.objects:
        print(o.metadata.score, o.properties)
        keyword_search_results.append({'uuid': o.uuid, 'score': i,
                                       'text': o.properties['instruction'] + o.properties['output']})
        i -= 1
        # print(o.metadata.score, o.metadata.explain_score)
    return keyword_search_results


# 关键字查询数据
def query_data_bm25():
    response = jeopardy.query.bm25(
        query=query,
        query_properties=["instruction"],
        return_metadata=MetadataQuery(score=True),
        limit=8
    )

    for o in response.objects:
        print(o.properties)
        print(o.metadata.score)
    return response.objects


# 查询数据
def query_data_near_text(qq):
    response = jeopardy.query.near_text(
        query=qq,
        limit=10,
        target_vector="instruction",  # Specify the target vector for named vector collections
        # vector=bgeEmbedding.sentence_vec(query).tolist(),
        return_metadata=MetadataQuery(distance=True)
    )

    for o in response.objects:
        print(o.metadata.distance, o.properties)
    return response.objects


# 查询数据
def query_data_near_vector():
    response = jeopardy.query.near_vector(
        near_vector=bgeEmbedding.sentence_vec(query).tolist(),
        limit=5,
        return_metadata=MetadataQuery(distance=True)
    )

    for o in response.objects:
        print(o.properties)
        print(o.metadata.distance)


# 获取全部对象
def fetch_objects():
    response = jeopardy.query.fetch_objects()
    search_results = response.objects
    for o in response.objects:
        print(o)
    return search_results


# 删除数据
def delete_data():
    jeopardy.data.delete_many(
        where=Filter.by_property("title").like("*悉尼*"),
        # dry_run=True,
        # verbose=True
    )


# 查询数据
def query_data_near_text2():
    response = jeopardy.query.near_text(
        query="food",
        distance=0.6,
        move_to=Move(force=0.85, concepts="haute couture"),
        move_away=Move(force=0.45, concepts="finance"),
        return_metadata=MetadataQuery(distance=True),
        limit=5
    )

    for o in response.objects:
        print(o.properties)
        print(o.metadata)


def update_data(uuid, update_data):
    jeopardy.data.update(
        uuid=uuid,
        properties={
            "output": update_data,
        }
    )


def search_id(id):
    data_object = jeopardy.query.fetch_object_by_id(id)
    print(data_object.properties)


def delete_data_id(uuid):
    collection = client.collections.get("EphemeralObject")
    collection.data.delete_by_id(uuid)


if __name__ == '__main__':
    # delete_collection()
    # delete_collection_name(collections_name)
    # create_collection()
    create_collection2()
    # collections_list_all()
    # get_collection_config()
    # print('-' * 100)
    # delete_data()
    uuidList = insert_data_batch(knoledge)
    # print(uuidList)
    # search_id('cf86039f-67af-4c0d-a30d-7d44a06a4a4e')
    # update_data('cf86039f-67af-4c0d-a30d-7d44a06a4a4e',HtmlUtils.replace_link_with_url('''
    # 院校申请费：UMEL：AUD130（有独立的线下支付链接，学生通过账密付款或墨尔本大学可以通过如下链接支付申请费<a href="https://pay.cibc.com/uom，需要有学生ID，支付成功后务必截图付款成功的凭证）" _src="https://pay.cibc.com/uom，需要有学生ID，支付成功后务必截图付款成功的凭证）">https://pay.cibc.com/uom，需要有学生ID，支付成功后务必截图付款成功的凭证）</a>UQ：AUD100&nbsp;&nbsp; （可以自己激活学生系统支付申请费）USYD：加上手续费AUD154.20（有独立的线下支付链接）UNSW：AUD150（生成reference number，有独立的线下支付链接）ANU：AUD110（24年入学申请费AUD110澳币）MONASH：AUD100 （有独立的线下支付链接）ADELAIDE: AUD150西澳UWA：&nbsp;AUD$125UTS：AUD50&nbsp;AUD302：维省公高（跟学费一起缴纳）AUD295：纽省公高（申请递交时缴纳）    '''))
    # print('-' * 100)
    # search_id('2365b879-63f9-4d56-922c-2657bfa1a8db')
    # insert_data_cs()
    # fetch_objects()
    # print('-' * 100)
    # query_data(query)
    # print('-' * 100)
    # query_data_bm25()
    # print('-' * 100)
    query_data_near_text("澳大利亚国立大学")
    # query_data_near_vector()
