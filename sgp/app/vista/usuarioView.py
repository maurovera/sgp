#INDEX
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlUsuario
from app.modelo import Usuario
from contextlib import closing

control = ControlUsuario()



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



@app.route('/usuario')
def indexUsuario():
    ''' Devuelve los datos de un Usuario en Concreto '''
    usuarios = listadoUsuarios();
    return render_template('indexUsuario.html', usuarios = usuarios)


@app.route('/usuario/eliminar')
@app.route('/usuario/eliminar/<id>')
def eliminarUsuario(id=None):
    if(id):
        usuario = control.getUsuarioById(id)
        
        if(usuario):
            
            r= control.eliminarUsuario(usuario)
            if(r["estado"] == True):
                flash("Se elimino con exito el usuario: " + usuario.nombre + " " + usuario.apellido)
            else:
                flash("Ocurrio un error: "+ r["mensaje"])
        else :
            flash("Ocurrio un error durante la eliminacion")
    
    return redirect(url_for('indexUsuario'))

         


@app.route('/usuario/nuevo', methods=['GET','POST'])
def nuevoUsuario():
    ''' Crea un nuevo Usuario '''
    #Si recibimos algo por post
    
    
    
    if request.method == 'POST' :
        
        print request.form['nombreUsuario']
        print request.form['nombre']
        print request.form['apellido']
        print request.form['CI']
        print request.form['telefono']
        print request.form['email']
        print request.form['contrasena']
        
        nombreUsuario = request.form['nombreUsuario']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        CI = request.form['CI']
        telefono = request.form['telefono']
        email = request.form['email']
        contrasena = request.form['contrasena']
        
        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente 
        #con un metodo kachiai
        if(nombreUsuario and nombre and apellido and CI and telefono and email and contrasena):
            usuario = Usuario()
            usuario.nombreUsuario = nombreUsuario
            usuario.nombre = nombre
            usuario.apellido = apellido
            usuario.CI = CI
            usuario.telefono = telefono
            usuario.email = email
            usuario.contrasena = contrasena
            
            
            r = control.nuevoUsuario(usuario)
            if(r["estado"] == True):
                flash("Exito, se creo un nuevo usuario")    
            else :
                flash("Ocurrio un error : " + r["mensaje"])
                    
    return redirect(url_for('indexUsuario'))


@app.route('/usuario/modificar', methods=['GET','POST'])
def modificarUsuario():
    ''' Modifica un Usuario '''
    
    
    
    if request.method == 'POST' :
        
        print request.form['nombreUsuario']
        print request.form['nombre']
        print request.form['apellido']
        print request.form['CI']
        print request.form['telefono']
        print request.form['email']
        print request.form['idUsuario']
        
        id = request.form['idUsuario']
        nombreUsuario = request.form['nombreUsuario']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        CI = request.form['CI']
        telefono = request.form['telefono']
        email = request.form['email']
        contrasena = request.form['contrasena']
        
        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente 
        #con un metodo kachiai
        if(id and nombreUsuario and nombre and apellido and CI and telefono and email and contrasena):
            usuario = control.getUsuarioById(id)
            if (usuario):
                usuario.nombreUsuario = nombreUsuario
                usuario.nombre = nombre
                usuario.apellido = apellido
                usuario.CI = CI
                usuario.telefono = telefono
                usuario.email = email
                usuario.contrasena = contrasena
                    
                r = control.modificarUsuario(usuario)
                if( r["estado"] == True ):
                    flash("Modficado con exito")
                else:
                    flash("Ocurrio un error : " + r["mensaje"])
                       
        
    return redirect(url_for('indexUsuario'))

@app.route("/usuarios/buscar")
@app.route("/usuarios/buscar/<nombrebuscado>")
def buscarUsuario(nombrebuscado):
    ''' Devuelve una lista de usuarios que coincidan con el nombre proporcionado '''
    print "Helloooooowww"
    usuarios = busquedaPorNombre(nombrebuscado);
    return render_template('indexUsuario.html', usuarios = usuarios)