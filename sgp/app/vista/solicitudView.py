#INDEX
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlSolicitud
from app.modelo import SolicitudDeCambio
from contextlib import closing

control = ControlSolicitud()



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



@app.route('/solicitud')
def indexSolicitud():
    ''' Devuelve los datos de una sol en Concreto '''
    solicitudes = listadoSolicitudes();
    return render_template('indexSolicitud.html', solicitudes = solicitudes)


@app.route('/solicitud/eliminar')
@app.route('/solicitud/eliminar/<idSolicitud>')
def eliminarSolicitud(idSolicitud=None):
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
    
    return redirect(url_for('indexSolicitud'))

         


@app.route('/solicitud/nuevo', methods=['GET','POST'])
def nuevaSolicitud():
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
        estado1 = request.form['estado']
        #Descripcion = request.form['descripcion']
        #Estado = request.form['estado']
          
        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente 
        #con un metodo kachiai
        if(nombreSolicitud and descripcion1 and estado1):
            solicitud = SolicitudDeCambio()
            #solicitud.idSolicitud = idSolicitud
            solicitud.nombreSolicitud = nombreSolicitud
            solicitud.descripcion = descripcion1
            solicitud.estado = estado1
            
            r = control.nuevaSolicitud(solicitud)
            if(r["estado"] == True):
                flash("Exito, se creo un nuevo usuario")    
            else :
                flash("Ocurrio un error : " + r["mensaje"])
                    
    return redirect(url_for('indexSolicitud'))


@app.route('/solicitud/modificar', methods=['GET','POST'])
def modificarSolicitud():
    ''' Modifica una sol '''
    
    
    
    if request.method == 'POST' :
        
        print request.form['idSolicitud']
        print request.form['nombreSolicitud']
        print request.form['descripcion']
        print request.form['estado']
        
        idSolicitud = request.form['idSolicitud']
        nombreSolicitud = request.form['nombreSolicitud']
        Descripcion = request.form['descripcion']
        Estado = request.form['estado']
        
        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente 
        #con un metodo kachiai
        if(idSolicitud and nombreSolicitud and Descripcion and Estado):
            solicitud = control.getSolicitudById(idSolicitud)
            if (solicitud):
                
                solicitud.idSolicitud = idSolicitud
                solicitud.nombreSolicitud = nombreSolicitud
                solicitud.descripcion = Descripcion
                solicitud.estado = Estado
                    
                r = control.modificarSolicitud(solicitud)
                if( r["estado"] == True ):
                    flash("Modficado con exito")
                else:
                    flash("Ocurrio un error : " + r["mensaje"])
                       
        
    return redirect(url_for('indexSolicitud'))

@app.route("/solicitud/buscar")
@app.route("/solicitud/buscar/<nombrebuscado>")
def buscarSolicitud(nombrebuscado):
    ''' Devuelve una lista de solicitudes que coincidan con el nombre proporcionado '''
    print "Helloooooowww"
    solicitudes = busquedaPorNombre(nombrebuscado);
    return render_template('indexSolicitud.html', solicitudes = solicitudes)
