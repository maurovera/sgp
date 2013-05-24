'''
Created on 10/04/2013

@author: cathesanz
'''
#INDEX
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlRol
from app.modelo import Rol
from app.controlador import ControlUsuario
from app.controlador import ControlPermiso
from app.controlador import ControlProyecto
from app.controlador import ControlFase

from app.modelo import Usuario
from contextlib import closing

control = ControlRol()
controlusuario = ControlUsuario()
controlpermisos = ControlPermiso()
controlProyecto = ControlProyecto()
controlFase = ControlFase()

def busquedaPorNombre(nombre):
    ''' Devuelve un listado de los rols que coincidan con un nombre '''
    lista = None
    r = True
    if(r):
        lista = control.buscarPorNombre(nombre)
    else:
        flash("Error. Lista no devuelta")
    return lista

def listadoRolesPorProyecto(proyecto):
    ''' Devuelve un listado de los rols '''
    lista = None
    r = True
    if(r):
        lista = control.getRolPorProyecto(proyecto)
    else:
        flash("Error. Lista no devuelta")
    return lista

def listadoProyecto(proyecto):
    lista = controlProyecto.getProyectoById(proyecto)
    return lista

#def listadoFases(proyecto):
#    lista = controlFase.getFaseByProyecto(proyecto)
#    return lista


@app.route('/proyecto/rolesPro')
@app.route('/proyecto/rolesPro/<idProyecto>')
def indexRolesPorProyecto(idProyecto):
    ''' Devuelve los datos de un rol en Concreto '''
    roles = listadoRolesPorProyecto(idProyecto);
    proy = controlProyecto.getProyectoById(idProyecto)
    proyectos = listadoProyecto(idProyecto);
#    Faseslista = listadoFases();
    return render_template('indexRolesPorProyecto.html', roles = roles, proyectos = proyectos, idProyecto = idProyecto, proy = proy)


@app.route('/proyecto/rolesPro/eliminarSin')
@app.route('/proyecto/rolesPro/eliminarSin/<idProyecto>/<id>')
def eliminarRolesPorProyecto(idProyecto, id=None):
    
    rol = control.getRolById(id)
    if(rol):
        r= control.eliminarRolSinAvisar(rol)
        if(r["estado"] == True):
            flash("Se elimino con exito el rol: " + rol.nombre + " : " + rol.descripcion)
        else:
            flash("Ocurrio un error: "+ r["mensaje"])
    else :
        flash("Ocurrio un error durante la eliminacion")

    return redirect(url_for('indexRolesPorProyecto', idProyecto = idProyecto))


@app.route('/proyecto/rolesPro/agregar')
@app.route('/proyecto/rolesPro/agregar/<idProyecto>', methods=['GET','POST'])
def agregar(idProyecto):
    ''' Crea un nuevo rol '''
    #Si recibimos algo por post


    print "entreen nuevo"
    if request.method == 'POST' :

        print request.form['nombre']
        print request.form['descripcion']
        print request.form['idFase']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        fase = request.form['idFase'] 
        
   
            
        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente
        #con un metodo kachiai
        if(nombre and descripcion):
            rol = Rol()
            rol.nombre = nombre
            rol.descripcion = descripcion
            rol.idProyecto = idProyecto
            rol.idFase = fase
            #else: sino no carga nadaaaaaaaaaaaaaaaaaaaaaaaaa carajo    
            r = control.nuevoRol(rol)
            if(r["estado"] == True):
                flash("Exito, se creo un nuevo rol")
            else :
                flash("Ocurrio un error : " + r["mensaje"])

    return redirect(url_for('indexRolesPorProyecto', idProyecto = idProyecto))


@app.route('/proyecto/rolesPro/modificarRoles')
@app.route('/proyecto/rolesPro/modificarRoles/<idProyecto>', methods=['GET','POST'])
def modificarRolesPorProyecto(idProyecto):
    ''' Modifica un rol '''



    if request.method == 'POST' :

        print request.form['nombre']
        print request.form['descripcion']
        print request.form['idRol']

        id = request.form['idRol']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']

        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente
        #con un metodo kachiai
        if(id and nombre and descripcion ):
            rol = control.getRolById(id)
            if (rol):

                rol.nombre = nombre
                rol.descripcion = descripcion

                r = control.modificarRol(rol)
                if( r["estado"] == True ):
                    flash("modficamos con exito")
                else:
                    flash("Ocurrio un error : " + r["mensaje"])


    return redirect(url_for('indexRolesPorProyecto', idProyecto = idProyecto))



#----------inicio de permisos a roles----------------------------------------------------

@app.route("/proyecto/permisosNuevo/rol")
@app.route("/proyecto/permisosNuevo/rol/<idRol>")
def permisosRolEnProyecto(idRol):
    '''Administra los roles de un usuario en especifico'''

    r = control.getRolById(idRol)
    permisos = controlpermisos.getPermisos()

    return render_template('permisosRolEnProyecto.html', permisos= permisos, rol = r)
#s
@app.route("/proyecto/permisosNuevo/rol/eliminar")
@app.route("/proyecto/permisosNuevo/rol/eliminar/<idRol>/<idPermiso>")
def eliminarPermisoRolEnProyecto(idRol,idPermiso):
    print idPermiso
    print idRol

    if ( idRol and idPermiso):
        rol = control.getRolById(idRol)
        pRemover = controlpermisos.getPermisoById(idPermiso)
        r = control.quitarPermiso(rol,pRemover)
        print rol.permisos
        if( r["estado"] == True ):
            flash("Se ha removido el permiso con exito")
        else:
            flash("Ocurrio un error : " + r["mensaje"])
    else:
        flash("Ocurrio un error, intente de nuevo")

    return redirect(url_for('permisosRolEnProyecto', idRol= idRol))

@app.route("/proyecto/permisos/rol/nuevo", methods=['GET', 'POST'])
def nuevoPermisoRolEnProyecto():
    print request.form['idPermiso']
    print request.form['idRol']

    idPermiso = request.form['idPermiso']
    idRol = request.form['idRol']

    if(idPermiso and idRol):
        rol = control.getRolById(idRol)
        pNuevo = controlpermisos.getPermisoById(idPermiso)

        r = control.agregarPermiso(rol,pNuevo)
        print rol.permisos
        if( r["estado"] == True ):
            flash("Se agrego el permiso con exito")
        else:
            flash("Ocurrio un error : " + r["mensaje"])


    else :
        flash("Ocurrio un error, debe completar correctamente el formulario")



    return redirect(url_for('permisosRolEnProyecto', idRol= idRol))

#----------------------------------------------------------------------------------------

# @app.route("/roles/buscar")
# @app.route("/roles/buscar/<nombrebuscado>")
# def buscarRol(nombrebuscado):
#     ''' Devuelve una lista de rols que coincidan con el nombre proporcionado '''
#     print "Helloooooowww"
#     roles = busquedaPorNombre(nombrebuscado);
#     return render_template('indexRol.html', roles = roles)


# # #@app.route("/roles/usuario")
# # #@app.route("/roles/usuario/<idUsuario>")
# # #def rolesUsuario(idUsuario):
# #     '''Administra los roles de un usuario en especifico'''
# # 
# #     u = controlusuario.getUsuarioById(idUsuario)
# #     roles = control.getRoles()
# # 
# #     return render_template('rolUsuario.html', roles= roles, usuario = u)
# 
# @app.route("/roles/usuario/nuevo", methods=['GET', 'POST'])
# def nuevoRolUsuario():
#     print request.form['idUsuario']
#     print request.form['idRol']
# 
#     idUsuario = request.form['idUsuario']
#     idRol = request.form['idRol']
# 
#     if(idUsuario and idRol):
#         u = controlusuario.getUsuarioById(idUsuario)
#         rolNuevo = control.getRolById(idRol)
#         roles = control.getRoles()
#         r = controlusuario.agregarRol(u,rolNuevo)
#         print u.roles
#         if( r["estado"] == True ):
#             flash("Se agrego el rol con exito")
#         else:
#             flash("Ocurrio un error : " + r["mensaje"])
# 
# 
#     else :
#         flash("Ocurrio un error, debe completar correctamente el formulario")
# 
# 
# 
#     return redirect(url_for('rolesUsuario', idUsuario= idUsuario))
# 
# 
# 
# @app.route("/roles/usuario/eliminar")
# @app.route("/roles/usuario/eliminar/<idUsuario>/<idRol>")
# def eliminarRolUsuario(idUsuario,idRol):
#     print "LO QUE ME LLEGA DE ELIMINAR ROL USUARIO"
#     print idUsuario
#     print idRol
# 
#     if ( idRol and idUsuario):
#         u = controlusuario.getUsuarioById(idUsuario)
#         rolRemover = control.getRolById(idRol)
#         r = controlusuario.quitarRol(u,rolRemover)
#         print u.roles
#         if( r["estado"] == True ):
#             flash("Se ha removido el rol con exito")
#         else:
#             flash("Ocurrio un error : " + r["mensaje"])
#     else:
#         flash("Ocurrio un error, intente de nuevo")
# 
#     return redirect(url_for('rolesUsuario', idUsuario= idUsuario))
# 
# 
# @app.route("/permisos/rol")
# @app.route("/permisos/rol/<idRol>")
# def permisosRol(idRol):
#     '''Administra los roles de un usuario en especifico'''
# 
#     r = control.getRolById(idRol)
#     permisos = controlpermisos.getPermisos()
# 
#     return render_template('permisosRol.html', permisos= permisos, rol = r)
# #s
# @app.route("/permisos/rol/eliminar")
# @app.route("/permisos/rol/eliminar/<idRol>/<idPermiso>")
# def eliminarPermisoRol(idRol,idPermiso):
#     print idPermiso
#     print idRol
# 
#     if ( idRol and idPermiso):
#         rol = control.getRolById(idRol)
#         pRemover = controlpermisos.getPermisoById(idPermiso)
#         r = control.quitarPermiso(rol,pRemover)
#         print rol.permisos
#         if( r["estado"] == True ):
#             flash("Se ha removido el permiso con exito")
#         else:
#             flash("Ocurrio un error : " + r["mensaje"])
#     else:
#         flash("Ocurrio un error, intente de nuevo")
# 
#     return redirect(url_for('permisosRol', idRol= idRol))
# 
# @app.route("/permisos/rol/nuevo", methods=['GET', 'POST'])
# def nuevoPermisoRol():
#     print request.form['idPermiso']
#     print request.form['idRol']
# 
#     idPermiso = request.form['idPermiso']
#     idRol = request.form['idRol']
# 
#     if(idPermiso and idRol):
#         rol = control.getRolById(idRol)
#         pNuevo = controlpermisos.getPermisoById(idPermiso)
# 
#         r = control.agregarPermiso(rol,pNuevo)
#         print rol.permisos
#         if( r["estado"] == True ):
#             flash("Se agrego el permiso con exito")
#         else:
#             flash("Ocurrio un error : " + r["mensaje"])
# 
# 
#     else :
#         flash("Ocurrio un error, debe completar correctamente el formulario")
# 
# 
# 
#     return redirect(url_for('permisosRol', idRol= idRol))
