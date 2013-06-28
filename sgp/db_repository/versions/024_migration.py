from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
datos_item = Table('datos_item', post_meta,
    Column('idItem', Integer, primary_key=True, nullable=False),
    Column('version', Integer, nullable=False),
    Column('complejidad', Integer),
    Column('costo', Integer),
    Column('prioridad', Integer),
    Column('estado', String(length=45)),
    Column('idItemActual', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['datos_item'].columns['costo'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['datos_item'].columns['costo'].drop()
