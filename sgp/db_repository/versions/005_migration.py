from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
usuario = Table('usuario', post_meta,
    Column('idUsuario', Integer, primary_key=True, nullable=False),
    Column('nombreUsuario', String(length=45)),
    Column('contrasena', String(length=160)),
    Column('nombre', String(length=45)),
    Column('apellido', String(length=45)),
    Column('telefono', String(length=20)),
    Column('CI', Integer),
    Column('email', String(length=45)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['usuario'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['usuario'].drop()
