from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date, timezone, datetime

from weaviate.collections.classes.filters import Filter


class KnowledgeData(BaseModel):
    dataType: Optional[int] = Field(None)
    content: Optional[str] = Field(None)
    KClass: Optional[str] = Field(None)
    KCountryId: Optional[int] = Field(None)
    KSchoolId: Optional[int] = Field(None)
    AOfferCountryId: Optional[int] = Field(None)
    AOfferCollegeId: Optional[int] = Field(None)
    AOfferDegreeLevelId: Optional[int] = Field(None)
    AOfferCollegeRank: Optional[int] = Field(None)
    AEducationSchoolNameZh: Optional[str] = Field(None)
    AEducationPeriodId: Optional[int] = Field(None)
    AEducationSchoolTypeName: Optional[str] = Field(None)
    AOfferTypeId: Optional[int] = Field(None)
    ACourseStartTimeSta: Optional[date] = Field(None)
    ACourseStartTimeEnd: Optional[date] = Field(None)
    AEducationGpaSta: Optional[float] = Field(None)
    AEducationGpaEnd: Optional[float] = Field(None)
    page: Optional[int] = Field(None)
    pageNum: Optional[int] = Field(None)
    currentSourch: Optional[str] = Field(None)
    AOfferCollegeRankMin: Optional[int] = Field(None)
    AOfferCollegeRankMax: Optional[int] = Field(None)


def build_query_filters(data: KnowledgeData) -> List[Dict[str, Any]]:
    query_filters = []

    if data.dataType is not None:
        query_filters.append(Filter.by_property("dataType").equal(data.dataType),)
    if data.KClass is not None:
        query_filters.append(Filter.by_property("k_class").contains_any([data.KClass]),)
    if data.KCountryId is not None:
        query_filters.append(Filter.by_property("k_countryIds").contains_any([data.KCountryId]),)
    if data.KSchoolId is not None:
        query_filters.append(Filter.by_property("k_schoolIds").contains_any([data.KSchoolId]),)
    if data.AOfferCountryId is not None:
        query_filters.append(Filter.by_property("m_offer_country_id").equal(data.AOfferCountryId),)
    if data.AOfferCollegeId is not None:
        query_filters.append(Filter.by_property("m_offer_college_id").equal(data.AOfferCollegeId),)
    if data.AOfferDegreeLevelId is not None:
        query_filters.append(Filter.by_property("m_offer_degree_level_id").equal(data.AOfferDegreeLevelId),)
    if data.AOfferCollegeRank is not None:
        query_filters.append(Filter.by_property("m_offer_college_rank").greater_than(data.AOfferCollegeRankMin),)
        query_filters.append(Filter.by_property("m_offer_college_rank").less_than(data.AOfferCollegeRankMax),)
    if data.AEducationSchoolNameZh is not None:
        query_filters.append(Filter.by_property("m_education_school_name_zh").like(data.AEducationSchoolNameZh),)
    if data.AEducationPeriodId is not None:
        query_filters.append(Filter.by_property("m_education_period_id").equal(data.AEducationPeriodId),)
    if data.AEducationSchoolTypeName is not None:
        query_filters.append(Filter.by_property("m_education_school_type_name").like(data.AEducationSchoolTypeName),)
    if data.AOfferTypeId is not None:
        query_filters.append(Filter.by_property("m_offer_type").equal(data.AOfferTypeId),)
    if data.ACourseStartTimeSta is not None:
        query_filters.append(Filter.by_property("m_course_start_time").greater_than(data.ACourseStartTimeSta),)
    if data.ACourseStartTimeEnd is not None:
        query_filters.append(Filter.by_property("m_course_start_time").less_than(data.ACourseStartTimeEnd),)
    if data.AEducationGpaSta is not None:
        query_filters.append(Filter.by_property("m_education_gpa").greater_than(data.AEducationGpaSta),)
    if data.AEducationGpaEnd is not None:
        query_filters.append(Filter.by_property("m_education_gpa").less_than(data.AEducationGpaEnd),)
    return query_filters
