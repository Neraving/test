from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.config import Configurator
from sqlalchemy import create_engine
from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy.pool import NullPool
from myproject.models import (
    DBSession,
    Base,
    register,
    all_users,
    User,
    del_all,
    del_user,
    all_guys,
    add_guy
    )

engine = create_engine('sqlite:///gen_tree.db')
DBSession.configure(bind=engine)
Base.metadata.bind = engine
Base.metadata.create_all(engine)


#register("123123","123123","ccccc")

register("sdf,","sdf","sdf")

#del_user("123")







all_guys()

all_users()




#del_all()