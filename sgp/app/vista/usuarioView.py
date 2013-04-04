#INDEX
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlUsuario
from app.modelo import Usuario
from contextlib import closing

control = ControlUsuario()




def listadoUsuarios():
    ''' Devuelve un listado de los usuarios '''
    lista = None
    try:
        lista = control.getUsuarios()
    except Exception, error:
        print "ERROR : " + str(error)
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
            try:
                control.eliminarUsuario(usuario)
                flash("Se elimino con exito el usuario" + usuario.nombre + " " + usuario.apellido)
            except:
                flash("Ocurrio un error durante la eliminacion")
        else :
            flash("Ocurrio un error durante la eliminacion")
    
    return redirect(url_for('indexUsuario'))

@app.route('/usuario/nuevo', methods=['GET','POST'])
def nuevoUsuario():
    ''' Crea un nuevo Usuario '''
    hayerror = True
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
            
            try:
                control.nuevoUsuario(usuario)
                print "Guardamos"
                hayerror = False
            except Exception, error:
                print "ERROR" + str(error)
                hayerror = True
                
            
    
    
    if (hayerror == True):
        #OCURRIO UN ERROR ??
        print "Ocurrio un error"
        flash("Ocurrio un error. Revise si ha completado correctamente los campos")
        
    return redirect(url_for('indexUsuario'))


@app.route('/usuario/modificar', methods=['GET','POST'])
def modificarUsuario():
    ''' Modifica un Usuario '''
    hayerror = True
    #Si recibimos algo por post
    
    
    
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
                try:
                    control.modificarUsuario(usuario)
                    print "mODIFICAMOS PUTO"
                    hayerror = False
                    flash("Se ha modificado con exito!")
                except Exception, error:
                    print "Error" + str(error)
                
    
    if (hayerror == True):
        #OCURRIO UN ERROR ??
        print "Ocurrio un error"
        flash("Ocurrio un error. Revise si ha completado correctamente los campos")
        
    return redirect(url_for('indexUsuario'))
