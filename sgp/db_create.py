#!/usr/bin/python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
from app.modelo import Permiso
from app.modelo import Usuario
from app.modelo import Rol
from app.controlador import ControlUsuario
from app.controlador import ControlPermiso
from app.controlador import ControlRol

import os.path
db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

controlpermisos = ControlPermiso()
controlusuario = ControlUsuario()
controlrol = ControlRol()

u = Usuario()
r = Rol()

nombresPermisos = [' Crear Usuario ', ' Modificar Usuario ', ' Eliminar Usuario ', ' Crear Roles ', ' Modificar Roles ',' Eliminar Roles ', ' Crear Proyectos ', ' Modificar Proyectos ', ' Configurar Proyectos ', ' Eliminar Proyectos ', ' Crear Fases ', ' Ver Fases ', ' Crear Item ', ' Modificar Item ', ' Configurar Item ', ' Aprobar-Rechazar Item ', ' Eliminar Item ', ' Crear Tipo Item ', ' Modificar Tipo Item ', ' Eliminar Tipo Item ', ' Crear Linea Base ', ' Liberar-Cerrar Linea Base ', ' Eliminar Linea Base ', ' Informes Solicitar ']

print nombresPermisos

i = 0

for nombre in nombresPermisos :
    i = i + 1
    p = Permiso()
    p.nombre = nombre
    p.valor = i
    print p.nombre
    print p.valor
    controlpermisos.nuevoPermiso(p)
    r.permisos.append(p)

r.nombre = "Administrador Sistema"
r.descripcion = "Root"

controlrol.nuevoRol(r)

u.nombreUsuario = "root"
u.contrasena = "toor"
u.nombre = "Administrador"
u.apellido = "SGP"
u.email = "admin@sgp.com"
u.CI = 0
u.telefono = "999-999"

u.roles.append(r)

controlusuario.nuevoUsuario(u)