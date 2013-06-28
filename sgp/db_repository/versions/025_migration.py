from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
relacion = Table('relacion', post_meta,
    Column('idRelacion', Integer, primary_key=True, nullable=False),
    Column('tipo', String(length=45), nullable=False),
    Column('idSucesor', Integer),
    Column('idAntecesor', Integer),
    Column('idProyecto', Integer),
    Column('idFase', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['relacion'].columns['idFase'].create()
    post_meta.tables['relacion'].columns['idProyecto'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['relacion'].columns['idFase'].drop()
    post_meta.tables['relacion'].columns['idProyecto'].drop()
