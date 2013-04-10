'''
Created on 10/04/2013

@author: cathesanz
'''
#INDEX
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlRol
from app.modelo import Rol
from contextlib import closing

control = ControlRol()



def busquedaPorNombre(nombre):
    ''' Devuelve un listado de los rols que coincidan con un nombre '''
    lista = None
    r = True
    if(r):
        lista = control.buscarPorNombre(nombre)
    else:
        flash("Error. Lista no devuelta")
    return lista

def listadoRoles():
    ''' Devuelve un listado de los rols '''
    lista = None
    r = True
    if(r):
        lista = control.getRoles()
    else:
        flash("Error. Lista no devuelta")
    return lista



@app.route('/rol')
def indexRol():
    ''' Devuelve los datos de un rol en Concreto '''
    roles = listadoRoles();
    return render_template('indexRol.html', roles = roles)


@app.route('/rol/eliminar')
@app.route('/rol/eliminar/<id>')
def eliminarRol(id=None):
    if(id):
        rol = control.getRolById(id)
        
        if(rol):
            
            r= control.eliminarRol(rol)
            if(r["estado"] == True):
                flash("Se elimino con exito el rol: " + rol.nombre + " : " + rol.descripcion)
            else:
                flash("Ocurrio un error: "+ r["mensaje"])
        else :
            flash("Ocurrio un error durante la eliminacion")
    
    return redirect(url_for('indexRol'))

         


@app.route('/rol/nuevo', methods=['GET','POST'])
def nuevoRol():
    ''' Crea un nuevo rol '''
    #Si recibimos algo por post
    
    
    
    if request.method == 'POST' :
        
        print request.form['nombre']
        print request.form['descripcion']
        
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        
        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente 
        #con un metodo kachiai
        if(nombre and descripcion):
            rol = Rol()
            rol.nombre = nombre
            rol.descripcion = descripcion
            
            
            r = control.nuevoRol(rol)
            if(r["estado"] == True):
                flash("Exito, se creo un nuevo rol")    
            else :
                flash("Ocurrio un error : " + r["mensaje"])
                    
    return redirect(url_for('indexRol'))


@app.route('/rol/modificar', methods=['GET','POST'])
def modificarRol():
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
                       
        
    return redirect(url_for('indexRol'))

@app.route("/roles/buscar")
@app.route("/roles/buscar/<nombrebuscado>")
def buscarRol(nombrebuscado):
    ''' Devuelve una lista de rols que coincidan con el nombre proporcionado '''
    print "Helloooooowww"
    roles = busquedaPorNombre(nombrebuscado);
    return render_template('indexRol.html', roles = roles)
