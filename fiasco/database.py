from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Database:
    def __init__(self):
        self.engine = None
        self.db_session = None

    def connect_db(self, user, passwd, db, host):
        self.engine = create_engine("mysql://%s:%s@%s/%s" % (user, passwd, host, db))
        self.db_session = scoped_session(sessionmaker(autocommit=False,
                                autoflush=False,
                                bind=self.engine))
        Base.query = self.db_session.query_property()

    def init_db(self):
        #import models
        Base.metadata.create_all(bind=self.engine)
