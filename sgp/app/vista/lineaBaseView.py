# -*- coding: utf-8 -*-
#INDEX
import datetime
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlLineaBase
from app.controlador import ControlItem
from app.controlador import ControlDatosItem
from app.controlador import ControlFase
from app.controlador import ControlProyecto
from app.controlador import ControlHistorialLineaBase
from app.controlador import ControlHistorialItems
from app.modelo import HistorialLineaBase
from app.modelo import LineaBase
from app.modelo import HistorialItems
from contextlib import closing

control = ControlLineaBase()
controlItem = ControlItem()
controlDatos = ControlDatosItem()
controlFase = ControlFase()
controlProyecto =  ControlProyecto()
controlHistorial = ControlHistorialLineaBase()
controlHistorialItems = ControlHistorialItems()

def listadoItem(idFase):
    ''' Devuelve un listado de los tipo item '''
    lista = None
    r = True
    if(r):
        lista = controlItem.getItemByFase(idFase)
    else:
        flash("Error. Lista no devuelta")
    return lista


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

def listadoDeEstados():
    ''' Devuelve un listado de las lineas base '''
    listaN = []
    #lista = control.getLBByFase(idFase)
    listaN.append({"numero" : 0, "estado" :  "creado"})
    listaN.append({"numero" : 1, "estado" :  "liberado"})
    listaN.append({"numero" : -1, "estado" :  "no valido"})    
    return listaN



@app.route('/lineaBase')
@app.route('/lineaBase/<idProyecto>/<idFase>')
def indexLineaBase(idProyecto= None, idFase=None):
    ''' Devuelve los datos de una LB en Concreto '''
    lineaBases = listadoLineaBase(idFase);
    listaItem = listadoItemAprobado(idFase);
    listaEstado = listadoDeEstados();
    
    estadoDeLaFase(idFase, idProyecto)
    
    vacio = False
    if len(listaItem) == 0:
        vacio = True
    
        
    print idProyecto
    print idFase
    print "listaItem"
    print listaItem
    return render_template('indexLineaBase.html',vacio = vacio, lineaBases = lineaBases, idProyecto=idProyecto, idFase=idFase, listaItem = listaItem, listaEstado = listaEstado)


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
@app.route('/lineaBase/abrir/<id>/<idProyecto>/<idFase>/<idUsuario>')
def abrirLineaBase(id=None, idFase=None, idProyecto = None, idUsuario = None):
    ''' pasa todo los estados de los items a estado aprobado menos los que estan en revision '''
    lb = control.getLineaBaseById(id)
    #pasa a un estado liberado estado igual a 1
    lb.estado = 1
    control.modificarLineaBase(lb)
    
    # se pasa todo los items en estado final a aprobado
    lista = lb.items
    paHistorial = ""
    for d in lista:
        dato = controlItem.getDatoActualByIdItemActual(d.idItemActual)
        itA = controlItem.getItemById(d.idItemActual)
        paHistorial = paHistorial + " " + itA.nombreItemActual + "," 
        if dato.estado != "revision":
            dato.estado = "aprobado"
            # aca guau le dessigno de esta mierda
            dato.itemLB.remove(lb)
            controlDatos.modificarDatosItem(dato)
            
            
            # parte del historial items
            
            historialN = HistorialItems()
            historialN.idUsuario = idUsuario
            historialN.tipoModificacion = "estado de item a aprobado"
            historialN.fechaModificacion = str(datetime.date.today())
            historialN.idItem = d.idItemActual
            controlHistorialItems.nuevoHistorialItems(historialN)
            #---------------------------------------------------------------
    
    # parte del historial de lb
    historial = HistorialLineaBase()
    historial.tipoOperacion = "linea base liberado: " + paHistorial
    historial.fechaModificacion = str(datetime.date.today())
    historial.idLB = lb.idLB
    historial.idUsuario = idUsuario
    controlHistorial.nuevoHistorialLineaBase(historial)
    # ----------------------------------------------------------
    
    
    
    flash("Se abrio con exito la Linea Base ")
    # CORROBORAMOS QUE TENGA ALMENOS UNA LB
    estadoDeLaFaseAlEliminar(idFase, idProyecto)                
       
    # pregunta es necesario desligar a todo los items de la lb base liberada
        
    
    
    
    return redirect(url_for('indexLineaBase', idProyecto = idProyecto, idFase=idFase))


@app.route('/lineaBase/cerrar')
@app.route('/lineaBase/cerrar/<id>/<idProyecto>/<idFase>/<idUsuario>')
def cerrarLineaBase(id=None, idFase=None, idProyecto = None, idUsuario = None):
    ''' pasa todo los estados de los items a estado aprobado menos los que estan en revision '''
    lb = control.getLineaBaseById(id)
    #pasa a un estado cerrado estado igual a 0
    lb.estado = 0
    control.modificarLineaBase(lb)
    
    # se pasa todo los items en estado final a aprobado
    lista = lb.items
    paHistorial = ""
    for d in lista:
        dato = controlItem.getDatoActualByIdItemActual(d.idItemActual)
        itA = controlItem.getItemById(d.idItemActual)
        paHistorial = paHistorial + " " + itA.nombreItemActual + "," 
        #if dato.estado != "revision":
        dato.estado = "final"
        # aca guau le dessigno de esta mierda
        dato.itemLB.remove(lb)
        controlDatos.modificarDatosItem(dato)
            
            
        # parte del historial items
            
        historialN = HistorialItems()
        historialN.idUsuario = idUsuario
        historialN.tipoModificacion = "estado de item a final"
        historialN.fechaModificacion = str(datetime.date.today())
        historialN.idItem = d.idItemActual
        controlHistorialItems.nuevoHistorialItems(historialN)
            #---------------------------------------------------------------
    
    # parte del historial de lb
    historial = HistorialLineaBase()
    historial.tipoOperacion = "linea base cerrada: " + paHistorial
    historial.fechaModificacion = str(datetime.date.today())
    historial.idLB = lb.idLB
    historial.idUsuario = idUsuario
    controlHistorial.nuevoHistorialLineaBase(historial)
    # ----------------------------------------------------------
    
    
    
    flash("Se cerro con exito la Linea Base ")
    # CORROBORAMOS QUE TENGA ALMENOS UNA LB
    estadoDeLaFaseAlEliminar(idFase, idProyecto)                
       
    # pregunta es necesario desligar a todo los items de la lb base liberada
        
    
    
    
    return redirect(url_for('indexLineaBase', idProyecto = idProyecto, idFase=idFase))


@app.route('/lineaBase/nuevo')
@app.route('/lineaBase/nuevo/<idProyecto>/<idFase>', methods=['GET','POST'])
def nuevaLB(idFase=None, idProyecto = None):
    ''' Crea una nueva linea base '''
    #Si recibimos algo por post



    if request.method == 'POST' :

        idUsuario = request.form['idUsuario']
        print "LO QUE SE RECIBE POR POST EN LB"
        #print request.form['numero']
        print request.form.getlist('item')
        print "------fin lb post---------"
        #idLB= request.form['idLB']
        #numero = request.form['numero']
        idFase = idFase
        listaItem = request.form.getlist('item')
        print "Estoy aca adentro del form :D CAGADA DE PATO..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente
        #con un metodo kachiai
        if(idFase and listaItem):
            lineaBase = LineaBase()
            #falta auto incremento de numero de linea base por fase
            nu = listadoLineaBase(idFase)
            lineaBase.numero = len( list(nu) ) + 1
            lineaBase.estado = 0
            lineaBase.idFase = idFase

            r = control.nuevaLineaBase(lineaBase)
            
            # parte del historial de lb
            paHistorial = ""
            for i in listaItem:
                it = controlItem.getItemById(i)
                paHistorial = paHistorial + it.nombreItemActual + ", "
                
            historial = HistorialLineaBase()
            historial.tipoOperacion = "linea base creada y cerrada: "+ paHistorial
            historial.fechaModificacion = str(datetime.date.today())
            historial.idLB = lineaBase.idLB
            historial.idUsuario = idUsuario
            controlHistorial.nuevoHistorialLineaBase(historial)
            # ----------------------------------------------------------

            if(r["estado"] == True):
                r1 = control.agregarItemLB(lineaBase,listaItem, idUsuario)
                if(r1["estado"] == True ):
                    estadoDeLaFase(idFase, idProyecto)
                    
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


@app.route('/lineaBase/mostrarItem')
@app.route('/lineaBase/mostrarItem/<idLB>/<idProyecto>/<idFase>')
def mostrarItemDeLB(idLB, idProyecto = None, idFase = None):
    lb = control.getLineaBaseById(idLB)
    lista  = lb.items
    print "esto son los datos del item:"
    listaN = []
    for d in lista:
        
        item = controlItem.getItemById(d.idItemActual)
        print "nombre del item : "
        print item.nombreItemActual
        dato = controlItem.getDatoActualByIdItemActual(d.idItemActual)
        print "estado del item"
        print dato.estado
        listaN.append({"nombre": item.nombreItemActual,"dato" :  dato.estado })
        
    print "lista nueva"
    for i in listaN:
        print i["nombre"]
    
    print "fin de listado"
    
    print "Esta es la lista de estado"
    listaEstado = listadoDeEstados();
    for i in listaEstado:
        print i["estado"]
        
    
    return redirect(url_for('indexLineaBase', idProyecto = idProyecto, idFase=idFase))    



def corroborarSiTieneLB(idFase):
    ''' corroborar si tiene una linea base '''
    valor = False
    listaLB = listadoLineaBase(idFase);
    
    for l in listaLB:
        #si la linea base no esta liberada
        if l.estado != 1:
            valor = True
    
    return valor    



# se agrego importar tipoItem entre fases
def corroborarFaseFinal(idFase):
    valor = False
    listaItem = listadoItem(idFase);
    
    for i in listaItem:
        if i.eliminado == False:
            if( not controlItem.comprobarItemEstadofinal(i) ):
                valor = True
              
    return valor    
    
    
def corroborarSiTieneItem(idFase):
    valor = False
    listaDeItem = listadoItem(idFase);
    for i in listaDeItem:
        if i.eliminado == False: 
                valor = True
    
    return valor
#def corroborarFasAntFinal(idFase, idProyecto):
#    valor = False
#    pro = controlProyecto.getProyectoById(idProyecto)
#    faseActual =  controlFase.getFaseById(idFase)
#    if faseActual.numeroFase == 1:
#        valor = False
#    if faseActual.numeroFase > 1:
#        for f in pro.fases:
            # si la fase que queres es diferente
#            if(f.numeroFase == faseActual.numeroFase - 1): 
                # y si al menos hay alguna fase que no es final
#                if(f.estado != 'final'):
#                   valor = True
            
#   return valor



def estadoDeLaFaseAlEliminar(idFase, idProyecto):
    faseActual = controlFase.getFaseById(idFase)
    proyecto = controlProyecto.getProyectoById(idProyecto)
    # aca se controla si todos son finales y la anterior es final
    if not corroborarFaseFinal(idFase):
        for f in proyecto.fases:
            if(faseActual.numeroFase > 1 ):
                if f.numeroFase == faseActual.numeroFase - 1:
                    if f.estado == 'final':
                        faseActual.estado = 'final'
                        controlFase.modificarFase(faseActual)
            elif faseActual.numeroFase == 1:
                faseActual.estado = 'final'
                controlFase.modificarFase(faseActual)
                
    
    
    elif corroborarSiTieneLB(idFase):
        faseActual.estado = "en linea base"
        controlFase.modificarFase(faseActual)
    elif corroborarSiTieneItem(idFase):
        faseActual.estado = "desarrollo"
        controlFase.modificarFase(faseActual)
    else: 
        faseActual.estado = "no iniciado"
        controlFase.modificarFase(faseActual)   
            
     
    # aqui cambia los estados de las fases sgtes si es necesario
    if faseActual.estado != 'final':
        for f in proyecto.fases:
            if f.numeroFase > faseActual.numeroFase:
                fase = controlFase.getFaseById(f.idFase)
                if corroborarSiTieneLB(f.idFase):
                    fase.estado = "en linea base"
                    controlFase.modificarFase(fase)
                else:
                    fase.estado = "desarrollo"
                    controlFase.modificarFase(fase)


def estadoDeLaFase(idFase, idProyecto):
    faseActual = controlFase.getFaseById(idFase)
    proyecto = controlProyecto.getProyectoById(idProyecto)
    # aca se controla si todos son finales y la anterior es final
    if not corroborarFaseFinal(idFase):
        for f in proyecto.fases:
            if(faseActual.numeroFase > 1 ):
                if f.numeroFase == faseActual.numeroFase - 1:
                    if f.estado == 'final':
                        faseActual.estado = 'final'
                        controlFase.modificarFase(faseActual)
                        cambiarAdelanteSiFinal(idFase, idProyecto)
            elif faseActual.numeroFase == 1:
                faseActual.estado = 'final'
                controlFase.modificarFase(faseActual)
                cambiarAdelanteSiFinal(idFase, idProyecto)
                
                     
                
    elif corroborarSiTieneLB(idFase):
        faseActual.estado = "en linea base"
        controlFase.modificarFase(faseActual)
    elif corroborarSiTieneItem(idFase):
        faseActual.estado = "desarrollo"
        controlFase.modificarFase(faseActual)
    else: 
        faseActual.estado = "no iniciado"
        controlFase.modificarFase(faseActual)   
            
 
def cambiarAdelanteSiFinal(idFase, idProyecto):
    faseActual = controlFase.getFaseById(idFase)
    pro = controlProyecto.getProyectoById(idProyecto) 
    if faseActual.estado == 'final':
        for f in pro.fases:
            if f.numeroFase > faseActual.numeroFase:
                fase = controlFase.getFaseById(f.idFase)
                if  not corroborarFaseFinal(idFase): 
                    fase.estado = "final"
                    controlFase.modificarFase(fase)
                elif corroborarSiTieneLB(f.idFase):
                    fase.estado = "en linea base"
                    controlFase.modificarFase(fase)
                else:
                    fase.estado = "desarrollo"
                    controlFase.modificarFase(fase)
    
 
 
     
    # aqui cambia los estados de las fases sgtes si es necesario
#     if faseActual.estado != 'final':
#         for f in proyecto.fases:
#             if f.numeroFase > faseActual.numeroFase:
#                 fase = controlFase.getFaseById(f.idFase)
#                 if corroborarSiTieneLB(f.idFase):
#                     fase.estado = "en linea base"
#                     controlFase.modificarFase(fase)
#                 else:
#                     fase.estado = "desarrollo"
#                     controlFase.modificarFase(fase)

@app.route('/lineaBase/listado')
@app.route('/lineaBase/listado/<id>/<idProyecto>/<idFase>')
def listaItemLB(id = None, idProyecto= None, idFase=None):
    lineaBase = control.getLineaBaseById(id)
    
    datos  = lineaBase.items
    print "esto son los datos del item:"
    items = []
    for d in datos:
        item = controlItem.getItemById(d.idItemActual)
        datoItem = controlItem.getDatoActualByIdItemActual(d.idItemActual)
        #items.append(item)
        items.append({"nombre": item.nombreItemActual,
                      "eliminado": item.eliminado,
                      "version": item.ultimaVersion,
                      "prioridad" :  datoItem.prioridad })
        
        
    return render_template('listaItemLB.html', lineaBase = lineaBase, idProyecto=idProyecto, idFase=idFase, items = items)
