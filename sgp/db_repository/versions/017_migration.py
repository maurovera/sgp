from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
permiso = Table('permiso', post_meta,
    Column('idPermiso', Integer, primary_key=True, nullable=False),
    Column('nombre', String(length=45), nullable=False),
    Column('valor', Integer, nullable=False),
)

permisos_x_rol = Table('permisos_x_rol', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('idRol', Integer),
    Column('idPermiso', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['permiso'].create()
    post_meta.tables['permisos_x_rol'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['permiso'].drop()
    post_meta.tables['permisos_x_rol'].drop()
