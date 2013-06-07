#INDEX
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlHistorialLineaBase
from app.modelo import HistorialLineaBase
from contextlib import closing

control = ControlHistorialLineaBase()

def listadoHistorialLineaBase():
    ''' Devuelve un listado de los HistorialLineaBase '''
    lista = None
    r = True
    if(r):
        lista = control.getHistorialLineaBase()
    else:
        flash("Error. Lista no devuelta")
    return lista



@app.route('/hLB')
def indexHistorialLineaBase():
    ''' Devuelve los datos de un HLB en Concreto '''
    hLB = listadoHistorialLineaBase();
    return render_template('indexHistorialLineaBase.html', hLB = hLB)


@app.route('/hLB/eliminar')
@app.route('/hLB/eliminar/<id>')
def eliminarHistorialLineaBase(id=None):
    if(id):
        hLB = control.getHistorialLineaBaseById(id)
        
        if(hLB):
            
            r= control.eliminarHistorialLineaBase(hLB)
            if(r["estado"] == True):
                flash("Se elimino con exito el HistorialLineaBase: " + hLB.idHistorialLB)
            else:
                flash("Ocurrio un error: "+ r["mensaje"])
        else :
            flash("Ocurrio un error durante la eliminacion")
    
    return redirect(url_for('indexHistorialLineaBase'))

         


@app.route('/hLB/nuevo', methods=['GET','POST'])
def nuevoHistorialLineaBase():
    ''' Crea un nuevo HistorialLineaBase '''
    #Si recibimos algo por post
    
    
    
    if request.method == 'POST' :
        
        print request.form['idHistorialLB']
        print request.form['tipoOperacion']
        print request.form['fechaModificacion']
        
        idHistorialLB = request.form['idHistorialLB']
        tipoOperacion = request.form['tipoOperacion']
        fechaModificacion = request.form['fechaModificacion']
        
        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente 
        #con un metodo kachiai
        if(idHistorialLB and tipoOperacion and fechaModificacion):
            hLB = HistorialLineaBase()
            hLB.idHistorialLB = idHistorialLB
            hLB.tipoOperacion = tipoOperacion
            hLB.fechaModificacion = fechaModificacion
            r = control.nuevoHistorialLineaBase(hLB)
            if(r["estado"] == True):
                flash("Exito, se creo un nuevo usuario")    
            else :
                flash("Ocurrio un error : " + r["mensaje"])
                    
    return redirect(url_for('indexHistorialLineaBase'))


@app.route('/hLB/modificar', methods=['GET','POST'])
def modificarHistorialLineaBase():
    ''' Modifica un HistorialLineaBase '''
    
    
    
    if request.method == 'POST' :
        
        print request.form['idHistorialLB']
        print request.form['tipoOperacion']
        print request.form['fechaModificacion']
        
        idHistorialLB = request.form['idHistorialLB']
        tipoOperacion = request.form['tipoOperacion']
        fechaModificacion = request.form['fechaModificacion']
        
        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente 
        #con un metodo kachiai
        if(idHistorialLB and tipoOperacion and fechaModificacion):
            hLB = control.getHistorialLineaBaseById(id)
            if (hLB):
                hLB.idHistorialLB = idHistorialLB
                hLB.tipoOperacion = tipoOperacion
                hLB.fechaModificacion = fechaModificacion    
                r = control.modificarHistorialLineaBase(hLB)
                if( r["estado"] == True ):
                    flash("Modficado con exito")
                else:
                    flash("Ocurrio un error : " + r["mensaje"])
                       
        
    return redirect(url_for('indexHistorialLineaBase'))

