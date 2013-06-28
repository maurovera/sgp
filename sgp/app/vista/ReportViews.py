'''
Created on 18/06/2013

@author: victor
'''

import datetime
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from flask.helpers import send_file
from geraldo.generators import PDFGenerator



from app.modelo import Fase
#from pm.models.HistorialDetalle import HistorialDetalle
from app.modelo import HistorialItems
from app.modelo import Item
from app.modelo import LineaBase
from app.modelo import MyReport
from app.modelo import Proyecto
from app.modelo import Relacion
from app.modelo import SolicitudCambio


import StringIO
import os



@app.route('/report/proyectoitems', methods=['GET', 'POST']) 
def proyectoitemsReporte():
    """
        Reporte de items de un proyecto ordenado por fases
        @param id_proyecto: identificador del proyecto del cual se hara el reporte
    """
    params = {'GET':request.args, 'POST':request.form}[request.method]
    response = {}
    if not ensureParams(params, ['id_proyecto']): 
        response = {"success" : False , "msg" : "Parametros Insuficientes!!"} 
        return response
    try:
        listaItems = []
        id_proyecto= int(str(params['id_proyecto']))
        proyecto = Proyectos.query.filter(Proyectos.id_proyecto==id_proyecto).one()
        fases = Fases.query.filter(Fases.id_proyecto==id_proyecto).all()
        if fases:
            for f in fases:
                items = Items.query.filter(Items.id_fase==f.id_fase).all()
                if items:
                    for i in items:
                        if i.estado!=6:
                            estructura ={"Nombre" : i.nombre, "Descripcion": i.descripcion, "Version": i.version, 
                                         "Prioridad":i.prioridad, "Complejidad": i.complejidad, "Costo": i.costo,
                                         "Fase": f.nombre, "Fase-Descripcion": f.descripcion, "PosicionF": f.posicion}
                            listaItems.append(estructura)
        
    except Exception, e:
        print e
        response ={"success" : False , "msg" : "Ups!! Hubo un error al intentar obtener los valores"}
        return response
    if not listaItems:
        estructura ={"Nombre" : "-", "Descripcion": "-", "Version": "-", 
                    "Prioridad":"-", "Complejidad": "-", "Costo": 0,
                    "Fase": "-", "Fase-Descripcion": "-", "PosicionF": "-"}
        listaItems.append(estructura)

    listaItems.sort(lambda a,b: cmp(a['PosicionF'], b['PosicionF']))
    my_report = MyReport(queryset=listaItems)
    
    strIO = StringIO.StringIO()
    my_report.generate_by(PDFGenerator, filename=strIO)
    strIO.seek(0)
    
    return send_file(strIO,
                     attachment_filename="reporteItemsPorFase.pdf",
                     as_attachment=False)
    
    
@app.route('/report/historialitem', methods=['GET', 'POST']) 
def historialItemReporte():
    """
        Reporte del historial de un item
        Historial de item, Un usuario podra elegir un item dado y generar 
        un reporte que liste los valores de cada version del mismo.
        @param id_item: identificador del item sobre el cual se hara el historial
    """
    params = {'GET':request.args, 'POST':request.form}[request.method]
    response = {}
    if not ensureParams(params, ['id_item']): 
        response = {"success" : False , "msg" : "Parametros Insuficientes!!"} 
        return response
    try:
        listaItems = []
        id_item= int(str(params['id_item']))
        itemActual = Items.query.filter(Items.id_item==id_item).one()
        historialItem = HistorialItem.query.filter(HistorialItem.id_item==id_item).all()
        for hi in historialItem:
            
            historial_detalle= HistorialDetalle.query.filter(HistorialDetalle.id_historial_item==hi.id_historial_item).all()
    
            listaHijos=""
            for hd in historial_detalle:
                relacion_item=Relaciones.query.filter(Relaciones.id_relacion== hd.id_relacion).one()
                if hd.estado_relacion!=False and relacion_item.tipo==1 and relacion_item.nombre_destino!=itemActual.nombre:
                    listaHijos = listaHijos + relacion_item.nombre_destino + " ,"  
            
            listaPadres=""
            for hd in historial_detalle:
                relacion_item=Relaciones.query.filter(Relaciones.id_relacion== hd.id_relacion).one()
                if hd.estado_relacion!=False and relacion_item.tipo==1 and relacion_item.nombre_origen!=itemActual.nombre:
                    listaPadres = listaPadres + relacion_item.nombre_origen + " ,"    
                    
            listaSucesores=""
            for hd in historial_detalle:
                relacion_item=Relaciones.query.filter(Relaciones.id_relacion== hd.id_relacion).one()
                if hd.estado_relacion!=False and relacion_item.tipo==2 and relacion_item.nombre_destino!=itemActual.nombre:
                    listaSucesores = listaSucesores + relacion_item.nombre_destino + " ,"    
            
            listaAntecesores=""
            for hd in historial_detalle:
                relacion_item=Relaciones.query.filter(Relaciones.id_relacion== hd.id_relacion).one()
                if hd.estado_relacion!=False and relacion_item.tipo==2 and relacion_item.nombre_origen!=itemActual.nombre:
                    listaAntecesores = listaAntecesores + relacion_item.nombre_origen + " ,"  
            
            
            estructura ={"Nombre" : hi.nombre, "Descripcion": hi.descripcion, "Version": hi.version, 
                         "Prioridad":hi.prioridad, "Complejidad": hi.complejidad, "Costo": hi.costo
                         ,"relaciones":[{"padres":listaPadres, "hijos": listaHijos,"sucesores":listaSucesores,"antecesores":listaAntecesores}]}
            listaItems.append(estructura)
        
    except Exception, e:
        print e
        response ={"success" : False , "msg" : "Ups!! Hubo un error al intentar obtener los valores"}
        return response

    listaItems.sort(lambda a,b: cmp(a['Nombre'], b['Nombre']))
    my_report = Reporte3(queryset=listaItems)
    
    strIO = StringIO.StringIO()
    my_report.generate_by(PDFGenerator, filename=strIO)
    strIO.seek(0)
    
    return send_file(strIO,
                     attachment_filename="reporteHistorialItem.pdf",
                     as_attachment=False)
    

@app.route('/report/solicitudcambio', methods=['GET', 'POST']) 
def solicitudCambioReporte():
    """
        Reporte de items de un proyecto ordenado por fases
        @param id_proyecto: identificador del proyecto del cual se hara el reporte
    """
    params = {'GET':request.args, 'POST':request.form}[request.method]
    response = {}
    if not ensureParams(params, ['id_proyecto','id_usuario']): 
        response = {"success" : False , "msg" : "Parametros Insuficientes!!"} 
        return response
    try:
        
        listaSolicitudes = []
        id_proyecto= int(str(params['id_proyecto']))
        id_usuario= int(str(params['id_usuario']))
        proyecto = Proyectos.query.filter(Proyectos.id_proyecto==id_proyecto).one()
        fases = Fases.query.filter(Fases.id_proyecto==id_proyecto).all()
        for f in fases:
            items = Items.query.filter(Items.id_fase==f.id_fase).all()
            for i in items:
                solicitudItem = Solicitud_Items.query.filter(Solicitud_Items.id_item==i.id_item).first()
                if solicitudItem:
                    solicitudCambio = SolicitudCambio.query.filter(SolicitudCambio.id_solicitud_cambio==solicitudItem.id_solicitud_cambio).first()
                    votacion = VotacionSolicitudCambio.query.filter(VotacionSolicitudCambio.id_solicitud_cambio==solicitudCambio.id_solicitud_cambio).filter(VotacionSolicitudCambio.id_usuario==id_usuario).first()
                    if votacion:
                        if votacion.voto==True:
                            voto = 'Si'
                        else:
                            voto= 'No'
                    else:
                        voto='No'
                    if solicitudCambio:
                        estructura ={"Solicitante" : solicitudCambio.user_name, "Estado": solicitudCambio.estado, 
                                 "LB_Afectada": solicitudCambio.lbs_afectadas, "Voto_Lider":voto, "id_solicitud":solicitudCambio.id_solicitud_cambio}
                        if estructura not in listaSolicitudes:
                            listaSolicitudes.append(estructura)
    except Exception, e:
        print e
        response ={"success" : False , "msg" : "Ups!! Hubo un error al intentar obtener los valores"}
        return response
    if not listaSolicitudes:
        estructura ={"Solicitante" : "-", "Estado": "-", 
                     "LB_Afectada": "-", "Voto_Lider":"-", "id_solicitud":"-"}
        listaSolicitudes.append(estructura)
    listaSolicitudes.sort(lambda a,b: cmp(a['id_solicitud'], b['id_solicitud']))
    my_report = Reporte1(queryset=listaSolicitudes)
    
    strIO = StringIO.StringIO()
    my_report.generate_by(PDFGenerator, filename=strIO)
    strIO.seek(0)
    
    return send_file(strIO,
                     attachment_filename="reporteSolicitudesCambio.pdf",
                     as_attachment=False)