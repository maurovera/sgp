from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
post = Table('post', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
)

user = Table('user', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String),
    Column('email', String),
    Column('role', SmallInteger),
)

atributo_de_item = Table('atributo_de_item', post_meta,
    Column('idAtributosDeItem', Integer, primary_key=True, nullable=False),
    Column('valor', String(length=100), nullable=False),
    Column('prueba', Integer),
    Column('idAtributoPorTipoItem', Integer),
)

linea_base = Table('linea_base', post_meta,
    Column('idLB', Integer, primary_key=True, nullable=False),
    Column('numero', Integer),
    Column('estado', Integer),
    Column('idFase', Integer),
    Column('idUsuario', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].drop()
    pre_meta.tables['user'].drop()
    post_meta.tables['atributo_de_item'].columns['prueba'].create()
    post_meta.tables['linea_base'].columns['idUsuario'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].create()
    pre_meta.tables['user'].create()
    post_meta.tables['atributo_de_item'].columns['prueba'].drop()
    post_meta.tables['linea_base'].columns['idUsuario'].drop()
