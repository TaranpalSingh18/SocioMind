
from email.policy import default
from click import File
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Annotated
from enum import Enum

class BusinessModel(BaseModel):
    name:Annotated[str, Field(max_length=25)]
    industry:Annotated[str, Field(max_length=50)]
    services:List[str]
    tone: Annotated[str, Field(default="None")]

class ToneModel(str, Enum):
    PROFESSIONAL="professional"
    WITTY="witty"
    FRIENDLY="friendly"

class PostModel(str, Enum):
    PROMO="promo"
    TIP="tip"
    UPDATE="update"


class IndustryRelevModel(BaseModel):
    relevance_score: str
    summary:str
    title:str

class IndustryModel(BaseModel):
    news: List[IndustryRelevModel]

class ContentModel(BaseModel):
    business_profile: BusinessModel
    industry_news:IndustryModel
    tone: ToneModel
    post_type: PostModel
    frequency:int


class WeeklyModel(BaseModel):
    frequency: int
    days: Optional[List[str]]

     





