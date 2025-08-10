## using postgresql
from sqlalchemy import Column, String, Text, Boolean, Integer, 
from sqlalchemy_utils import ChoiceType
from db.database import Base

class Content(Base):
    __tablename__="content"

    business_profile = Column()
