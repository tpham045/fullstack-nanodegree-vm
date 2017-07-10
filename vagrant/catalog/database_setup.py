import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__='user'
    username = Column(
        String(250), nullable = False
    )
    id = Column(
        Integer, primary_key = True
    )
    email = Column(
        String(250), nullable = False
    )
    picture = Column(
        String(250), nullable = False
    )
    
class Catalog(Base):
    __tablename__ = 'catalog'
    name = Column(
        String(250), nullable = False
    )
    id = Column(
        Integer, primary_key = True
    )
    user_id = Column(
        Integer, ForeignKey('user.id')
    )
    user = relationship(User)
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id':self.id
        }

class Item(Base):
    __tablename__= 'item'
    name = Column(
        String(250), nullable = False
    )
    id = Column(
        Integer, primary_key = True
    )
    picture = Column(
        String(250), nullable = False
    )
    description = Column(String(250))
    price = Column(String(8))
    user_id = Column(
        Integer, ForeignKey('user.id')
    )
    user = relationship(User)
    catalog_id = Column(
        Integer, ForeignKey('catalog.id')
    )
    catalog = relationship(Catalog)

engine = create_engine(
    'sqlite:///item_catalog_project_with_user.db'
)

Base.metadata.create_all(engine)
