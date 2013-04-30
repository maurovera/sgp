#INDEX
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlTipoItem
from app.modelo import TipoItem
from contextlib import closing

control = ControlTipoItem()



def busquedaPorNombre(nombre):
    ''' Devuelve un listado de los tipo de item que coincidan con un nombre '''
    lista = None
    r = True
    if(r):
        lista = control.buscarPorNombre(nombre)
    else:
        flash("Error. Lista no devuelta")
    return lista

def listadoTipoItem():
    ''' Devuelve un listado de los tipo item '''
    lista = None
    r = True
    if(r):
        lista = control.getTipoItems()
    else:
        flash("Error. Lista no devuelta")
    return lista

@app.route('/tipoItem')
def indexTipoItem():
    ''' Devuelve los datos de un Tipo item en Concreto '''
    tipoItems = listadoTipoItem();
    return render_template('indexTipoItem.html', tipoItems = tipoItems)


@app.route('/tipoItem/eliminar')
@app.route('/tipoItem/eliminar/<id>')
def eliminarTipoItem(id=None):
    if(id):
        tipoItem = control.getTipoItemById(id)
        
        if(tipoItem):
            
            r= control.eliminarTipoItem(tipoItem)
            if(r["estado"] == True):
                flash("Se elimino con exito el tipo item: " + tipoItem.nombre)
            else:
                flash("Ocurrio un error: "+ r["mensaje"])
        else :
            flash("Ocurrio un error durante la eliminacion")
    
    return redirect(url_for('indexTipoItem'))

         


@app.route('/tipoItem/nuevo', methods=['GET','POST'])
def nuevoTipoItem():
    ''' Crea un nuevo Tipo Item '''
    #Si recibimos algo por post
    
    
    
    if request.method == 'POST' :
        
        
        print request.form['nombre']
        print request.form['codigo']
        print request.form['descripcion']
        
        
        nombre = request.form['nombre']
        codigo = request.form['codigo']
        descripcion = request.form['descripcion']
        
        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente 
        #con un metodo kachiai
        if(nombre and codigo and descripcion):
            tipoItem = TipoItem()
            tipoItem.nombre = nombre
            tipoItem.codigo = codigo
            tipoItem.descripcion = descripcion
            
            
            r = control.nuevoTipoItem(tipoItem)
            if(r["estado"] == True):
                flash("Exito, se creo un nuevo tipo item")    
            else :
                flash("Ocurrio un error : " + r["mensaje"])
                    
    return redirect(url_for('indexTipoItem'))


@app.route('/tipoItem/modificar', methods=['GET','POST'])
def modificarTipoItem():
    ''' Modifica un tipo item '''
    
    
    
    if request.method == 'POST' :
        
       
        print request.form['nombre']
        print request.form['codigo']
        print request.form['descripcion']
        print request.form['idTipoItem']
        
        id = request.form['idTipoItem']
        
        nombre = request.form['nombre']
        codigo = request.form['codigo']
        descripcion = request.form['descripcion']
        
        
        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente 
        #con un metodo kachiai
        if(id and nombre and codigo and descripcion):
            tipoItem = control.getTipoItemById(id)
            if (tipoItem):
                tipoItem.nombre = nombre
                tipoItem.codigo = codigo
                tipoItem.descripcion = descripcion
                
                    
                r = control.modificarTipoItem(tipoItem)
                if( r["estado"] == True ):
                    flash("Modficado con exito")
                else:
                    flash("Ocurrio un error : " + r["mensaje"])
                       
        
    return redirect(url_for('indexTipoItem'))

@app.route("/tipoItem/buscar")
@app.route("/tipoItem/buscar/<nombrebuscado>")
def buscarTipoItem(nombrebuscado):
    ''' Devuelve una lista de tipo de items que coincidan con el nombre proporcionado '''
    print "Helloooooowww"
    tipoItem = busquedaPorNombre(nombrebuscado);
    return render_template('indexTipoItem.html', tipoItem = tipoItem)
