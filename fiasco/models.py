from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, PickleType
from database import Base


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(255))
    salt = Column(String(255))

    def __init__(self, name=None, email=None, password=None, salt=None):
        self.username = name
        self.email = email
        self.password = password
        self.salt = salt

    def __repr__(self):
        return '<User %r>' % (self.username)

    def user_exists(self, username):
        return self.query.filter(User.username == username).first()


class Playset(Base):
    __tablename__ = 'playset'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    owner = Column(Integer)
    description = Column(Text())
    relationships = Column(String(255))  # JSON string of IDs related to the details table
    needs = Column(String(255))
    locations = Column(String(255))
    objects = Column(String(255))

    def __init__(self, name=None, owner=None, desc=None, rel=None, needs=None, loc=None, obj=None):
        self.name = name
        self.owner = owner
        self.description = desc
        self.relationships = rel
        self.needs = needs
        self.locations = loc
        self.objects = obj

    def __repr__(self):
        return '<Playset %r>' % (self.name)

    def list_playsets(self):
        return self.query.all()

    def get_playset(self, id):
        return self.query.filter(Playset.id == id).first()


class Details(Base):
    __tablename__ = 'details'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    id = Column(Integer, primary_key=True)
    detail_type = Column(Enum('relationship', 'need', 'location', 'object'))
    playset_id = Column(Integer)
    data = Column(PickleType())

    def __init__(self, playset_id=None, detail_type=None, data=None):
        self.playset_id = playset_id
        self.detail_type = detail_type
        self.data = data

    def __repr__(self):
        return '<Detail for Playset #%s>' % (self.playset_id)


class Game(Base):
    __tablename__ = 'game'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    playset_id = Column(Integer)
    time_created = Column(DateTime)
    time_started = Column(DateTime)
    time_finished = Column(DateTime)
    character_1 = Column(Integer)
    character_2 = Column(Integer)
    character_3 = Column(Integer)
    character_4 = Column(Integer)
    character_5 = Column(Integer)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Game %r>' % (self.name)
