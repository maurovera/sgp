from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
atributo_de_item = Table('atributo_de_item', pre_meta,
    Column('idAtributosDeItem', Integer, primary_key=True, nullable=False),
    Column('valor', String, nullable=False),
    Column('idAtributoPorTipoItem', Integer),
    Column('prueba', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['atributo_de_item'].columns['prueba'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['atributo_de_item'].columns['prueba'].create()
