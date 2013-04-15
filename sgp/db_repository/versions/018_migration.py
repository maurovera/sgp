from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
rol = Table('rol', post_meta,
    Column('idRol', Integer, primary_key=True, nullable=False),
    Column('nombre', String(length=45), nullable=False),
    Column('descripcion', String(length=100), nullable=False),
    Column('idProyecto', Integer),
    Column('idFase', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['rol'].columns['idFase'].create()
    post_meta.tables['rol'].columns['idProyecto'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['rol'].columns['idFase'].drop()
    post_meta.tables['rol'].columns['idProyecto'].drop()
