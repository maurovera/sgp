#INDEX
import datetime
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlItem
from app.modelo import Item
from app.modelo import DatosItem
from app.controlador import ControlDatosItem
from contextlib import closing

#---------------------------------------------
# no se si sirve de algo esto
from app.controlador import ControlUsuario
from app.controlador import ControlPermiso
from app.modelo import Usuario
#----------------------------------------------

control = ControlItem() 
# control == controlador
controladorDatosItem = ControlDatosItem()

#........... no se si sirve-----------------------------
controladorusuario = ControlUsuario()




#---------Esta parte es en donde se crean los datos del item---------------


@app.route("/item/datos")
@app.route("/item/datos/<idItemActual>/<idProyecto>")
def datos(idItemActual, idProyecto = None):
    '''Se encarga render a un pantalla para cargar datos de item '''
    t = control.getItemById(idItemActual)
    return render_template('datosItem.html', item = t, idProyecto =  idProyecto)

#si no funciona poner atributos/tipoItem/nuevo
@app.route("/item/datos/nuevo")
@app.route("/item/datos/nuevo/<idProyecto>", methods=['GET','POST'])
def nuevaDatosItem(idProyecto):
    '''Se encarga de Agregar nuevos datos a un item'''
    version = request.form['version']
    complejidad = request.form['complejidad']
    prioridad = request.form['prioridad']
    #estado = request.form['estado']
    
    idItemActual = request.form['idItemActual']

    if(version and complejidad and prioridad and idItemActual):
        #anga
        item = control.getItemById(idItemActual)
        datos = DatosItem()
        datos.version = version
        datos.complejidad = complejidad
        datos.prioridad = prioridad
        datos.estado = "actual"
        datos.idItemActual = idItemActual
        
#------------------------------- modificamos la version = ultversion en item
        item.ultimaVersion = version
        #aqui se utiliza el controlador para agregar el dato
        r = control.agregarDatosItem(item,datos)
        #print tipoItem.atributo
        if( r["estado"] == True ):
            flash("Se agrego el dato con exito")
        else:
            flash("Ocurrio un error : " + r["mensaje"])


    else :
        flash("Ocurrio un error, debe completar correctamente el formulario")
        
        

    return redirect(url_for('datos',idItemActual = idItemActual, idProyecto = idProyecto))



#@app.route("/item/datos/modificar", methods=['GET','POST'])
#def modificarDatosItem():
    
    #version = request.form['version']
    
    
    #complejidad = request.form['complejidad']
    #prioridad = request.form['prioridad']
    #estado = request.form['estado']
    #idItemActual = request.form['idItemActual']
    #idDatosItem = request.form['idItem']
    
    
    #if(idItemActual and idDatosItem):
        #anga
        
        #datos = controladorDatosItem.getDatosItemById(idDatosItem)
        #datos.version = version
        #datos.complejidad = complejidad
        #datos.prioridad = prioridad
        #datos.estado = "caducado"
        
        #Aca Modifica los datos viejos 
        #r = controladorDatosItem.modificarDatosItem(datos)
        #aca carga un nuevo dato
        
        
        #if( r["estado"] == True ):
            #flash("Se modifico los datos con exito")
        #else:
            #flash("Ocurrio un error : " + r["mensaje"])


    #else :
        #flash("Ocurrio un error, debe completar correctamente el formulario")

    
    #return redirect(url_for('datos',idItemActual = idItemActual))


@app.route("/item/datos/eliminar")
@app.route("/item/datos/eliminar/<idItemActual>/<idProyecto>/<idItem>")
def eliminarDatosItem(idItemActual,idProyecto, idItem ):
    '''Se encarga de eliminar un atributo de un tipo de item'''
    print idItemActual
    print idItem

    if ( idItemActual and idItem):
        p = control.getItemById(idItemActual)
        datosRemover = controladorDatosItem.getDatosItemById(idItem)
        # aqui se usa el controlador del atributo por tipo item para eliminar
        r = control.quitarDatosItem(p, datosRemover)
        # se elimina completamente el dato
        p = controladorDatosItem.eliminarDatosItem(datosRemover)
        if( r["estado"] == True ):
            flash("Se ha removido el dato del item con exito")
        else:
            flash("Ocurrio un error : " + r["mensaje"])
    else:
        flash("Ocurrio un error, intente de nuevo")

    return redirect(url_for('datos', idItemActual= idItemActual, idProyecto = idProyecto))


@app.route("/item/return")
@app.route("/item/return/<idProyecto>/<idFase>")
def returnDatosItem(idProyecto, idFase):
    return redirect(url_for('indexItem', idProyecto = idProyecto, idFase=idFase ))



@app.route("/item/datos/revertir")
@app.route("/item/datos/revertir/<idItem>/<idItemActual>/<idProyecto>")
def revertirDatosItem(idItem= None, idItemActual = None, idProyecto = None ):
    '''Se encarga de modificar datos de un  dato'''
    item = control.getItemById(idItemActual)
    datos = controladorDatosItem.getDatosItemById(idItem)
    
    datos.estado = "actual"
    item.ultimaVersion = datos.version
        
    p = control.modificarItem(item)
    controladorDatosItem.modificarDatosItem(datos)
        
    if( p["estado"] == True ):
        flash("Se volvio a esta version de item")
    else:
        flash("Ocurrio un error : " + p["mensaje"])


    
    return redirect(url_for('datos',idItemActual = idItemActual, idProyecto = idProyecto))


@app.route("/item/datos/caducar")
@app.route("/item/datos/caducar/<idItem>/<idItemActual>/<idProyecto>")
def caducarDatosItem(idItem= None, idItemActual = None, idProyecto = None ):
    '''Se encarga de modificar datos de un  dato'''
    
    datos = controladorDatosItem.getDatosItemById(idItem)
    datos.estado = "caducado"
    p= controladorDatosItem.modificarDatosItem(datos)
        
    if( p["estado"] == True ):
        flash("Se volvio a esta version de item")
    else:
        flash("Ocurrio un error : " + p["mensaje"])


    
    return redirect(url_for('datos',idItemActual = idItemActual, idProyecto = idProyecto))

