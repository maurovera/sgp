'''
Created on 02/05/2013

@author: cathesanz
'''
#INDEX
from xhtml2pdf import pisa
from StringIO import StringIO
import datetime
from flask import render_template, flash, redirect, request, session, g, url_for, abort, Response
from app import app
from app.controlador import ControlProyecto
from app.modelo import Proyecto
from app.modelo import Fase

from app.controlador import ControlFase
from app.controlador import ControlTipoItem
from app.controlador import ControlRelacion
from app.controlador import ControlItem
from app.modelo import Usuario
from contextlib import closing

controlador = ControlProyecto()
controlFase = ControlFase()
controlTipoIndex =  ControlTipoItem()
controlRelacion = ControlRelacion()
controlItem = ControlItem()

def busquedaPorNombre(nombre):
    ''' Devuelve un listado de los proyectos que coincidan con un nombre '''
    lista = None
    r = True
    if(r):
        lista = controlador.buscarPorNombre(nombre)
    else:
        flash("Error. Lista no devuelta")
    return lista

def listadoProyectos():
    ''' Devuelve un listado de los Proyectos '''
    lista = None
    r = True
    if(r):
        lista = controlador.getProyectos()
    else:
        flash("Error. Lista no devuelta")
    return lista



@app.route('/admfases')
def indexFase():
    ''' Devuelve los datos de un proyecto en Concreto '''
    proyectos = listadoProyectos();
    
    return render_template('indexfases.html', proyectos = proyectos)



@app.route("/admfases/principal", methods=['GET','POST'])
def mostrarProyecto():
    
    id = request.form["idProyecto"]
    print id
    if FinalProyecto(id):
        proyecto = controlador.getProyectoById(id)
        proyecto.estado = 'finalizado'
        controlador.modificarProyecto(proyecto)
    else:
        proyecto = controlador.getProyectoById(id)
        proyecto.estado = 'iniciado'
        controlador.modificarProyecto(proyecto)    
        
    
    #nombre de la funcion y los parametros
    return redirect(url_for('indexAdministrarFase', idProyecto = id))
    #return render_template('indexAdministrarFases.html', idProyecto = id )

#@app.route('/admfases/recibeId')
#@app.route('/admfases/recibeId/<id>')
#def recibeId(id = None):
 #   proyectoF = controlador.getProyectoById(id)
  #  return redirect(url_for('iniciarProyecto', proyecto = proyectoF))    
        
    
#--------------------------aca van a ir los vistas de administrar fases--------
# jajaja ---------------------------------------------------------------------- 
#------------------------------------------------------------------------------

#-------------- aqui inicia la parte de fases jajaja.....................
@app.route("/admfases/administrar")
@app.route("/admfases/administrar/<idProyecto>")
def indexAdministrarFase(idProyecto):
    
    '''Se encarga de dar inicio a un proyecto '''
    
    # aqui deberia haber un control de cambio 
    
    p = controlador.getProyectoById(idProyecto)
    return render_template('indexAdministrarFases.html', proyecto = p )




def FinalProyecto(idProyecto):
    valor = True
    proyecto =  controlador.getProyectoById(idProyecto)
    for f in proyecto.fases:
        if f.estado != 'final':
            valor = False
           
    return valor

@app.route("/admfases/salir") 
@app.route("/admfases/salir/<idProyecto>")
def salirDeAdminFase(idProyecto = None):
    if FinalProyecto(idProyecto):
        proyecto = controlador.getProyectoById(idProyecto)
        proyecto.estado = 'finalizado'
        controlador.modificarProyecto(idProyecto)
    else:
        proyecto = controlador.getProyectoById(idProyecto)
        proyecto.estado = 'iniciado'
        controlador.modificarProyecto(idProyecto)    
    
    return redirect(url_for('indexFase'))



def generarColor(n):
    colores = ["#f55","#5f5","#55f","#ccc","#aa5","#5aa","#a5a","#bab","#000","#999","#fab"]

    return colores[n % 10]

@app.route("/admfases/administrar/grafo")
@app.route("/admfases/administrar/grafo/<idProyecto>")
def grafoProyecto(idProyecto):
    
    '''Se encarga de dar inicio a un proyecto '''
    proyecto = controlador.getProyectoById(idProyecto)
    fases = list(proyecto.fases)
    listadoItem = []
    for f in fases:
        for i in f.items:
            if i.eliminado == False:
                listadoItem.append(i)
    
    print listadoItem
    
    relaciones = controlRelacion.getRelacionesByIdProyecto(idProyecto)
    print relaciones
    
    ''' 
                nodes:{
                     ${grafo['nodos']}
                   },

                   edges:{
                     ${grafo['aristas']}
                   }
        
        str(p_item.id_item_actual) + " : {'color': '#333', 'shape': 'box', 'label': '" +\
                           self.codigo + "(" + str(p_item.complejidad) + ")'},\n"
    '''
    
    json = "nodes: {"
    
    for i in listadoItem:
        f = controlFase.getFaseById(i.idFase)
        
        color = generarColor(f.numeroFase)
        x = 5 * f.numeroFase
        nodo = str(i.idItemActual) + " : {'color': '"+color+"', 'shape': 'box', 'label': '" +\
                           i.nombreItemActual + "', 'x' : " +str(x)+ "},\n"
        json = json + nodo
    
    json = json + "},\n"
    
    json = json + "edges:{"
    
    for r in relaciones:
        '''bar:{foo:{similarity:0},
              baz:{similarity:.666}'''
        arista = str(r.idAntecesor) + ":{" + str(r.idSucesor) + " : {similarity:666, pointSize:3, length: 10, color : '#f00' } },\n"
        json = json + arista
    
    json = json + "}"
    print json
    
    return render_template('indexGrafo.html', proyecto = proyecto, json=json )



def create_pdf(pdf_data):
    pdf = StringIO()
    pisa.CreatePDF(StringIO(pdf_data), pdf)
    return pdf

@app.route("/informe/listadoitem/<idProyecto>")
@app.route("/informe/listadoitem/")
def pruebaReporte(idProyecto):
    
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
            items.append({"nombre": item.nombreItemActual,
                          "eliminado": item.eliminado,
                          "version": item.ultimaVersion,
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
