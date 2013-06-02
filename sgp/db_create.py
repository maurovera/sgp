#!/usr/bin/python
import datetime
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
from app.modelo import Permiso
from app.modelo import Usuario
from app.modelo import Rol
from app.modelo import Proyecto
from app.modelo import Fase
from app.controlador import ControlUsuario
from app.controlador import ControlPermiso
from app.controlador import ControlRol
from app.controlador import ControlProyecto
from app.controlador import ControlFase
from app.vista import proyectoView
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
controlProyecto = ControlProyecto()
controlFase = ControlFase()

u = Usuario()
r = Rol()
pro = Proyecto()
f = Fase()
nombresPermisos = [' Crear Usuario ', ' Modificar Usuario ', ' Eliminar Usuario ', ' Crear Roles ', ' Modificar Roles ',' Eliminar Roles ', ' Crear Proyectos ', ' Modificar Proyectos ', ' Configurar Proyectos ', ' Eliminar Proyectos ', ' Crear Fases ', ' Ver Fases ', ' Crear Item ', ' Modificar Item ', ' Configurar Item ', ' Aprobar-Rechazar Item ', ' Eliminar Item ', ' Crear Tipo Item ', ' Modificar Tipo Item ', ' Eliminar Tipo Item ', ' Crear Linea Base ', ' Liberar-Cerrar Linea Base ', ' Eliminar Linea Base ', ' Informes Solicitar ', 'votar']

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

# se crea un nuevo proyecto  

pro.nombre = "proyectoUno"

pro.descripcion = "es un proyecto inicial" 
pro.fechaCreacion = str(datetime.date.today())
pro.complejidadTotal = 0
pro.estado = "no iniciado"

controlProyecto.nuevoProyecto(pro)


#--------crea el rol al usuario root para administrar el proyecto
w = Rol()
w.nombre = "Administrador Proyecto " + pro.nombre
w.descripcion = "Administrar el Proyecto " + pro.nombre
w.idProyecto = pro.idProyecto
cp = ControlPermiso()
    #Y vamos agregando los permisos respectivos a proyectos
w.permisos.append(cp.buscarPorValor(7))
w.permisos.append(cp.buscarPorValor(8))
w.permisos.append(cp.buscarPorValor(9))
w.permisos.append(cp.buscarPorValor(10))

r2 = controlusuario.agregarRol(u,w)
#--------------------------------------------------


#--------------------------------------------------
# se crea una fase

f.nombre = "fase uno inicial"
f.numeroFase = len( list(pro.fases) ) + 1
f.descripcion = "es una fase incial"
f.estado = "no iniciado"
    
#Relaciones
f.idProyecto = pro.idProyecto
controlFase.nuevaFase(f)


#-------------------------------------------

# se crea un nuevo proyecto en estado iniciado  
pro1 = Proyecto()
pro1.nombre = "proyectoDos"

pro1.descripcion = "es un proyecto iniciado" 
pro1.fechaCreacion = str(datetime.date.today())
pro1.complejidadTotal = 0
pro1.estado = "iniciado"

controlProyecto.nuevoProyecto(pro1)


#--------crea el rol al usuario root para administrar el proyecto
w1 = Rol()
w1.nombre = "Administrador Proyecto " + pro1.nombre
w1.descripcion = "Administrar el Proyecto " + pro1.nombre
w1.idProyecto = pro1.idProyecto
cp1 = ControlPermiso()
    #Y vamos agregando los permisos respectivos a proyectos
w1.permisos.append(cp1.buscarPorValor(7))
w1.permisos.append(cp1.buscarPorValor(8))
w1.permisos.append(cp1.buscarPorValor(9))
w1.permisos.append(cp1.buscarPorValor(10))

r2 = controlusuario.agregarRol(u,w1)
#--------------------------------------------------


#--------------------------------------------------
# se crea una fase
f2 = Fase()
f2.nombre = "fase dos inicial"
f2.numeroFase = len( list(pro1.fases) ) + 1
f2.descripcion = "es una fase incial dos"
f2.estado = "no iniciado"
    
#Relaciones
f2.idProyecto = pro1.idProyecto

controlFase.nuevaFase(f2)
# se crea una fase
f3 = Fase()
f3.nombre = "fase tres inicial"
f3.numeroFase = len( list(pro1.fases) ) + 1
f3.descripcion = "es una fase incial tres"
f3.estado = "no iniciado"
    
#Relaciones
f3.idProyecto = pro1.idProyecto




controlFase.nuevaFase(f3)

#-------------------------------------------



