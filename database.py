from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL='postgresql://postgres:password@localhost/myapp'

# SQLALCHEMY_DATABASE_URL='mysql+pymysql://root:your_password@127.0.0.1:3306/fastapi'


engine=create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()
