#INDEX
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlRelacion
from app.controlador import ControlItem
from app.modelo import Item
from app.modelo import Relacion
from contextlib import closing

control = ControlRelacion()
controlItem = ControlItem()


#def busquedaPorNombre(nombre):
#    ''' Devuelve un listado de los usuarios que coincidan con un nombre '''
#    lista = None
#    r = True
#    if(r):
#        lista = control.buscarPorNombre(nombre)
#    else:
#        flash("Error. Lista no devuelta")
#    print lista
#    return lista

def listadoRelaciones():
    ''' Devuelve un listado de las Relaciones '''
    lista = None
    r = True
    if(r):
        lista = control.getRelaciones()
    else:
        flash("Error. Lista no devuelta")
    return lista

def listadoItems():
    lista = controlItem.getItems()
    
    return lista



@app.route('/relacion')
def indexRelacion():
    ''' Devuelve los datos de una Relacion en Concreto '''
    relaciones = listadoRelaciones();
    items = listadoItems();
    return render_template('indexRelacion.html', relaciones = relaciones, items = items)


@app.route('/relacion/eliminar')
@app.route('/relacion/eliminar/<id>')
def eliminarRelacion(id=None):
    if(id):
        relacion = control.getRelacionById(id)
        
        if(relacion):
            
            r= control.eliminarRelacion(relacion)
            if(r["estado"] == True):
                flash("Se elimino con exito la relacion: " + str(relacion.idRelacion))
            else:
                flash("Ocurrio un error: "+ r["mensaje"])
        else :
            flash("Ocurrio un error durante la eliminacion")
    
    return redirect(url_for('indexRelacion'))

         


@app.route('/relacion/nueva', methods=['GET','POST'])
def nuevaRelacion():
    ''' Crea un nueva Relacion '''
    #Si recibimos algo por post
    
    #tipo = request.form['tipo']
    idSucesor = request.form['idSucesor']
    idAntecesor = request.form['idAntecesor']
    #print tipo
    print idSucesor
    print idAntecesor
    item1 = controlItem.getItemById(idSucesor)
    item2 = controlItem.getItemById(idAntecesor)
    
    # esto es para controlar el tipo nada mas que sea antecesor o sucesor
    if item1.idFase == item2.idFase:
        tipo = "Padre-Hijo"
    else:
        tipo = "Antecesor-Sucesor"    
    #---------------------------------------------------------------------
    # aca iria el algoritmo de deteccion de ciclos jejeje
    # acaaaaaaaaaa va el algoritmo de deteccion
    #--------------------------------------------------------------------
    # tiraria el mensaje con flash
    
    #---------------------------------------------------------------------
    
            
#         print "Estoy aca adentro del form..."
#         Si esta todo completo (Hay que hacer una verificacion probablemente 
#         con un metodo kachiai
    if(tipo and idSucesor and idAntecesor):
        relacion = Relacion()
        relacion.tipo = tipo
        relacion.idSucesor = idSucesor
        relacion.idAntecesor = idAntecesor
        
        r = control.nuevoRelacion(relacion)
        if(r["estado"] == True):
            flash("Exito, se creo una nueva relacion")    
        else :
            flash("Ocurrio un error : " + r["mensaje"])
                    
    return redirect(url_for('indexRelacion'))


@app.route('/relacion/modificar', methods=['GET','POST'])
def modificarRelacion():
    ''' Modifica una relacion '''
    
    
#     
#     if request.method == 'POST' :
#         
#         print request.form['nombreUsuario']
#         print request.form['nombre']
#         print request.form['apellido']
#         print request.form['CI']
#         print request.form['telefono']
#         print request.form['email']
#         print request.form['idUsuario']
#         
#         id = request.form['idUsuario']
#         nombreUsuario = request.form['nombreUsuario']
#         nombre = request.form['nombre']
#         apellido = request.form['apellido']
#         CI = request.form['CI']
#         telefono = request.form['telefono']
#         email = request.form['email']
#         contrasena = request.form['contrasena']
#         
#         print "Estoy aca adentro del form..."
#         #Si esta todo completo (Hay que hacer una verificacion probablemente 
#         #con un metodo kachiai
#         if(id and nombreUsuario and nombre and apellido and CI and telefono and email and contrasena):
#             usuario = control.getUsuarioById(id)
#             if (usuario):
#                 usuario.nombreUsuario = nombreUsuario
#                 usuario.nombre = nombre
#                 usuario.apellido = apellido
#                 usuario.CI = CI
#                 usuario.telefono = telefono
#                 usuario.email = email
#                 usuario.contrasena = contrasena
#                     
#                 r = control.modificarUsuario(usuario)
#                 if( r["estado"] == True ):
#                     flash("Modficado con exito")
#                 else:
#                     flash("Ocurrio un error : " + r["mensaje"])
#                        
#         
    return redirect(url_for('indexRelacion'))


