#INDEX
import datetime
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlSolicitud
from app.controlador import ControlItem
from app.controlador import ControlRol
from app.controlador import ControlMensaje
from app.controlador import ControlProyecto
from app.controlador import ControlFase
from app.controlador import ControlUsuario
from app.modelo import SolicitudDeCambio
from app.modelo import Mensaje

from contextlib import closing

control = ControlSolicitud()
controlItem =  ControlItem()
controlRol = ControlRol()
controlFase = ControlFase()
controlProyecto = ControlProyecto()
controlMensaje = ControlMensaje()
controlUsuario = ControlUsuario()


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

def listaMiembros(idProyecto):
    
    miembros = controlRol.getMiembrosComite(idProyecto)
    
    return miembros

    

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
    listaFinal = listanueva
    solicitudes = control.getSolicitudes()

    for s in solicitudes :
        if (s.estado == 'pendiente' or s.estado == 'creado'):
            for item in listanueva :
                if( item.idItemActual == s.idItem):
                    listaFinal.remove(item)



    return listaFinal

@app.route('/solicitud')
@app.route('/solicitud/<idProyecto>/<idFase>')
def indexSolicitud(idProyecto, idFase):
    ''' Devuelve los datos de una sol en Concreto '''
    solicitudes = listadoSolicitudesByFase(idFase)
    #items = listadoItem();
    usuario = controlUsuario.getUsuarioById(session['idUsuario'])
    items = listadoItemFinal(idFase)
    miembros = listaMiembros(idProyecto)
    return render_template('indexSolicitud.html',usuario = usuario,  solicitudes = solicitudes, items =  items, idProyecto = idProyecto, idFase = idFase, miembros = miembros)


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
            detalleImpacto = controlItem.calcularImpacto(item) 
            solicitud.costo = detalleImpacto[1]
            solicitud.impacto = detalleImpacto[0]
            solicitud.idItem = item
            solicitud.accionSol = accionSol
            solicitud.cantidadVotos = 0
            solicitud.votoPositivo = 0
            solicitud.votoNegativo = 0
            solicitud.idUsuario = session['idUsuario']

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
        #Comprobar que hay miembros necesario
        if ( comprobarMiembros(idProyecto) == False ):
            flash("El comite de solicitud de cambio aun no se ha conformado" )
            return redirect(url_for('indexSolicitud', idProyecto = idProyecto, idFase = idFase))
        solicitud.estado = "pendiente"
        #Obtenemos los miembros
        miembros = controlRol.getMiembrosComite(idProyecto)
        print "Estos son los miembros:"
        print miembros
        solicitud.cantidadVotos = len(miembros)
        solicitud.votoPositivo = 0
        solicitud.votoNegativo = 0

        r = control.modificarSolicitud(solicitud)
        if( r["estado"] == True ):
            enviarMensajeMiembros(miembros,solicitud)
            flash("Solicitud Enviada")
        else:
            flash("Ocurrio un error : " + r["mensaje"])


    return redirect(url_for('indexSolicitud', idProyecto = idProyecto, idFase = idFase))

def enviarMensajeMiembros(miembros, solicitud):
    '''Se encarga de enviar los mensajes al comite'''
    item = controlItem.getItemById(solicitud.idItem)
    fase = controlFase.getFaseById(item.idFase)
    proyecto = controlProyecto.getProyectoById(fase.idProyecto)
    
    
    #[complejidad,costo,listadoItem]
    for m in miembros:

        mensaje = Mensaje()
        mensaje.titulo = "Solicitud de Cambio Item: " + item.nombreItemActual
        mensaje.cuerpo = "Se ha creado una solicitud de cambio para " + solicitud.accionSol
        mensaje.cuerpo += "el item : " + item.nombreItemActual
        mensaje.cuerpo += ".El mismo se encuentra en el proyecto " + proyecto.nombre
        mensaje.cuerpo += ", de la fase " + fase.nombre
        mensaje.cuerpo += "<br/> Se ruega votar en la brevedad posible. Para votar haga click en"
        mensaje.cuerpo += "<br/><a href='" + url_for('votarSolicitud') + "/" + str(solicitud.idSolicitud)
        mensaje.cuerpo += "' class='btn' >Votar</a>"
        mensaje.fecha = str(datetime.date.today())
        mensaje.idUsuario = m.idUsuario
        mensaje.estado = "no leido"

        r = controlMensaje.nuevoMensaje(mensaje)
        if (r["estado"] == False):
            print "Explotooooo!! Mensaje"
            print r["mensaje"]

@app.route('/solicitud/votar')
@app.route('/solicitud/votar/<idSolicitud>')
def votarSolicitud(idSolicitud = None):
    solicitud = control.getSolicitudById(idSolicitud)
    usuario = controlUsuario.getUsuarioById(solicitud.idUsuario)
    detalleImpacto = controlItem.calcularImpacto(solicitud.idItem)
    listadoItem = detalleImpacto[2]
    votantesStr = []
    if (solicitud.votantes):
        votantesStr = solicitud.votantes.split(",")
    votantes = []
    for vstr in votantesStr :
        if (vstr != ''):
            votantes.append(int(vstr))
    return render_template('votarSolicitud.html', solicitud = solicitud, votantes = votantes, usuario = usuario, listadoItem = listadoItem)


@app.route('/solicitud/votarPositivo')
@app.route('/solicitud/votarPositivo/<idSolicitud>')
def votarPositivo(idSolicitud = None):
    solicitud = control.getSolicitudById(idSolicitud)
    usuario = controlUsuario.getUsuarioById(session['idUsuario'])

    votantesStr = []
    if (solicitud.votantes):
        votantesStr = solicitud.votantes.split(",")
    votantes = []
    for vstr in votantesStr :
        if (vstr != ''):
            votantes.append(int(vstr))
    solicitud.votoPositivo = solicitud.votoPositivo + 1
    votantes.append(usuario.idUsuario)
    lista = ""
    for v in votantes:
        lista += str(v) + ","

    solicitud.votantes = lista
    #Se debe comprobar la mayoria
    #Aca supuestamente
    r = control.modificarSolicitud(solicitud)
    if( r["estado"] == True ):
        flash("Su voto ha sido computado")
        if ( verificarVotos(solicitud) != 0 ):
            procesarSolicitud(solicitud)
    else:
        flash("Ocurrio un error : " + r["mensaje"])
    return redirect( url_for('votarSolicitud', idSolicitud = idSolicitud) )

@app.route('/solicitud/votarNegativo')
@app.route('/solicitud/votarNegativo/<idSolicitud>')
def votarNegativo(idSolicitud = None):
    solicitud = control.getSolicitudById(idSolicitud)
    usuario = controlUsuario.getUsuarioById(session['idUsuario'])

    votantesStr = []
    if (solicitud.votantes):
        votantesStr = solicitud.votantes.split(",")
    votantes = []
    for vstr in votantesStr :
        if (vstr != ''):
            votantes.append(int(vstr))
    solicitud.votoNegativo = solicitud.votoNegativo + 1
    votantes.append(usuario.idUsuario)
    lista = ""
    for v in votantes:
        lista += str(v) + ","

    solicitud.votantes = lista
    #Se debe comprobar la mayoria
    #Aca supuestamente
    r = control.modificarSolicitud(solicitud)
    if( r["estado"] == True ):
        flash("Su voto ha sido computado")
        if ( verificarVotos(solicitud) != 0 ):
            procesarSolicitud(solicitud)
    else:
        flash("Ocurrio un error : " + r["mensaje"])
    return redirect( url_for('votarSolicitud', idSolicitud = idSolicitud) )

def listadoUsuariosPorRoles(idProyecto):
    retorno = []
    pro =  controlProyecto.getProyectoById(idProyecto)
    lista = controlRol.getRolPorProyecto(idProyecto)

    for rol in lista:
        if (rol.nombre == "MiembroComite "+pro.nombre):
            usuarios = controlUsuario.getUsuariosByRol(rol)
            print usuarios
            for usuario in usuarios :
                if(not (usuario in retorno) ):
                    retorno.append(usuario)
    return retorno

def comprobarMiembros(idProyecto):
    '''Comprueba que el numero de miembros sea impar'''
    lista = listadoUsuariosPorRoles(idProyecto)
    #Numero par
    if ( len(lista) % 2 == 0 ):
        return False
    else:
        return True

def verificarVotos(solicitud):
    ''' Realiza el conteo de votos'''
    #Gana la aprobacion
    if (solicitud.cantidadVotos / 2 == solicitud.votoPositivo - 1  ):
        print "Se aprueba"
        return 1
    #Se rechaza
    if (solicitud.cantidadVotos / 2 == solicitud.votoNegativo - 1 ):
        print "Se rechaza"
        return -1

    return 0

def procesarSolicitud(solicitud):
    #Se aprueba
    if (verificarVotos(solicitud) == 1 ):
        #Realizamos las operaciones para habilitar la modificacion
        # El item solicitado pasa a revision y su red (antecesores sucesores)
        # Los otros item en la misma LB de final a aprobado
        # La LB pasa a un estado NO VALIDO
        # Las LB de su Red pasan a NO VALIDO
        solicitud.estado = "aceptada"
        control.modificarSolicitud(solicitud)
        controlItem.pasarRevision(solicitud.idItem,solicitud.idItem, 0 )

    if (verificarVotos(solicitud) == -1 ):
        solicitud.estado = "rechazado"
        control.modificarSolicitud(solicitud)