#INDEX
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlUsuario
from app.controlador import ControlRol
from app.controlador import ControlProyecto
from app.modelo import Usuario
from contextlib import closing

control = ControlUsuario()
controlRol = ControlRol()
controlProyecto = ControlProyecto()


def busquedaPorNombre(nombre):
    ''' Devuelve un listado de los usuarios que coincidan con un nombre '''
    lista = None
    r = True
    if(r):
        lista = control.buscarPorNombre(nombre)
    else:
        flash("Error. Lista no devuelta")
    print lista
    return lista

def listadoUsuarios():
    ''' Devuelve un listado de los usuarios '''
    lista = None
    r = True
    if(r):
        lista = control.getUsuarios()
    else:
        flash("Error. Lista no devuelta")
    return lista

def listadoUsuariosPorRoles(idProyecto):
    retorno = []
    lista = controlRol.getRolPorProyecto(idProyecto)
    print "ListadoUsuariosPorRoles:"
    print lista
    print "ListadoUsuariosPorroles..."
    for rol in lista:
        usuarios = control.getUsuariosByRol(rol)
        print usuarios
        for usuario in usuarios :
            if(not (usuario in retorno) ):    
                retorno.append(usuario) 
    return retorno
    
def listadoRoles(idProyecto):
    lista = controlRol.getRolPorProyecto(idProyecto)
    return lista
    
@app.route('/proyecto/miembro')
@app.route('/proyecto/miembro/<idProyecto>')
def indexMiembroProyectoFase(idProyecto):
    ''' Devuelve los datos de un Usuario en Concreto '''
    usuarios = listadoUsuariosPorRoles(idProyecto);
    usu = listadoUsuarios();
    roles = listadoRoles(idProyecto);
    proy = controlProyecto.getProyectoById(idProyecto)
    return render_template('miembroProyectoFase.html', usu= usu, usuarios = usuarios, idProyecto = idProyecto, roles = roles, proy = proy)

@app.route('/proyecto/miembro/agregarMiembro')
@app.route('/proyecto/miembro/agregarMiembro/<idProyecto>', methods=['GET','POST'])
def agregarMiembro(idProyecto):
    
    #print request.form['idUsuario']
    
    #print"este es el maldivggggggggggggggto usuario"
    #print "estos son los datos del rol... Nombre y des del rol"
    #print request.form['nombreRol']
    #print request.form['descripcionRol']
    #print idProyecto
    #print request.form['idRol']
    
    
    print request.form['idUsuario']
    print request.form['idRol']

    idUsuario = request.form['idUsuario']
    idRol = request.form['idRol']

    if(idUsuario and idRol):
        u = control.getUsuarioById(idUsuario)
        rolNuevo = controlRol.getRolById(idRol)
        #roles = controlRol.getRoles()
        r = control.agregarRol(u,rolNuevo)
        print u.roles
        if( r["estado"] == True ):
            flash("Se agrego un usuario al proyecto con el rol con exito")
        else:
            flash("Ocurrio un error : " + r["mensaje"])


    else :
        flash("Ocurrio un error, debe completar correctamente el formulario")







    
    
    #print "se imprimen todo los roles del usuario"
    #for f in usu.roles:
     #   print "esto son los id de los roles asociados al proyecto"
      #  print f.idProyecto
        
    
    return redirect(url_for('indexMiembroProyectoFase', idProyecto = idProyecto))



@app.route('/proyecto/miembro/quitarMiembro')
@app.route('/proyecto/miembro/quitarMiembro/<idProyecto>/<idUsuario>', methods=['GET','POST'])
def quitarMiembro(idProyecto, idUsuario):
    
    print "este el id de proyecto y el id usuario"
    print idProyecto
    print idUsuario
    print "LO QUE ME LLEGA DE ELIMINAR ROL USUARIO"
    print idUsuario
    
    usu = control.getUsuarioById(idUsuario)
    usu.roles
    print "esto te tiene que traer solo los roles asociados al proyecto"
    for t in usu.roles:
        if str(t.idProyecto) == str(idProyecto):
            print "se removio este rol"
            print t
            control.quitarRol(usu,t)
            print usu.roles
    
    for t in usu.roles:
        if str(t.idProyecto) == str(idProyecto):
            print "se removio este rol"
            print t
            control.quitarRol(usu,t)
            print usu.roles
                
        

    return redirect(url_for('indexMiembroProyectoFase', idProyecto = idProyecto))




# esta seccion es para asignar roles a usuarios 
@app.route("/proyecto/miembro/rol")
@app.route("/proyecto/miembro/rol/<idProyecto>/<idUsuario>")
def rolesUsuarioProyecto(idProyecto, idUsuario ):
    '''Administra los roles de un usuario en especifico'''

    u = control.getUsuarioById(idUsuario)
    
    roles = listadoRoles(idProyecto)

    return render_template('rolUsuarioProyecto.html', roles= roles, usuario = u, idProyecto = idProyecto)

@app.route("/proyecto/miembro/rol/nuevo")
@app.route("/proyecto/miembro/rol/nuevo/<idProyecto>", methods=['GET', 'POST'])
def nuevoRolUsuarioProyecto(idProyecto):
    print request.form['idUsuario']
    print request.form['idRol']

    idUsuario = request.form['idUsuario']
    idRol = request.form['idRol']

    if(idUsuario and idRol):
        u = control.getUsuarioById(idUsuario)
        rolNuevo = controlRol.getRolById(idRol)
        roles = controlRol.getRoles()
        r = control.agregarRol(u,rolNuevo)
        print u.roles
        if( r["estado"] == True ):
            flash("Se agrego el rol con exito")
        else:
            flash("Ocurrio un error : " + r["mensaje"])


    else :
        flash("Ocurrio un error, debe completar correctamente el formulario")



    return redirect(url_for('rolesUsuarioProyecto', idProyecto = idProyecto, idUsuario= idUsuario))



@app.route("/proyecto/miembro/rol/eliminar")
@app.route("/proyecto/miembro/rol/eliminar/<idProyecto>/<idUsuario>/<idRol>")
def eliminarRolUsuarioProyecto(idProyecto, idUsuario,idRol):
    print "LO QUE ME LLEGA DE ELIMINAR ROL USUARIO"
    print idUsuario
    print idRol

    if ( idRol and idUsuario):
        u = control.getUsuarioById(idUsuario)
        rolRemover = controlRol.getRolById(idRol)
        r = control.quitarRol(u,rolRemover)
        print u.roles
        if( r["estado"] == True ):
            flash("Se ha removido el rol con exito")
        else:
            flash("Ocurrio un error : " + r["mensaje"])
    else:
        flash("Ocurrio un error, intente de nuevo")

    return redirect(url_for('rolesUsuarioProyecto',idProyecto=idProyecto, idUsuario= idUsuario))
#------------------------------Fin de asignacion  de roles a usuarios------------------