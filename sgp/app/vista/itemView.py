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
#controladorrol = ControlRol()
#----------------------------------------------
valorGlobal = 0
#def busquedaPorNombre(nombre):
#    ''' Devuelve un listado de los tipo de item que coincidan con un nombre '''
#    lista = None
#    r = True
#    if(r):
#        lista = control.buscarPorNombre(nombre)
#    else:
#        flash("Error. Lista no devuelta")
#    return lista

def listadoItem(idFase):
    ''' Devuelve un listado de los tipo item '''
    lista = None
    r = True
    if(r):
        lista = control.getItemByFase(idFase)
    else:
        flash("Error. Lista no devuelta")
    return lista

@app.route('/item')
@app.route('/item/<idProyecto>/<idFase>')
def indexItem(idProyecto=None,idFase=None):
    ''' Devuelve los datos de un item en Concreto '''
    items = listadoItem(idFase);
    return render_template('indexItem.html', items = items, idProyecto = idProyecto, idFase = idFase)


@app.route('/item/eliminar')
@app.route('/item/eliminar/<idProyecto>/<idFase>/<id>')
def eliminarItem(idProyecto=None,idFase=None,id=None):
    if(id):
        item = control.getItemById(id)
        
        if(item):
            
            r= control.eliminarItem(item)
            if(r["estado"] == True):
                flash("Se elimino con exito el item: " + str( item.numero) )
            else:
                flash("Ocurrio un error: "+ r["mensaje"])
        else :
            flash("Ocurrio un error durante la eliminacion")
    
    return redirect(url_for('indexItem', idProyecto=idProyecto, idFase=idFase))

         


@app.route('/item/nuevo', methods=['GET','POST'])
def nuevoItem():
    ''' Crea un nuevo Item '''
    #Si recibimos algo por post
    
    
    
    if request.method == 'POST' :
        
        
        #print request.form['nombre']
        #print request.form['codigo']
        #print request.form['descripcion']
        
        
        numero = request.form['numero']
        #eliminado = request.form['eliminado']
        #if eliminado == 1:
        #    eliminado= True
        #elif eliminado == 0:
        #    eliminado = False
            
                
        #ultimaVersion = request.form['ultimaVersion']
        idProyecto = request.form['idProyecto']
        #aca tiene que ser idTipoItem jajajaja
        idFase = request.form['idFase']
        
        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente 
        #con un metodo kachiai
        if(numero and idFase):
            item = Item()
            item.numero = numero
            item.eliminado = False
            item.ultimaVersion = 0
            item.idFase = idFase
            #tipoItem.idProyecto = idProyecto
            
            r = control.nuevoItem(item)
            if(r["estado"] == True):
                flash("Exito, se creo un nuevo item")    
            else :
                flash("Ocurrio un error : " + r["mensaje"])
                    
    return redirect(url_for('indexItem', idProyecto=idProyecto, idFase=idFase ))


@app.route('/item/modificar', methods=['GET','POST'])
def modificarItem():
    ''' Modifica un item '''
    
    
    
    if request.method == 'POST' :
        
       
        #print request.form['nombre']
        #print request.form['codigo']
        #print request.form['descripcion']
        #print request.form['idTipoItem']
        
        id = request.form['idItemActual']
        
        numero = request.form['numero']
        #eliminado = request.form['eliminado']
        #if eliminado == 1:
        #    eliminado= True
        #elif eliminado == 0:
        #    eliminado = False

        #ultimaVersion = request.form['ultimaVersion']
        
        idProyecto = request.form['idProyecto']
        idFase = request.form['idFase']
        
        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente 
        #con un metodo kachiai
        if(id and numero):
            item = control.getItemById(id)
            if (item):
                item.numero = numero
                #item.eliminado = eliminado
                #item.ultimaVersion = ultimaVersion
                
                
                    
                r = control.modificarItem(item)
                if( r["estado"] == True ):
                    flash("Modficado con exito el item")
                else:
                    flash("Ocurrio un error : " + r["mensaje"])
                       
        
    return redirect(url_for('indexItem', idProyecto=idProyecto, idFase=idFase))

#@app.route("/item/buscar")
#@app.route("/item/buscar/<nombrebuscado>")
#def buscarTipoItem(nombrebuscado):
#    ''' Devuelve una lista de tipo de items que coincidan con el nombre proporcionado '''
#    print "Helloooooowww"
#    tipoItems = busquedaPorNombre(nombrebuscado);
#    return render_template('indexTipoItem.html', tipoItems = tipoItems)


#---------Esta parte es en donde se crean los datos del item---------------


@app.route("/item/datos")
@app.route("/item/datos/<idItemActual>")
def datos(idItemActual):
    '''Se encarga render a un pantalla para cargar datos de item '''
    t = control.getItemById(idItemActual)
    return render_template('datosItem.html', item = t)

#si no funciona poner atributos/tipoItem/nuevo
@app.route("/item/datos/nuevo", methods=['GET','POST'])
def nuevaDatosItem():
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
        
        

    return redirect(url_for('datos',idItemActual = idItemActual))



@app.route("/item/datos/modificar", methods=['GET','POST'])
def modificarDatosItem():
    '''Se encarga de modificar datos de un  item'''
    #version = request.form['version']
    
    
    #complejidad = request.form['complejidad']
    #prioridad = request.form['prioridad']
    #estado = request.form['estado']
    idItemActual = request.form['idItemActual']
    idDatosItem = request.form['idItem']
    
    
    if(idItemActual and idDatosItem):
        #anga
        
        datos = controladorDatosItem.getDatosItemById(idDatosItem)
        #datos.version = version
        #datos.complejidad = complejidad
        #datos.prioridad = prioridad
        datos.estado = "caducado"
        
        #Aca Modifica los datos viejos 
        r = controladorDatosItem.modificarDatosItem(datos)
        #aca carga un nuevo dato
        
        
        if( r["estado"] == True ):
            flash("Se modifico los datos con exito")
        else:
            flash("Ocurrio un error : " + r["mensaje"])


    else :
        flash("Ocurrio un error, debe completar correctamente el formulario")

    
    return redirect(url_for('datos',idItemActual = idItemActual))


@app.route("/item/datos/volver", methods=['GET','POST'])
def volverDatosItem():
    '''Se encarga de modificar datos de un  item'''
    version = request.form['version']
    #complejidad = request.form['complejidad']
    #prioridad = request.form['prioridad']
    #estado = request.form['estado']
    idItemActual = request.form['idItemActual']
    idDatosItem = request.form['idItem']
    
    if(version and idItemActual and idDatosItem):
        #anga
        item = control.getItemById(idItemActual)
        item.ultimaVersion = version
        p = control.modificarItem(item)
        
        #datos.version = version
        #datos.complejidad = complejidad
        #datos.prioridad = prioridad
        datos = controladorDatosItem.getDatosItemById(idDatosItem)
        datos.estado = "actual"
        
        controladorDatosItem.modificarDatosItem(datos)
        
        if( p["estado"] == True ):
            flash("Se volvio a esta version de item")
        else:
            flash("Ocurrio un error : " + p["mensaje"])


    else :
        flash("Ocurrio un error, debe completar correctamente el formulario")

    return redirect(url_for('datos',idItemActual = idItemActual))





@app.route("/item/datos/eliminar")
@app.route("/item/datos/eliminar/<idItemActual>/<idItem>")
def eliminarDatosItem(idItemActual,idItem):
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

    return redirect(url_for('datos', idItemActual= idItemActual))


#@app.route("/item/return")
#@app.route("/item/return/<idItemActual>/<idProyecto>/<idFase>")
#def returnDatosItem(idItemActual,idProyecto, idFase):
#    return redirect(url_for('indexItem', idProyecto= idProyecto, idFase=idFase ))


