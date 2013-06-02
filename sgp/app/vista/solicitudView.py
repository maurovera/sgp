#INDEX
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlSolicitud
from app.controlador import ControlItem
from app.modelo import SolicitudDeCambio

from contextlib import closing

control = ControlSolicitud()
controlItem =  ControlItem()


def busquedaPorNombre(nombre):
    ''' Devuelve un listado de los nombreSolicitud que coincidan con un nombre '''
    lista = None
    r = True
    if(r):
        lista = control.buscarPorNombre(nombre)
    else:
        flash("Error. Lista no devuelta")
    print lista
    return lista



def listadoSolicitudes():
    ''' Devuelve un listado de las sol '''
    lista = None
    r = True
    if(r):
        lista = control.getSolicitudes()
    else:
        flash("Error. Lista no devuelta")
    return lista

def listadoSolicitudesByFase(idFase):
    ''' Devuelve un listado de las sol '''
   
    lista =  controlItem.getItemByFase(idFase)
    listaSol = control.getSolicitudes()
    listaNueva = []
    for i in lista:
        for ls in listaSol:
            if i.idItemActual == ls.idItem:
                listaNueva.append(ls)
    
            
    return listaNueva



def listadoItem():
    ''' Devuelve un listado de los tipo item '''
    lista = None
    r = True
    if(r):
        lista = controlItem.getItemFinal()
    else:
        flash("Error. Lista no devuelta")
    return lista

def listadoItemFinal(idFase):
    ''' Devuelve un listado de los tipo item '''
    lista = None
    listanueva = []
    lista = controlItem.getItemByFase(idFase)
    for i in lista:
        if(controlItem.comprobarItemEstadofinal(i)):
            listanueva.append(i)
        
    return listanueva

@app.route('/solicitud')
@app.route('/solicitud/<idProyecto>/<idFase>')
def indexSolicitud(idProyecto, idFase):
    ''' Devuelve los datos de una sol en Concreto '''
    solicitudes = listadoSolicitudesByFase(idFase)
    #items = listadoItem();
    items = listadoItemFinal(idFase)
    return render_template('indexSolicitud.html', solicitudes = solicitudes, items =  items, idProyecto = idProyecto, idFase = idFase)


@app.route('/solicitud/eliminar')
@app.route('/solicitud/eliminar/<idProyecto>/<idFase>/<idSolicitud>')
def eliminarSolicitud(idProyecto, idFase, idSolicitud=None):
    if(idSolicitud):
        solicitud = control.getSolicitudById(idSolicitud)
    
        if(solicitud):
            
            r= control.eliminarSolicitud(solicitud)
            if(r["estado"] == True):
                flash("Se elimino con exito la solicitud: " + solicitud.nombreSolicitud)
            else:
                flash("Ocurrio un error: "+ r["mensaje"])
        else :
            flash("Ocurrio un error durante la eliminacion")
    
    return redirect(url_for('indexSolicitud', idProyecto=idProyecto, idFase=idFase))

         

@app.route('/solicitud/nuevo')
@app.route('/solicitud/nuevo/<idProyecto>/<idFase>', methods=['GET','POST'])
def nuevaSolicitud(idProyecto, idFase):
    ''' Crea una nueva sol '''
    #Si recibimos algo por post
    
    
    print "entre aca "
    if request.method == 'POST' :
        print "entre aca  en el if post"
        #print request.form['idSolicitud']
        print request.form['nombreSolicitud']
        
        print "nooooooooooooooooooooooooo"
        
#     idSolicitud = db.Column(db.Integer, primary_key = True)
#     nombreSolicitud = db.Column( db.String(45), index = True, nullable = False)
#     Descripcion = db.Column( db.String(160) , nullable = False)
#     Estado = db.Column( db.String(45) )
#     costo = db.Column( db.Integer )
#     impacto = db.Column( db.Integer )
#     idItem = db.Column(db.Integer, db.ForeignKey('item.idItemActual'))
          
        
        #idSolicitud = request.form['idSolicitud']
        nombreSolicitud = request.form['nombreSolicitud']
        descripcion1 = request.form['descripcion']
        #estado1 = request.form['estado']
        item  =  request.form['idItem']
        #Descripcion = request.form['descripcion']
        #Estado = request.form['estado']
        accionSol = request.form['accionSol']
        print accionSol + "jajajjaajja esta es una accion carajo"  
        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente 
        #con un metodo kachiai
        if(nombreSolicitud and descripcion1):
            solicitud = SolicitudDeCambio()
            #solicitud.idSolicitud = idSolicitud
            solicitud.nombreSolicitud = nombreSolicitud
            solicitud.descripcion = descripcion1
            solicitud.estado = "creado"
            solicitud.costo = 0
            solicitud.impacto = 0
            solicitud.idItem = item
            solicitud.accionSol = accionSol
            
            r = control.nuevaSolicitud(solicitud)
            if(r["estado"] == True):
                flash("Exito, se creo un nuevo usuario")    
            else :
                flash("Ocurrio un error : " + r["mensaje"])
                    
    return redirect(url_for('indexSolicitud', idProyecto= idProyecto, idFase = idFase))


@app.route('/solicitud/modificar')
@app.route('/solicitud/modificar/<idProyecto>/<idFase>', methods=['GET','POST'])
def modificarSolicitud(idProyecto, idFase):
    ''' Modifica una sol '''
    
    
    
    if request.method == 'POST' :
        
        print request.form['idSolicitud']
        print request.form['nombreSolicitud']
        print request.form['descripcion']
        #print request.form['estado']
        
        idSolicitud = request.form['idSolicitud']
        nombreSolicitud = request.form['nombreSolicitud']
        Descripcion = request.form['descripcion']
        #Estado = request.form['estado']
        
        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente 
        #con un metodo kachiai
        if(idSolicitud and nombreSolicitud and Descripcion ):
            solicitud = control.getSolicitudById(idSolicitud)
            if (solicitud):
                
                solicitud.idSolicitud = idSolicitud
                solicitud.nombreSolicitud = nombreSolicitud
                solicitud.descripcion = Descripcion
                #solicitud.estado = Estado
                    
                r = control.modificarSolicitud(solicitud)
                if( r["estado"] == True ):
                    flash("Modficado con exito")
                else:
                    flash("Ocurrio un error : " + r["mensaje"])
                       
        
    return redirect(url_for('indexSolicitud', idProyecto = idProyecto, idFase = idFase))

@app.route("/solicitud/buscar")
@app.route("/solicitud/buscar/<idProyecto>/<idFase>/<nombrebuscado>")
def buscarSolicitud(idProyecto, idFase,nombrebuscado ):
    ''' Devuelve una lista de solicitudes que coincidan con el nombre proporcionado '''
    print "Helloooooowww"
    solicitudes = busquedaPorNombre(nombrebuscado);
    return render_template('indexSolicitud.html', solicitudes = solicitudes)


@app.route('/solicitud/enviarSol')
@app.route('/solicitud/enviarSol/<idProyecto>/<idFase>/<idSolicitud>')
def enviarSol(idProyecto, idFase, idSolicitud):
    print "este es el id de solicitud"
    print idSolicitud
    solicitud = control.getSolicitudById(idSolicitud)
    if(solicitud):
        solicitud.estado = "pendiente"
        r = control.modificarSolicitud(solicitud)
        if( r["estado"] == True ):
            flash("Solicitud Enviada")
        else:
            flash("Ocurrio un error : " + r["mensaje"])
        

    return redirect(url_for('indexSolicitud', idProyecto = idProyecto, idFase = idFase))
