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
from app.controlador import ControlTipoItem
from app.controlador import ControlFase
from app.modelo import Usuario
#----------------------------------------------

control = ControlItem()
# control == controlador
controladorDatosItem = ControlDatosItem()
controlTipoItem = ControlTipoItem()
controlFase = ControlFase()

#........... no se si sirve-----------------------------
controladorusuario = ControlUsuario()
#controladorrol = ControlRol()
#----------------------------------------------

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


def listadoTipoItem(idFase):
    ''' Retorna una lista de Tipos de Item que corresponde a la fase'''
    lista = controlTipoItem.getTipoItemByFase(idFase)
    return lista


@app.route('/item')
@app.route('/item/<idProyecto>/<idFase>')
def indexItem(idProyecto=None,idFase=None):
    ''' Devuelve los datos de un item en Concreto '''
    items = listadoItem(idFase);
    tipoItems = listadoTipoItem(idFase);
    return render_template('indexItem.html', items = items, idProyecto = idProyecto, idFase = idFase, tipoItems = tipoItems)


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



        idProyecto = request.form['idProyecto']
        idFase = request.form['idFase']
        idTipoItem = request.form['idTipoItem']

        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente
        #con un metodo kachiai
        if(idFase and idTipoItem):
            #Se necesita cargar todos los atributos del tipo item.
            item = Item()
            item.idFase = idFase
            item.idTipoItem = idTipoItem
            item.eliminado = False

            fase = controlFase.getFaseById(idFase)
            tipoItem = controlTipoItem.getTipoItemById(idTipoItem)
            numero = len( list(fase.items) ) + 1
            item.numero = numero
            item.ultimaVersion = 0


            r = control.nuevoItem(item)
            if (r["estado"] == True):
                #Aca tenemos que mandar a la pantalla de carga del item
                if (fase.estado != "desarrollo"):
                    fase.estado = "desarrollo"
                    controlFase.modificarFase(fase)

                return redirect(url_for('datos', idProyecto = idProyecto, idItemActual = item.idItemActual ))
            else:
                flash("Ocurrio un error " + r["mensaje"])

    return redirect(url_for('indexItem', idProyecto=idProyecto, idFase=idFase))


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

