#coding: utf-8
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, PickleType
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )
from pyramid.threadlocal import get_current_request
from pyramid.events import subscriber, NewRequest
import md5
import random
import string  # pylint: disable=W0402
import socket
from sqlalchemy import create_engine

Base = declarative_base()
DBSession = scoped_session(sessionmaker(), scopefunc=get_current_request)
Base = declarative_base()
engine = create_engine('sqlite:///gen_tree.db')
DBSession.configure(bind=engine)
Base.metadata.bind = engine
Base.metadata.create_all(engine)


class User(Base):
    """ User class for keeping employee info & credentials """

    __tablename__ = "user"
    _password = None

    id = Column(Integer, primary_key=True)

    name = Column(String(255))
    email = Column(String(50))
    #_salt = Column("salt", String(32))
    #hpass = Column(String(32))



    @hybrid_property
    def salt(self):
        if self._salt:
            return self._salt
        self._salt = rndstr(32)
        return self._salt

    @salt.expression    # pyflakes: disable=W806
    def salt(cls):      # pylint: disable=E0213
        return cls._salt

    @salt.setter
    def salt(self, value):
        self._salt = value

    @property
    def password(self):
        """ Gets a transient password """
        return self._password

    @password.setter
    def password(self, value):
        """ set transient password and updates password
            hash if password is not empty
        """
        if not value:
            return
        self._password = value
        #self.hpass = User.get_hashed_password(self)

    #def check_password(self, passwd):
     #   return self.hpass == User.get_hashed_password(self, passwd)


class Test_guys(Base):

    __tablename__ = "guys"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

def register(name, email, password):
    if name and email and password:
        session = DBSession()
        query = session.query(User).filter(User.email == email)
        try:
            user = query.one()
            #raise EmailExistError(u'Такой почтовый ящик уже существует')
            return False
        except NoResultFound:
            # Создаем нового пользователя
            user = User(name=name, email=email)
            ##TODO SMTP mail
            #send_email(email, password, 1)
            user.password = password
            session.add(user)
            session.commit()
            return user
    else:
        return False


def add_guy(guy_name):
    session = DBSession()
    query = session.query(Test_guys).filter(Test_guys.name == guy_name)
    try:
        user = query.one()
        #raise EmailExistError(u'Такой почтовый ящик уже существует')
        return False
    except NoResultFound:
        guy = Test_guys(name=guy_name)
        session.add(guy)
        session.commit()
        return guy


def login(email, password):
    """
    Функция проверяет наличие почтового ящика в БД и сверяет пароль
    :param email: ПЯ введенный пользователем
    :param password: пароль введенный пользовытелем
    :return: True - пользователь найден в базе
    """

    session = DBSession()
    query = session.query(User).filter(User.email == email)
    try:
        user = query.one()
        if User.get_hashed_password(user, password) == user.hpass:
            return user
        else:
            return None
    except NoResultFound:
        return None


def all_users():
    session = DBSession()
    for user in session.query(User):
        print user.name, user.email


def all_guys():
    session = DBSession()
    for guy in session.query(Test_guys):
        print guy.name


def del_all():
    session = DBSession
    for user in session.query(User):
        session.delete(user)
    session.commit()


def del_user(user):
    session = DBSession()
    try:
        user1 = session.query(User).filter_by(name=user).first()
        #print user1
        session.delete(user1)
        session.commit()
    except Exception, ex:
        print ex

def del_guy(user):
    session = DBSession()
    guy = session.query(Test_guys).filter_by(name=user).first()
    session.delete(guy)
    session.commit()