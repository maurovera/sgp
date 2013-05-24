#INDEX
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlUsuario
from app.controlador import ControlRol
from app.modelo import Usuario
from contextlib import closing

control = ControlUsuario()
controlRol = ControlRol()


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

def listadoRoles(idProyecto):
    lista = controlRol.getRolPorProyecto(idProyecto)
    return lista
    
@app.route('/proyecto/miembro')
@app.route('/proyecto/miembro/<idProyecto>')
def indexMiembroProyectoFase(idProyecto):
    ''' Devuelve los datos de un Usuario en Concreto '''
    usuarios = listadoUsuarios();
    roles = listadoRoles(idProyecto);
    return render_template('miembroProyectoFase.html', usuarios = usuarios, idProyecto = idProyecto, roles = roles)

@app.route('/proyecto/miembro/agregarMiembro')
@app.route('/proyecto/miembro/agregarMiembro/<idProyecto>', methods=['GET','POST'])
def agregarMiembro(idProyecto):
    
    print request.form['idUsuario']
    
    print"este es el maldivggggggggggggggto usuario"
    print "estos son los datos del rol... Nombre y des del rol"
    print request.form['nombreRol']
    print request.form['descripcionRol']
    print idProyecto
    return redirect(url_for('indexMiembroProyectoFase', idProyecto = idProyecto))