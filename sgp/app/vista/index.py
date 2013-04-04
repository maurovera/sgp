#INDEX
from flask import render_template, flash, redirect, request, g, session, url_for, abort
from app import app
from app.controlador import ControlUsuario
from app.modelo import Usuario

control = ControlUsuario()


@app.route('/')
@app.route('/index')
def index():
#    user = control.getUsuarioById(1)
#    print user
#    user.setnombreUsuario("OtroNombre")
#    control.modificarUsuario(user)
#    print "Creamos uno nuevo"
#    usuario = Usuario(nombreUsuario="Mauro", contrasena="puto", nombre="Mauro", apellido="Korea", telefono="123-321-123", CI = 123321, email="cacao@puto.com")
#
#    control.nuevoUsuario(usuario)
#
#    print "Luego de crear"
#    users = control.getUsuarios()
#    print users
#
#    control.eliminarUsuario(usuario)
#
#    print "Luego de eliminar"
#    users = control.getUsuarios()
#    print users

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        
        user = comprobarLogueo(request.form['nombreUsuario'],request.form['contrasena'])
        
        if (not user):
            error = "Usuario o Contrasena incorrectos, intente de nuevo"        
        else:
            usuario = user.nombre
            session['logged_in'] = True
            session['usuario'] = usuario
            flash('Estas logueado')
    
    if (error):
        flash("Ha ocurrido un error : " + error)
            
    return redirect( url_for('index') )


def comprobarLogueo(user, password):
    usuarioFormulario = Usuario()
    usuarioFormulario.nombreUsuario = user
    usuarioFormulario.contrasena = password
    
    usuario = control.comprobarLogin(usuarioFormulario)
    
    print usuario
    
    return usuario
    
    
    
    
    

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('usuario', None)
    flash('Has salido del sistema')
    return redirect(url_for('index'))
