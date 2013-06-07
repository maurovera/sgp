#INDEX
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlHistorialItems
from app.modelo import HistorialItems
from contextlib import closing

control = ControlHistorialItems()


def listadoHistorialItems():
    ''' Devuelve un listado de los HistorialItems'''
    lista = None
    r = True
    if(r):
        lista = control.getHistorialItems()
    else:
        flash("Error. Lista no devuelta")
    return lista



@app.route('/hItem')
def indexHistorialItems():
    ''' Devuelve los datos de un HistorialItems en Concreto '''
    hItems = listadoHistorialItems();
    return render_template('indexHistorialItems.html', hItems = hItems)


@app.route('/hItem/eliminar')
@app.route('/hItem/eliminar/<id>')
def eliminarHistorialItems(id=None):
    if(id):
        hItem = control.getHistorialItemsById(id)
        
        if(hItem):
            
            r= control.eliminarHistorialItems(hItem)
            if(r["estado"] == True):
                flash("Se elimino con exito el HistorialItem: " + hItem.idHistorialItems)
            else:
                flash("Ocurrio un error: "+ r["mensaje"])
        else :
            flash("Ocurrio un error durante la eliminacion")
    
    return redirect(url_for('indexHistorialItems'))

         


@app.route('/hItem/nuevo', methods=['GET','POST'])
def nuevoHistorialItems():
    ''' Crea un nuevo HistorialItems '''
    #Si recibimos algo por post
    
    
    
    if request.method == 'POST' :
        
        print request.form['idHistorialItems']
        print request.form['tipoModificacion']
        print request.form['fechaModificacion']
        
        idHistorialItems = request.form['idHistorialItems']
        tipoModificacion = request.form['tipoModificacion']
        fechaModificacion = request.form['fechaModificacion']
        
        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente 
        #con un metodo kachiai
        if(idHistorialItems and tipoModificacion and fechaModificacion):
            hItem = HistorialItems()
            hItem.idHistorialItems = idHistorialItems
            hItem.tipoModificacion = tipoModificacion
            hItem.fechaModificacion = fechaModificacion
            
            
            r = control.nuevoHistorialItems(hItem)
            if(r["estado"] == True):
                flash("Exito, se creo un nuevo usuario")    
            else :
                flash("Ocurrio un error : " + r["mensaje"])
                    
    return redirect(url_for('indexHistorialItems'))


@app.route('/hItem/modificar', methods=['GET','POST'])
def modificarHistorialItems():
    ''' Modifica un HistorialItems '''
    
    
    
    if request.method == 'POST' :
        
        print request.form['idHistorialItems']
        print request.form['tipoModificacion']
        print request.form['fechaModificacion']
        
        
        idHistorialItems = request.form['idHistorialItems']
        tipoModificacion = request.form['tipoModificacion']
        fechaModificacion = request.form['fechaModificacion']
        
        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente 
        #con un metodo kachiai
        if(idHistorialItems and tipoModificacion and fechaModificacion):
            hItem = control.getHistorialItemsById(id)
            if (hItem):
                hItem.idHistorialItems = idHistorialItems
                hItem.tipoModificacion = tipoModificacion
                hItem.fechaModificacion = fechaModificacion    
                r = control.modificarHistorialItems(hItem)
                if( r["estado"] == True ):
                    flash("Modficado con exito")
                else:
                    flash("Ocurrio un error : " + r["mensaje"])
                       
        
    return redirect(url_for('indexHistorialItems'))

