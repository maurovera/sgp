#INDEX
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlUsuario
from app.controlador import ControlRol
from app.controlador import ControlProyecto
from app.controlador import ControlPermiso
from app.modelo import Rol
from app.modelo import Usuario
from contextlib import closing

control = ControlUsuario()
controlRol = ControlRol()
controlProyecto = ControlProyecto()
controlPermiso = ControlPermiso()

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
    pro =  controlProyecto.getProyectoById(idProyecto)
    lista = controlRol.getRolPorProyecto(idProyecto)
    
    for rol in lista:
        if (rol.nombre == "MiembroComite "+pro.nombre):
            usuarios = control.getUsuariosByRol(rol)
            print usuarios
            for usuario in usuarios :
                if(not (usuario in retorno) ):    
                    retorno.append(usuario) 
    return retorno
    
def listadoUsuariosSoloPorRoles(idProyecto):
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
    
@app.route('/proyecto/comite')
@app.route('/proyecto/comite/<idProyecto>')
def indexComite(idProyecto):
    ''' Devuelve los datos de un Usuario en Concreto '''
    usuarios = listadoUsuariosPorRoles(idProyecto);
    usu = listadoUsuariosSoloPorRoles(idProyecto);
    roles = listadoRoles(idProyecto);
    proy = controlProyecto.getProyectoById(idProyecto)
    return render_template('comite.html', usu= usu, usuarios = usuarios, idProyecto = idProyecto, roles = roles, proy = proy)

@app.route('/proyecto/comite/agregarMiembro')
@app.route('/proyecto/comite/agregarMiembro/<idProyecto>', methods=['GET','POST'])
def agregarMiembroComite(idProyecto):
    
    #print request.form['idUsuario']
    
    #print"este es el maldivggggggggggggggto usuario"
    #print "estos son los datos del rol... Nombre y des del rol"
    #print request.form['nombreRol']
    #print request.form['descripcionRol']
    #print idProyecto
    #print request.form['idRol']
    
    
    print request.form['idUsuario']
    #print request.form['idRol']

    idUsuario = request.form['idUsuario']
    #idRol = request.form['idRol']
    pro = controlProyecto.getProyectoById(idProyecto)
    if(idUsuario):
        u = control.getUsuarioById(idUsuario)
        
        roles = controlRol.getRolPorProyecto(idProyecto)
        for r in roles :
            if r.nombre == "MiembroComite "+pro.nombre:
                print "hola VITEH " + r.nombre
                q = control.agregarRol(u, r)
                if( q["estado"] == True ):
                    flash("Se agrego un usuario miembro al proyecto con el rol con exito")
                else:
                    flash("Este usuario ya forma parte del comite")   
                    #flash("Ocurrio un error : " + q["mensaje"])


    else :
        flash("Ocurrio un error, debe completar correctamente el formulario")

                    
        #r = Rol()
        #p= controlPermiso.getPermisoById(19)
        #r.permisos.append(p)
        #r.nombre = "Miembro "+ u.nombre + pro.nombre
        #r.descripcion = "es un miembro del comite"
        #r.idProyecto = idProyecto
        #controlRol.nuevoRol(r)

        #roles = controlRol.getRoles()
        
        print u.roles
        






    
    
    #print "se imprimen todo los roles del usuario"
    #for f in usu.roles:
     #   print "esto son los id de los roles asociados al proyecto"
      #  print f.idProyecto
        
    
    return redirect(url_for('indexComite', idProyecto = idProyecto))



@app.route('/proyecto/comite/quitarMiembro')
@app.route('/proyecto/comite/quitarMiembro/<idProyecto>/<idUsuario>', methods=['GET','POST'])
def quitarMiembroComite(idProyecto, idUsuario):
     
    print "este el id de proyecto y el id usuario"
    print idProyecto
    print idUsuario
    print "LO QUE ME LLEGA DE ELIMINAR ROL USUARIO"
    print idUsuario
    pro = controlProyecto.getProyectoById(idProyecto)
    usu = control.getUsuarioById(idUsuario)
    usu.roles
    print "esto te tiene que traer solo los roles asociados al proyecto"
    for t in usu.roles:
        if str(t.idProyecto) == str(idProyecto):
            if t.nombre == "MiembroComite "+pro.nombre : 
                print "se removio este rol" + t.nombre
                print t
                control.quitarRol(usu,t)
                #controlRol.eliminarRolSinAvisar(t)
                print usu.roles
     
             

    return redirect(url_for('indexComite', idProyecto = idProyecto))
