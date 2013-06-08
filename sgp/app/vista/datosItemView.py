#INDEX
import datetime
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlItem
from app.modelo import Item
from app.modelo import AtributoDeItem
from app.modelo import DatosItem
from app.controlador import ControlDatosItem
from contextlib import closing

#---------------------------------------------
# no se si sirve de algo esto
from app.controlador import ControlUsuario
from app.controlador import ControlPermiso
from app.controlador import ControlTipoItem
from app.controlador import ControlAtributoDeItem
from app.modelo import Usuario
from app.controlador import ControlRelacion
from app.controlador import ControlFase
#----------------------------------------------
controlRelacion = ControlRelacion()
control = ControlItem()
controlFase = ControlFase()
# control == controlador
controladorDatosItem = ControlDatosItem()

#........... no se si sirve-----------------------------
controladorusuario = ControlUsuario()
controlTipoItem = ControlTipoItem()
controlAtributoDeItem = ControlAtributoDeItem()


#---------Esta parte es en donde se crean los datos del item---------------


@app.route("/item/datos")
@app.route("/item/datos/<idItemActual>/<idProyecto>")
def datos(idItemActual, idProyecto = None):
    '''Se encarga render a un pantalla para cargar datos de item '''
    t = control.getItemById(idItemActual)
    tipoItem = controlTipoItem.getTipoItemById(t.idTipoItem)
    atributos = list(tipoItem.atributosPorTipoItem)
    return render_template('datosItem.html', item = t, idProyecto =  idProyecto, atributos = atributos)

#si no funciona poner atributos/tipoItem/nuevo
@app.route("/item/datos/nuevo")
@app.route("/item/datos/nuevo/<idProyecto>", methods=['GET','POST'])
def nuevaDatosItem(idProyecto):
    '''Se encarga de Agregar nuevos datos a un item'''
    version = request.form['version']
    complejidad = request.form['complejidad']
    prioridad = request.form['prioridad']
    #estado = request.form['estado']
    idTipoItem = request.form['idTipoItem']
    idItemActual = request.form['idItemActual']

    if(version and complejidad and prioridad and idItemActual and idTipoItem):
        #anga
        item = control.getItemById(idItemActual)
        datos = DatosItem()
        datos.version = version
        datos.complejidad = complejidad
        datos.prioridad = prioridad
        datos.estado = "inicial"
        datos.idItemActual = idItemActual

#------------------------------- modificamos la version = ultversion en item
        item.ultimaVersion = version

        #aqui se utiliza el controlador para agregar el dato
        r = control.agregarDatosItem(item,datos)
        #print tipoItem.atributo
        if( r["estado"] == True ):
            #flash("Se agrego el dato con exito")
            #Cargamos los atributos
            print "Empezamos a meter los atributos por item"
            tipoItem = controlTipoItem.getTipoItemById(idTipoItem)
            atributos = list(tipoItem.atributosPorTipoItem)
            #Recorremos los atributos que pertenecen al tipo
            for atributo in atributos :
                valor = request.form[''+atributo.nombre]
                atributoDeItem = AtributoDeItem()
                atributoDeItem.valor = valor
                atributoDeItem.idAtributoPorTipoItem = atributo.idAtributosPorTipoItem
                controlAtributoDeItem.nuevoAtributoDeItem(atributoDeItem)
                controladorDatosItem.agregarAtributoDeItem(datos, atributoDeItem)
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

    datos.estado = "inicial"
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

@app.route("/item/datos/listo")
@app.route("/item/datos/listo/<idItem>/<idItemActual>/<idProyecto>")
def estadoListoDatosItem(idItem= None, idItemActual = None, idProyecto = None ):
    '''Estado Listo : Cuando no vas a tocar y puede ser aprobado o rechazado'''

    datos = controladorDatosItem.getDatosItemById(idItem)
    datos.estado = "listo"
    p= controladorDatosItem.modificarDatosItem(datos)

    if( p["estado"] == True ):
        flash("El estado del item ha sido modificado")
    else:
        flash("Ocurrio un error : " + p["mensaje"])


    return redirect(url_for('datos',idItemActual = idItemActual, idProyecto = idProyecto))

@app.route("/item/datos/aprobado")
@app.route("/item/datos/aprobado/<idItem>/<idItemActual>/<idProyecto>")
def estadoAprobadoDatosItem(idItem= None, idItemActual = None, idProyecto = None ):
    '''Estado Aprobado '''
    relaciones =  controlRelacion.getItemsAntecesores(idItemActual)
    # si relaciones no tiene ningun antecesor
    if relaciones != []:
        for r in relaciones:
            if r.tipo == 'Antecesor-Sucesor':
                datos = controladorDatosItem.getDatosItemById(idItem)
                datos.estado = "aprobado"
                p= controladorDatosItem.modificarDatosItem(datos)

                if( p["estado"] == True ):
                    flash("El estado del item ha sido modificado")
                else:
                    flash("Ocurrio un error : " + p["mensaje"])
            else:
                #flash("tiene solo una relacion Padre-Hijo y no puede ser aprobado")
                itemCabecera = control.getItemById(idItemActual)
                fase = controlFase.getFaseById(itemCabecera.idFase)
                if(fase.numeroFase == 1):
                    datos = controladorDatosItem.getDatosItemById(idItem)
                    datos.estado = "aprobado"
                    p= controladorDatosItem.modificarDatosItem(datos)
                    flash("El estado del item ha sido modificado")
                else:
                    flash("tiene solo una relacion Padre-Hijo, no es de la primera Fase y no se puede aprobar")
                 

    else:
        itemCabecera = control.getItemById(idItemActual)
        fase = controlFase.getFaseById(itemCabecera.idFase)
        if(fase.numeroFase == 1):
            datos = controladorDatosItem.getDatosItemById(idItem)
            datos.estado = "aprobado"
            p= controladorDatosItem.modificarDatosItem(datos)
            flash("El estado del item ha sido modificado")
        else:
            flash("No posee antecesores, no puede aprobarse el item")       

    
    return redirect(url_for('datos',idItemActual = idItemActual, idProyecto = idProyecto))

@app.route("/item/datos/rechazado")
@app.route("/item/datos/rechazado/<idItem>/<idItemActual>/<idProyecto>")
def estadoRechazadoDatosItem(idItem= None, idItemActual = None, idProyecto = None ):
    '''Estado Rechazado'''

    datos = controladorDatosItem.getDatosItemById(idItem)
    datos.estado = "rechazado"
    p= controladorDatosItem.modificarDatosItem(datos)

    if( p["estado"] == True ):
        flash("El estado del item ha sido modificado")
    else:
        flash("Ocurrio un error : " + p["mensaje"])


    return redirect(url_for('datos',idItemActual = idItemActual, idProyecto = idProyecto))