from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.schema import Base, User
import sqlalchemy.exc
import bcrypt
import os


class SQLAlchemy:
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://root:{}@{}/furmodt'.format(os.environ.get("DATABASE_PASSWORD"),
                                                                                os.environ.get("DATABASE_URL")))
        # echo=True
        self.session = sessionmaker(bind=self.engine)()

    def create_table(self):
        Base.metadata.create_all(self.engine)

    def user_register(self, user_id, user_pw, user_auth_level):
        success = True
        try:
            self.session.add(User(user_id=user_id, user_password=bcrypt.hashpw(user_pw.encode('utf-8'), bcrypt.gensalt()), user_authority_level=user_auth_level))
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print('id already exists')
            success = False
        finally:
            return success

    def user_login(self, user_id, user_pw):
        msg, authority_level = None, None
        try:
            user = self.session.query(User).filter(User.user_id == user_id).first()
            if bcrypt.checkpw(user_pw.encode('utf-8'), bytes(user.user_password, encoding='utf-8')):
                msg = 'success'
                authority_level = user.user_authority_level
            else:
                msg = 'wrong password'
        except AttributeError:
            msg = 'id not exists'
        finally:
            return msg, authority_level
