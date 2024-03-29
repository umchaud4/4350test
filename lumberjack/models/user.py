from sqlalchemy import Column, Integer, String
from lumberjack.database import Base, db_session

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    location = Column(String, nullable=True)
    sex = Column(String(1), nullable=True)
    date_of_birth = Column(String, nullable=True)

    def __init__(self, user_name=None, email=None, password=None, first_name=None, last_name=None,
                location=None, sex=None, date_of_birth=None):
        self.user_name = user_name
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.location = location
        self.sex = sex
        self.date_of_birth = date_of_birth

    @staticmethod
    def find_by_id(id):
        return (User.query.filter(User.user_id == id).first())

    @staticmethod
    def find_by_user_name(username):
        return (User.query.filter(User.user_name == username).first())

    @staticmethod
    def find_by_email(email):
        return (User.query.filter(User.email == email).first())

    @staticmethod
    def all():
        return (User.query.all())

    @staticmethod
    def save_to_db(user):
        db_session.add(user)
        db_session.commit()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymouse(self):
        return False

    def get_id(self):
        return unicode(self.user_id)

    def __repr__(self):
        return "<User id %d>" % self.user_id
