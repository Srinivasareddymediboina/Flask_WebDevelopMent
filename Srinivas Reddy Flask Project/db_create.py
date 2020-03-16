#  db_create.py
from sqlalchemy import Column,Integer,String,ForeignKey

from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# Create instance/Object for relationship b/w tables
Base = declarative_base()

class User(Base):
	__tablename__="users"#--> Assign Table Name
	id = Column(Integer, nullable=False,primary_key=True)
	name=Column(String(30),nullable=False)
	email=Column(String(50),nullable=False,unique=True)	
	password=Column(String(20),nullable=False)
	image=Column(String,nullable=False)	


class Item(Base):
	__tablename__="items"
	id =Column(Integer,primary_key=True,nullable=False)
	brand=Column(String(50),nullable=False)
	model=Column(String(50),nullable=False)
	url=Column(String,nullable=False)
	cost=Column(Integer,nullable=False)
	description=Column(String(500),nullable=False)
	user_id=Column(Integer,ForeignKey('users.id'))
	user=relationship(User,backref="items")
 
engine= create_engine("sqlite:///mydb.db")
Base.metadata.create_all(engine)
print("Successfully Created 'mydb.db'.")