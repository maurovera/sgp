'''
Created on 02/05/2013

@author: cathesanz
'''
#INDEX

import datetime
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlProyecto
from app.modelo import Proyecto
from app.modelo import Fase

from app.controlador import ControlFase
from app.controlador import ControlTipoItem
from app.modelo import Usuario
from contextlib import closing

controlador = ControlProyecto()
controlFase = ControlFase()
controlTipoIndex =  ControlTipoItem()


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
    p = controlador.getProyectoById(idProyecto)
    return render_template('indexAdministrarFases.html', proyecto = p )

#@app.route("/admfases/administrar/administrarTipoItem")
#@app.route("/admfases/administrar/administrarTipoItem/<idProyecto>/<idFase>")
#def administrarTipoItem(idProyecto=None,idFase=None):
    
    
#    return redirect(url_for('indexTipoItem'))


#def administrarItem():
    
#@app.route("/proyecto/fase/eliminar")
#@app.route("/proyecto/fase/eliminar/<idProyecto>/<idFase>")
#def administrarItem(idProyecto,idFase):
   

    #return redirect(url_for('iniciarProyecto', idProyecto= idProyecto))


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