#INDEX
from xhtml2pdf import pisa
from StringIO import StringIO
import datetime
from flask import render_template, flash, redirect, request, session, g, url_for, abort, Response
from app import app
from app.controlador import ControlProyecto
from app.modelo import Proyecto
from app.modelo import Fase
from app.modelo import Rol

from app.controlador import ControlFase
from app.controlador import ControlTipoItem
from app.controlador import ControlRelacion
from app.controlador import ControlItem
from app.controlador import ControlRol
from app.controlador import ControlUsuario
from app.controlador import ControlSolicitud
from app.controlador import ControlLineaBase
from app.modelo import Usuario
from contextlib import closing

controlador = ControlProyecto()
controlFase = ControlFase()
controlTipoIndex =  ControlTipoItem()
controlRelacion = ControlRelacion()
controlItem = ControlItem()
controlRol = ControlRol()
controlUsuario = ControlUsuario()
controlSolicitud = ControlSolicitud()
controlLineaBase = ControlLineaBase()




@app.route('/indexReporte')
def indexReportes():
    proyectos = controlador.getProyectos()
    
    return render_template('IndexReporte.html', proyectos = proyectos )



def create_pdf(pdf_data):
    pdf = StringIO()
    pisa.CreatePDF(StringIO(pdf_data), pdf)
    return pdf


# esta es la que hace la lista de los item por fase
#@app.route("/informe/listadoitem/<idProyecto>")
#@app.route("/informe/listadoitem/")
@app.route('/informe/listadoItem', methods=['GET','POST'])
def pruebaReporte():
    '''  genera un reporte  '''
    
    idProyecto = request.form['idProyecto']
    
    proyecto = controlador.getProyectoById(idProyecto)
    fases = controlFase.getFasesByIdProyecto(idProyecto)
    listadoFinal = [];
    #Recorre las fases del proyecto
    for f in fases:
        items = []
        lista = list(f.items)
        #Recolectamos los items de la fase
        for item in lista:
            datoItem = controlItem.getDatoActualByIdItemActual(item.idItemActual)
            #items.append(item)
            items.append({"numero": item.numero,
                          "nombre": item.nombreItemActual,                          
                          "version": item.ultimaVersion,
                          "prioridad": datoItem.costo,
                           })
                          #"prioridad" :  datoItem.prioridad })
        
        listadoFinal.append ({"nombre": f.nombre,
                             "numero": f.numeroFase,
                             "items": list(items),
                             })
        
    
    print listadoFinal
    
    
    pdf = create_pdf(render_template('testReporte.html', lista = listadoFinal))
    resp = Response(response=pdf.getvalue(),
                    status=200,
                    mimetype="application/pdf")
    return resp
    '''
    return render_template('testReporte.html', lista = listadoFinal)
    '''

def itemPorProyecto(idProyecto):
    ''' Devuelve un listado de todo los item de un proyecto '''
    
    proyecto = controlador.getProyectoById(idProyecto)
    itemsPro = []
    for f in proyecto.fases:
        lista =  controlItem.getItemByFase(f.idFase)
        for i in lista:
            itemsPro.append(i)

    return itemsPro


@app.route('/informe/pasoMedio', methods=['GET','POST'])
def elejirItem():
    idProyecto = request.form['idProyecto']
    items = itemPorProyecto(idProyecto);
    
    return render_template('pasoMedioReporte.html', items = items)



#@app.route("/informe/historialItem/<idItemActual>")
#@app.route("/informe/historialItem/")
@app.route('/informe/pasoMedio/listadoItem', methods=['GET','POST'])
def historialDeItem():
    idItemActual = request.form['idItemActual']
    '''  genera un reporte  '''
    item = controlItem.getItemById(idItemActual)
    
    
    
    pdf = create_pdf(render_template('historialReporte.html', item = item))
    resp = Response(response=pdf.getvalue(),
                    status=200,
                    mimetype="application/pdf")
    return resp
    






def listadoSolicitudesByProyecto(idProyecto):
    ''' Devuelve un listado de las sol '''
    listaSol = controlSolicitud.getSolicitudes()
    proyecto = controlador.getProyectoById(idProyecto)
    soles = []
    for f in proyecto.fases:
        lista =  controlItem.getItemByFase(f.idFase)
    
        listaNueva = []
        for i in lista:
            for ls in listaSol:
                if i.idItemActual == ls.idItem:
                    listaNueva.append(ls)
                    soles.append(ls)
        
    

    return soles




@app.route('/informe/solicitud', methods=['GET','POST'])
def informeSolicitud():
    idProyecto = request.form['idProyecto']
    '''  genera un reporte  '''
    sol = listadoSolicitudesByProyecto(idProyecto)
    print "solicitudes"
    print sol
    usuarioLista = controlUsuario.getUsuarios()
    
    solicitudDic = []    
    for s in sol:
        dato = controlItem.getDatoActualByIdItemActual(s.idItem)
        lbAfectada = dato.itemLB
        print "son las lb afectadas"
        #print lbAfectada.idItemActual
        for a in lbAfectada:
            #lb =  controlLineaBase.getLineaBaseById(a)
            #print lb
            print a.idLB
            solicitudDic.append({   "codigo": s.idSolicitud,
                                "nombre": s.nombreSolicitud,                          
                                "usuario": s.idUsuario,
                                "votantes": s.votantes,
                                "estado": s.estado,
                                "LB Afectada": a.idLB,
                            })
        
    
    
    
    
    
    pdf = create_pdf(render_template('reporteSol.html', sol = sol, usuarioLista = usuarioLista, solicitudDic = solicitudDic))
    resp = Response(response=pdf.getvalue(),
                    status=200,
                    mimetype="application/pdf")
    return resp



