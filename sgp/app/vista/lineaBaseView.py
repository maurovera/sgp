# -*- coding: utf-8 -*-
#INDEX
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlLineaBase
from app.controlador import ControlItem
from app.modelo import LineaBase
from contextlib import closing

control = ControlLineaBase()
controlItem = ControlItem()

def listadoItemAprobado(idFase):
    lista = controlItem.getItemAprobadoByFase(idFase)
    return lista

def busquedaPorId(idLB):
    ''' Devuelve un listado de las LB que coincidan con un ID '''
    lista = None
    r = True
    print "-- " + idLB
    if(r):
        lista = control.buscarPorIdLB(idLB)
    else:
        flash("Error. Lista no devuelta")
    print lista
    return lista

def listadoLineaBase(idFase):
    ''' Devuelve un listado de las lineas base '''
    lista = None
    r = True
    if(r):
        lista = control.getLBByFase(idFase)
    else:
        flash("Error. Lista no devuelta")
    return lista


@app.route('/lineaBase')
@app.route('/lineaBase/<idProyecto>/<idFase>')
def indexLineaBase(idProyecto= None, idFase=None):
    ''' Devuelve los datos de una LB en Concreto '''
    lineaBases = listadoLineaBase(idFase);
    listaItem = listadoItemAprobado(idFase);
    print idProyecto
    print idFase
    print "listaItem"
    print listaItem
    return render_template('indexLineaBase.html', lineaBases = lineaBases, idProyecto=idProyecto, idFase=idFase, listaItem = listaItem)


@app.route('/lineaBase/eliminar')
@app.route('/lineaBase/eliminar/<id>/<idProyecto>/<idFase>')
def eliminarLineaBase(id=None, idFase=None, idProyecto = None):
    if(id):
        lineaBase = control.getLineaBaseById(id)

        if(lineaBase):

            r= control.eliminarLineaBase(lineaBase)
            if(r["estado"] == True):
                flash("Se elimino con exito la Linea Base con ID: ")
            else:
                flash("Ocurrio un error: "+ r["mensaje"])
        else :
            flash("Ocurrio un error durante la eliminacion")

    return redirect(url_for('indexLineaBase', idProyecto = idProyecto, idFase=idFase))

@app.route('/lineaBase/abrir')
@app.route('/lineaBase/abrir/<id>/<idProyecto>/<idFase>')
def abrirLineaBase(id=None, idFase=None, idProyecto = None):
    return redirect(url_for('indexLineaBase', idProyecto = idProyecto, idFase=idFase))


@app.route('/lineaBase/nuevo')
@app.route('/lineaBase/nuevo/<idProyecto>/<idFase>', methods=['GET','POST'])
def nuevaLB(idFase=None, idProyecto = None):
    ''' Crea una nueva linea base '''
    #Si recibimos algo por post



    if request.method == 'POST' :


        print "LO QUE SE RECIBE POR POST EN LB"
        print request.form['numero']
        print request.form.getlist('item')
        print "------fin lb post---------"
        #idLB= request.form['idLB']
        numero = request.form['numero']
        idFase = idFase
        listaItem = request.form.getlist('item')
        print "Estoy aca adentro del form :D CAGADA DE PATO..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente
        #con un metodo kachiai
        if(numero and idFase and listaItem):
            lineaBase = LineaBase()
            #falta auto incremento de numero de linea base por fase
            lineaBase.numero = numero
            lineaBase.estado = 0
            lineaBase.idFase = idFase

            r = control.nuevaLineaBase(lineaBase)

            if(r["estado"] == True):
                r1 = control.agregarItemLB(lineaBase,listaItem)
                if(r1["estado"] == True ):
                    flash("Exito, se creo una nueva LB")
                else:
                   flash("Ocurrio un error : " + r1["mensaje"])
            else :
                flash("Ocurrio un error : " + r["mensaje"])

    return redirect(url_for('indexLineaBase',idProyecto = idProyecto, idFase=idFase))

@app.route('/lineaBase/modificar')
@app.route('/lineaBase/modificar/<idProyecto>/<idFase>', methods=['GET','POST'])
def modificarLB(idFase=None, idProyecto=None):
    ''' Modifica una LB '''



    if request.method == 'POST' :

        print request.form['idLB']
        print request.form['numero']
        print request.form['estado']

        idLB= request.form['idLB']
        numero = request.form['numero']
        estado = request.form['estado']

        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente
        #con un metodo kachiai
        if(idLB and numero and estado):
            lineaBase = control.getLineaBaseById(idLB)
            if (lineaBase):
                lineaBase.idLB = idLB
                lineaBase.numero = numero
                lineaBase.estado = estado

                r = control.modificarLineaBase(lineaBase)
                if( r["estado"] == True ):
                    flash(u"Modficado con exito")
                else:
                    flash(u"Ocurrio un error : " + r["mensaje"])


    return redirect(url_for('indexLineaBase', idProyecto=idProyecto, idFase=idFase))

@app.route("/lineaBase/buscar")
@app.route("/lineaBase/buscar/<idBuscado>")
def buscarLB(idBuscado):
    ''' Devuelve una lista de LB que coincidan con el ID proporcionado '''
    print "Helloooooowww   " + idBuscado
    lineasBase = busquedaPorId(idBuscado);
    return render_template('indexLineaBase.html', lineaBases = lineasBase)