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
from app.modelo import Rol

from app.controlador import ControlFase
from app.controlador import ControlTipoItem
from app.controlador import ControlRelacion
from app.controlador import ControlItem
from app.controlador import ControlRol
from app.controlador import ControlUsuario
from app.modelo import Usuario
from contextlib import closing

controlador = ControlProyecto()
controlFase = ControlFase()
controlTipoIndex =  ControlTipoItem()
controlRelacion = ControlRelacion()
controlItem = ControlItem()
controlRol = ControlRol()
controlUsuario = ControlUsuario()

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

def listaProyectoPorRoles(idUsuario):
    ''' lista de proyectos por roles de usuario ''' 
    # el usuario logeado
    usuario = controlUsuario.getUsuarioById(session['idUsuario'])
    
    # si es root
    if usuario.nombreUsuario == "root":
        print usuario.nombreUsuario
        retorno = []
        lista = controlador.getProyectos()
        for p in lista:
            noini = "no iniciado"
            eli = "eliminado"
            if p.estado != noini and p.estado != eli:
                    retorno.append(p)
        
        
        
            
        return retorno
    
    #si no es root
    else:
        print "entreeeeeeeeeeeeeeeeeeeeeeeee"
        #usuario = idUsuario
        #quitar los id de proyecto de todo los roles del usuario
        proRepetidos = []
        for rol in usuario.roles:
            if rol.idProyecto != None:
                proRepetidos.append(rol.idProyecto)
            
        #quitamos los repetidos y cargamos lo que no son repetidos en proyectos    
        proyectos = []
        for a in proRepetidos:
            if a not in proyectos:
                proyectos.append(a)
                
        proyectosN = []
        for a in proyectos:
            b =  controlador.getProyectoById(a)   
            proyectosN.append(b)
        
        retorno = []
        for p in proyectosN:
            noini = "no iniciado"
            eli = "eliminado"
            if p.estado != noini and p.estado != eli:  
                retorno.append(p) 
        
        
        return retorno


def usuarioRootVeTodo():
    usuario = controlUsuario.getUsuarioById(session['idUsuario'])
    retorno = []
    if usuario.nombreUsuario == "root":
        
        lista = controlador.getProyectos()
        for proyecto in lista:
            if proyecto.estado != False:
               retorno.append(proyecto)
               
    return retorno 
        
         

@app.route('/admfases')
@app.route('/admfases/<idUsuario>')
def indexFase(idUsuario= None):
    ''' Devuelve los datos de un proyecto en Concreto '''
    ''' devuelve los proyectos que seran desarrollados '''
    
    p = listadoProyectos();
    proyectos = listaProyectoPorRoles(idUsuario);
    proyectosRoot = usuarioRootVeTodo();
    
    listaVerdad = listaProyectoPorRoles(idUsuario);
    print "esta es la listaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    print listaVerdad
    vacio = False
    if len(list(listaVerdad) ) == 0:
        vacio = True 
    
    
    return render_template('indexfases.html',vacio = vacio, proyectos = p, proyectosRoot = proyectosRoot, listaVerdad = listaVerdad)



@app.route("/admfases/principal", methods=['GET','POST'])
def mostrarProyecto():
    ''' recibe el proyecto seleccionado y lo redirecciona a la funcion indexAdministrarFase '''
    # id del proyecto seleccionado
    i = request.form["idProyecto"]
 
    
    
    print i
    if FinalProyecto(i):
        proyecto = controlador.getProyectoById(i)
        proyecto.estado = 'finalizado'
        controlador.modificarProyecto(proyecto)
    else:
        proyecto = controlador.getProyectoById(i)
        proyecto.estado = 'iniciado'
        controlador.modificarProyecto(proyecto)    
        
    
    
    
    return redirect(url_for('indexAdministrarFase', idProyecto = i))
    


def listadoFasesAutorizadas(idProyecto):
    #es el proyecto seleccionado
    proyecto = controlador.getProyectoById(idProyecto)
    # el usuario logeado
    usuario = controlUsuario.getUsuarioById(session['idUsuario'])
    
    #buscamos todo los roles del proyecto
    ''' trae los roles del usuario asociado al proyecto '''
    roles = controlRol.getRolPorProyecto(idProyecto)
    listaDeRoles = []
    for rol in roles:
        # si este rol tiene el usuario entonces meter
        if rol in usuario.roles:
            #esta es la lista de los roles que el usuario tiene en este proyecto 
            listaDeRoles.append(rol)
    
    
    
    
    
    # si el usuario logeado es root
    if controlUsuario.esUsuarioRoot(usuario) :
        return proyecto.fases
   
   
    # si no es root
    else:
        
        
        hayUnGeneral = Fase
        # solo controla que haya un none osea que tenga todo los permisos
        for fase in listaDeRoles:
            if fase.idFase == None:
                hayUnGeneral = True
                break
     
        #si tiene fases none puede ver toda las fases
        # osea si tiene en el rol idproyecto = proyecto actual y rol.idFase = none
        # es un admin o lo que fuere 
        if hayUnGeneral == True:
            return proyecto.fases
        # si no tiene fases none entonces trae toda las fases
        # tiene fases especificas
        else:
            RepetidoFaseId = []
            #quita los id de fase repetidos
            for repetido in listaDeRoles:
                if repetido.idFase != None:
                    RepetidoFaseId.append(repetido.idFase)
            #quita los id de fase no repetidos        
            noRepetidoFaseId = []
            for noRepetido in RepetidoFaseId:
                if noRepetido  not in  noRepetidoFaseId:
                    noRepetidoFaseId.append(noRepetido)
                    
            #quita las fases en si 
            retorno = []
            for f in noRepetidoFaseId:
                fase = controlFase.getFaseById(f)
                retorno.append(fase)

            return retorno
            
                    
                
            
            
            
            
    
    
    
    
            
    
    
    
    
    
        
        




#-------------- aqui inicia la parte de fases jajaja.....................
@app.route("/admfases/administrar")
@app.route("/admfases/administrar/<idProyecto>")
def indexAdministrarFase(idProyecto):
    
    '''Se encarga de dar inicio a un proyecto '''
    ''' este renderea el tema de las fases de un proyecto '''
    # aqui deberia haber un control de cambio 
    listadoDeFases = listadoFasesAutorizadas(idProyecto)
    p = controlador.getProyectoById(idProyecto)
    return render_template('indexAdministrarFases.html', proyecto = p, lista = listadoDeFases )




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
    
    ''' se genera conjunto de nodes y aristas para el arbor '''    
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
    
    #for r in relaciones:
        #arista = str(r.idAntecesor) + ":{ " + str(r.idSucesor) + " : {} },\n"
        #json = json + arista
    
    json = json + arista(idProyecto) +" }"
    print json
    '''
    # json de prueba jajajja
    # prueba con otros valores jajaja
    #post = "nodes:{\n"
    #joe = "joe:{'color':'orange','shape':'dot','label':'joe'},\n"
    
    #fido = "fido:{'color':'green','shape':'dot','label':'fido'},\n"
    #fluffy=  "fluffy:{'color':'blue','shape':'dot','label':'fluffy'}\n },"
    #ed = "edges:{\n"
    #rel1 = "dog:{ fido:{} },\n"
    #rel2=  "cat:{ fluffy:{} },\n"
    #rel3 =    "joe:{ fluffy:{},fido:{} }\n }"
    #rel4 =    "fluffy:{ fido:{} },\n"
    #envio = post + joe + fido + fluffy + ed+ rel4 +rel3  
    #print envio

    ''' 
    
    return render_template('indexGrafo.html', proyecto = proyecto, json=json )







def arista(idProyecto):
    '''' arista del grafo'''
    # todas las relaciones del proyecto
    relaciones = controlRelacion.getRelacionesByIdProyecto(idProyecto)
    
    #quitar los antecesores
    antecesores = []
    for ant in relaciones:
        antecesores.append(ant.idAntecesor)
        
    #quitamos los repetidos antecesores     
    listaDeAntecesores = []
    for i in antecesores:
        if i not in listaDeAntecesores:
            listaDeAntecesores.append(i) 
    
    
    # se genera las aristas del grafo
    arista =  ""
    for cabecera in listaDeAntecesores:
        arista = arista + str( cabecera)+":{ "
        sucesores = controlRelacion.getItemsSucesores(cabecera)
        for suc in sucesores:
            post = suc.idSucesor
            arista= arista + str(post)+":{},"
        
        arista = arista + "},\n"
        
    print "esta es la arista"
    print arista
    print "*************************"
    return arista


