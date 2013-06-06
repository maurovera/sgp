#INDEX
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlMensaje
from app.modelo import Mensaje
from contextlib import closing

controlMensaje = ControlMensaje()



#def busquedaPorNombre(nombre):
#     ''' Devuelve un listado de los usuarios que coincidan con un nombre '''
#     lista = None
#     r = True
#     if(r):
#         lista = control.buscarPorNombre(nombre)
#     else:
#         flash("Error. Lista no devuelta")
#     print lista
#     return lista

def listadoMensaje():
    ''' Devuelve un listado de los usuarios '''
    lista = None
    r = True
    if(r):
        lista = controlMensaje.getMensaje()
    else:
        flash("Error. Lista no devuelta")
    return lista



@app.route('/mensaje')
def indexMensaje():
    ''' Devuelve los datos de un Usuario en Concreto '''
    mensajes = listadoMensaje();
    return render_template('indexMensaje.html', mensajes = mensajes)


@app.route('/mensaje/eliminar')
@app.route('/mensaje/eliminar/<id>')
def eliminarMensaje(id=None):
    if(id):
        mensaje = controlMensaje.getMensajeById(id)

        if(mensaje):

            r= controlMensaje.eliminarMensaje(mensaje)
            if(r["estado"] == True):
                flash("Se elimino con exito el mensaje: " + mensaje.titulo)
            else:
                flash("Ocurrio un error: "+ r["mensaje"])
        else :
            flash("Ocurrio un error durante la eliminacion")

    return redirect(url_for('indexMensaje'))


@app.route('/mensaje/mostrar')
@app.route('/mensaje/mostrar/<idMensaje>')
def mostrarMensaje(idMensaje=None):
    if(idMensaje):
        mensaje = controlMensaje.getMensajeById(idMensaje)
        mensaje.estado = 'leido'
        controlMensaje.modificarMensaje(mensaje)
        return render_template('verMensaje.html', mensaje = mensaje)
