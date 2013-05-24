#INDEX
import datetime
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlTipoItem
from app.modelo import TipoItem
from app.modelo import AtributoPorTipoItem
from app.controlador import ControlAtributoPorTipoItem
from app.controlador import ControlFase
from contextlib import closing

#---------------------------------------------
# no se si sirve de algo esto
from app.controlador import ControlUsuario
from app.controlador import ControlPermiso
from app.modelo import Usuario
#----------------------------------------------

control = ControlTipoItem()
# control == controlador
controlFase = ControlFase()
controladorAtributoPorTipoItem = ControlAtributoPorTipoItem()

#........... no se si sirve-----------------------------
controladorusuario = ControlUsuario()
#controladorrol = ControlRol()
#----------------------------------------------

def busquedaPorNombre(nombre):
    ''' Devuelve un listado de los tipo de item que coincidan con un nombre '''
    lista = None
    r = True
    if(r):
        lista = control.buscarPorNombre(nombre)
    else:
        flash("Error. Lista no devuelta")
    return lista

def listadoTipoItem(idFase):
    ''' Devuelve un listado de los tipo item '''
    lista = None
    r = True
    if(r):
        lista = control.getTipoItemByFase(idFase)
    else:
        flash("Error. Lista no devuelta")
    return lista

def listadoTipoItemTodos():
    ''' Devuelve un listado de los tipo item '''
    lista = None
    r = True
    if(r):
        lista = control.getTipoItems()
    else:
        flash("Error. Lista no devuelta")
    return lista

@app.route('/tipoItem')
@app.route('/tipoItem/<idProyecto>/<idFase>')
def indexTipoItem(idProyecto=None,idFase=None):
    ''' Devuelve los datos de un Tipo item en Concreto '''
    tipoItems = listadoTipoItem(idFase);
    tipoItemsTodo = listadoTipoItemTodos();

    return render_template('indexTipoItem.html', tipoItems = tipoItems, idProyecto = idProyecto, idFase = idFase, tipoItemsTodo = tipoItemsTodo)


@app.route('/tipoItem/eliminar')
@app.route('/tipoItem/eliminar/<idProyecto>/<idFase>/<id>')
def eliminarTipoItem(idProyecto=None,idFase=None,id=None):
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

    return redirect(url_for('indexTipoItem', idProyecto=idProyecto, idFase=idFase))




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
        idProyecto = request.form['idProyecto']
        idFase = request.form['idFase']

        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente
        #con un metodo kachiai
        if(nombre and codigo and descripcion and idFase and idProyecto):
            tipoItem = TipoItem()
            tipoItem.nombre = nombre
            tipoItem.codigo = codigo
            tipoItem.descripcion = descripcion
            tipoItem.idFase = idFase
            tipoItem.idProyecto = idProyecto

            r = control.nuevoTipoItem(tipoItem)
            if(r["estado"] == True):
                fase = controlFase.getFaseById(idFase)
                if (fase.estado != "desarrollo"):
                    fase.estado = "desarrollo"
                    controlFase.modificarFase(fase)
                flash("Exito, se creo un nuevo tipo item")
            else :
                flash("Ocurrio un error : " + r["mensaje"])

    return redirect(url_for('indexTipoItem', idProyecto=idProyecto, idFase=idFase ))


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

        idProyecto = request.form['idProyecto']
        idFase = request.form['idFase']

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


    return redirect(url_for('indexTipoItem', idProyecto=idProyecto, idFase=idFase))

@app.route("/tipoItem/buscar")
@app.route("/tipoItem/buscar/<nombrebuscado>")
def buscarTipoItem(nombrebuscado):
    ''' Devuelve una lista de tipo de items que coincidan con el nombre proporcionado '''
    print "Helloooooowww"
    tipoItems = busquedaPorNombre(nombrebuscado);
    return render_template('indexTipoItem.html', tipoItems = tipoItems)




@app.route("/tipoItem/importarTipoItem")
@app.route("/tipoItem/importarTipoItem/<idProyecto>/<idFase>", methods=['GET','POST'])
def importarTipoItem(idProyecto, idFase):

    id = request.form["idTipoItem"]
    print id
    print "este el tipo item seleccionadoooooooooooooooooooooooooo "
    print request.form['nombre']
    print request.form['codigo']
    print request.form['descripcion']
    nombre = request.form['nombre']
    codigo = request.form['codigo']
    descripcion = request.form['descripcion']
    idPro = idProyecto
    idFas = idFase

    id1 =  control.getTipoItemById(id)


    if(nombre and codigo and descripcion and idFas and idPro):
            tipoItem = TipoItem()
            tipoItem.nombre = nombre
            tipoItem.codigo = codigo
            tipoItem.descripcion = descripcion
            tipoItem.idFase = idFas
            tipoItem.idProyecto = idPro

            r = control.nuevoTipoItem(tipoItem)
            if(r["estado"] == True):
                flash("Exito, se creo un nuevo tipo item")
            else :
                flash("Ocurrio un error : " + r["mensaje"])

    #se encarga de los atributos de item
    listadoDeAtributos = controladorAtributoPorTipoItem.getAtributoPorTipoItemByTipoItem(id)
    for unAtributo in listadoDeAtributos:
        nuevo = AtributoPorTipoItem()
        nuevo.idTipoItem = tipoItem.idTipoItem
        nuevo.nombre = unAtributo.nombre
        nuevo.tipo = unAtributo.tipo
        nuevo.valorPorDefecto = unAtributo.valorPorDefecto
        #aqui se utiliza el controlador para agregar el atributo
        control.agregarAtributoPorTipoItem(tipoItem,nuevo)


    #idProyecto = request.form['idProyecto']
    #idFase = request.form['idFase']

    #nombre de la funcion y los parametros
    return redirect(url_for('indexTipoItem', idProyecto = idProyecto, idFase = idFase))
#---------Esta parte es en donde se crean los atributos del item---------------


@app.route("/tipoItem/atributo")
@app.route("/tipoItem/atributo/<idTipoItem>")
def atributo(idTipoItem):
    '''Se encarga render a un pantalla para cargar atributos por tipo item '''
    t = control.getTipoItemById(idTipoItem)
    return render_template('atributoPorTipoItem.html', tipoItem = t )

@app.route("/tipoItem/lista")
@app.route("/tipoItem/lista/<idTipoItem>")
def lista(idTipoItem):
    '''Se encarga render a un pantalla para cargar atributos por tipo item '''
    t = control.getTipoItemById(idTipoItem)
    return render_template('listadoAtributos.html', tipoItem = t )


#si no funciona poner atributos/tipoItem/nuevo
@app.route("/tipoItem/atributos/nuevo", methods=['GET','POST'])
def nuevaAtributoTipoItem():
    '''Se encarga de Agregar nuevos atributos a un tipo de item'''
    nombre = request.form['nombre']
    tipo = request.form['tipo']
    valorPorDefecto = request.form['valorPorDefecto']

    idTipoItem = request.form['idTipoItem']

    if(nombre and tipo and valorPorDefecto and idTipoItem):
        #anga
        tipoItem = control.getTipoItemById(idTipoItem)
        atributo = AtributoPorTipoItem()
        atributo.nombre = nombre
        atributo.tipo = tipo
        atributo.valorPorDefecto = valorPorDefecto
        atributo.idTipoItem = idTipoItem

        #aqui se utiliza el controlador para agregar el atributo
        r = control.agregarAtributoPorTipoItem(tipoItem,atributo)
        #print tipoItem.atributo
        if( r["estado"] == True ):
            flash("Se agrego la fase con exito")
        else:
            flash("Ocurrio un error : " + r["mensaje"])


    else :
        flash("Ocurrio un error, debe completar correctamente el formulario")

    return redirect(url_for('atributo',idTipoItem = idTipoItem))



@app.route("/tipoItem/atributos/modificar", methods=['GET','POST'])
def modificarAtributoTipoItem():
    '''Se encarga de modificar atributos de un tipo de item'''
    nombre = request.form['nombre']
    tipo = request.form['tipo']
    valorPorDefecto = request.form['valorPorDefecto']
    idAtributoPorTipoItem = request.form['idAtributosPorTipoItem']
    idTipoItem = request.form['idTipoItem']
    if(nombre and tipo and valorPorDefecto and idAtributoPorTipoItem and idTipoItem):
        #anga

        atributo = controladorAtributoPorTipoItem.getAtributoPorTipoItemById(idAtributoPorTipoItem)
        atributo.nombre = nombre
        atributo.tipo = tipo
        atributo.valorPorDefecto = valorPorDefecto


        r = controladorAtributoPorTipoItem.modificarAtributoPorTipoItem(atributo)
        if( r["estado"] == True ):
            flash("Se modifico la fase con exito")
        else:
            flash("Ocurrio un error : " + r["mensaje"])


    else :
        flash("Ocurrio un error, debe completar correctamente el formulario")

    return redirect(url_for('atributo',idTipoItem = idTipoItem))

@app.route("/tipoItem/atributos/eliminar")
@app.route("/tipoItem/atributos/eliminar/<idTipoItem>/<idAtributoPorTipoItem>")
def eliminarAtributoTipoItem(idTipoItem,idAtributoPorTipoItem):
    '''Se encarga de eliminar un atributo de un tipo de item'''
    print idTipoItem
    print idAtributoPorTipoItem

    if ( idTipoItem and idAtributoPorTipoItem):
        p = control.getTipoItemById(idTipoItem)
        atributoRemover = controladorAtributoPorTipoItem.getAtributoPorTipoItemById(idAtributoPorTipoItem)
        # aqui se usa el controlador del atributo por tipo item para eliminar
        r = control.quitarAtributoPorTipoItem(p, atributoRemover)
        # se elimina completamente el atributo
        p = controladorAtributoPorTipoItem.eliminarAtributoPorTipoItem(atributoRemover)
        if( r["estado"] == True ):
            flash("Se ha removido la fase con exito")
        else:
            flash("Ocurrio un error : " + r["mensaje"])
    else:
        flash("Ocurrio un error, intente de nuevo")

    return redirect(url_for('atributo', idTipoItem= idTipoItem))


@app.route("/tipoItem/return")
@app.route("/tipoItem/return/<idTipoItem>/<idProyecto>/<idFase>")
def returnTipoItem(idTipoItem,idProyecto,idFase):
    return redirect(url_for('indexTipoItem', idProyecto=idProyecto, idFase=idFase ))

# se agrego importar tipoItem entre fases
