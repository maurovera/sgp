#INDEX
import datetime
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlItem
from app.modelo import Item
from app.modelo import DatosItem
from app.modelo import HistorialItems
from contextlib import closing

#---------------------------------------------
# no se si sirve de algo esto
from app.controlador import ControlUsuario
from app.controlador import ControlPermiso
from app.controlador import ControlTipoItem
from app.controlador import ControlFase
from app.controlador import ControlProyecto
from app.controlador import ControlRelacion
from app.controlador import ControlDatosItem
from app.controlador import ControlLineaBase
from app.controlador import ControlHistorialItems
from app.controlador import ControlAtributoDeItem
from app.modelo import Usuario
from app.modelo import AtributoDeItem
#----------------------------------------------
controlRelacion =  ControlRelacion()
control = ControlItem()

controlHistorialItems = ControlHistorialItems()
controladorDatosItem = ControlDatosItem()
controlTipoItem = ControlTipoItem()
controlFase = ControlFase()
controlProyecto = ControlProyecto()
controladorusuario = ControlUsuario()
controlLineaBase = ControlLineaBase()
controlAtributoDeItem = ControlAtributoDeItem()

def listadoItem(idFase):
    ''' Devuelve un listado de los tipo item '''
    lista = None
    r = True
    if(r):
        lista = control.getItemByFase(idFase)
    else:
        flash("Error. Lista no devuelta")
    return lista


def listadoTipoItem(idFase):
    ''' Retorna una lista de Tipos de Item que corresponde a la fase'''
    lista = controlTipoItem.getTipoItemByFase(idFase)
    return lista


@app.route('/item')
@app.route('/item/<idProyecto>/<idFase>')
def indexItem(idProyecto=None,idFase=None):
    ''' Devuelve los datos de un item en Concreto '''
    items = listadoItem(idFase);
    tipoItems = listadoTipoItem(idFase);
    nombresTipoItem = {}
    for tipo in tipoItems:
        nombresTipoItem[tipo.idTipoItem] = ''+ tipo.nombre

    estadosItem = {}
    for item in items:
        datos = item.datos
        for dItem in datos:
            if dItem.version == item.ultimaVersion :
                estadosItem[item.idItemActual] = dItem.estado
    
    #esta es la ultima modificacion            
    #estadoDeLaFase(idFase, idProyecto)
    vacio = False
    if len(tipoItems) == 0:
        vacio = True
           
    return render_template('indexItem.html', items = items, idProyecto = idProyecto, idFase = idFase, tipoItems = tipoItems, nombresTipoItem = nombresTipoItem, estadosItem = estadosItem, vacio = vacio)


@app.route('/item/eliminar')
@app.route('/item/eliminar/<idProyecto>/<idFase>/<idUsuario>/<id>')
def eliminarItem(idProyecto=None,idFase=None, idUsuario = None ,id=None):
    
    item = control.getItemById(id)
    datos = control.getDatoActualByIdItemActual(id)
    if datos.estado == 'aprobado':
        flash("no se puede eliminar, esta en un estado aprobado")
        return redirect(url_for('indexItem', idProyecto=idProyecto, idFase=idFase))
    elif datos.estado == 'final':
        flash("no se puede eliminar, esta en un estado final")
        return redirect(url_for('indexItem', idProyecto=idProyecto, idFase=idFase))             
    else:
        # se elimina todas sus relaciones
        eliminarRelacionPorItem(id)
        datos.estado = "eliminado"
        controladorDatosItem.modificarDatosItem(datos)    
        r= control.eliminarItem(item)
        if(r["estado"] == True):
            estadoDeLaFaseAlEliminar(idFase, idProyecto)
            
            # parte del historial
            historial = HistorialItems()
            historial.idUsuario = idUsuario
            historial.tipoModificacion = "eliminacion de item"
            historial.fechaModificacion = str(datetime.date.today())
            historial.idItem = item.idItemActual
        
            controlHistorialItems.nuevoHistorialItems(historial)
            
            
            
            flash("Se elimino con exito el item: " + str( item.numero) )
        else:
            flash("Ocurrio un error: "+ r["mensaje"])
        
    return redirect(url_for('indexItem', idProyecto=idProyecto, idFase=idFase))




@app.route('/item/nuevo', methods=['GET','POST'])
def nuevoItem():
    ''' Crea un nuevo Item '''
    #Si recibimos algo por post



    if request.method == 'POST' :



        idProyecto = request.form['idProyecto']
        idFase = request.form['idFase']
        idTipoItem = request.form['idTipoItem']
        nombreItem = request.form['nombreItem']
        idUsuario = request.form['idUsuario']
        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente
        #con un metodo kachiai
        if(idFase and idTipoItem and nombreItem):
            #Se necesita cargar todos los atributos del tipo item.
            item = Item()
            item.idFase = idFase
            item.idTipoItem = idTipoItem
            item.eliminado = False
            item.nombreItemActual = nombreItem
            fase = controlFase.getFaseById(idFase)
            tipoItem = controlTipoItem.getTipoItemById(idTipoItem)
            numero = len( list(fase.items) ) + 1
            item.numero = numero
            item.ultimaVersion = 0
           
          
            


            r = control.nuevoItem(item)
            if (r["estado"] == True):
                estadoDeLaFase(idFase, idProyecto)
                # parte del historial
                historial = HistorialItems()
                historial.idUsuario = idUsuario
                historial.tipoModificacion = "nuevo item"
                historial.fechaModificacion = str(datetime.date.today())
                historial.idItem = item.idItemActual
        
                controlHistorialItems.nuevoHistorialItems(historial)

                # se crea un dato item si o si para evitar dramas
                datoPorDefault(item, idTipoItem)
                
                    
                return redirect(url_for('datos', idProyecto = idProyecto, idItemActual = item.idItemActual ))
            else:
                flash("Ocurrio un error " + r["mensaje"])


           


    return redirect(url_for('indexItem', idProyecto=idProyecto, idFase=idFase))


def datoPorDefault(item, idTipoItem):
        datos = DatosItem()
        datos.version = 1
        datos.complejidad = 0
        datos.prioridad = 0
        datos.costo = 0
        datos.estado = "inicial"
        datos.idItemActual = item.idItemActual
        

        item.ultimaVersion = datos.version

        
        control.agregarDatosItem(item,datos)
        
        #Cargamos los atributos
        print "Empezamos a meter los atributos por item"
        tipoItem = controlTipoItem.getTipoItemById(idTipoItem)
        atributos = list(tipoItem.atributosPorTipoItem)
        #Recorremos los atributos que pertenecen al tipo
        for atributo in atributos :
            valor = "vacio"
            atributoDeItem = AtributoDeItem()
            atributoDeItem.valor = valor
            atributoDeItem.idAtributoPorTipoItem = atributo.idAtributosPorTipoItem
            controlAtributoDeItem.nuevoAtributoDeItem(atributoDeItem)
            controladorDatosItem.agregarAtributoDeItem(datos, atributoDeItem)
       




@app.route('/item/modificar', methods=['GET','POST'])
def modificarItem():
    ''' Modifica un item '''



    if request.method == 'POST' :


        #print request.form['nombre']
        #print request.form['codigo']
        #print request.form['descripcion']
        #print request.form['idTipoItem']

        id = request.form['idItemActual']

        numero = request.form['numero']
        #eliminado = request.form['eliminado']
        #if eliminado == 1:
        #    eliminado= True
        #elif eliminado == 0:
        #    eliminado = False

        #ultimaVersion = request.form['ultimaVersion']

        idProyecto = request.form['idProyecto']
        idFase = request.form['idFase']

        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente
        #con un metodo kachiai
        if(id and numero):
            item = control.getItemById(id)
            if (item):
                item.numero = numero
                #item.eliminado = eliminado
                #item.ultimaVersion = ultimaVersion



                r = control.modificarItem(item)
                if( r["estado"] == True ):
                    flash("Modficado con exito el item")
                else:
                    flash("Ocurrio un error : " + r["mensaje"])


    return redirect(url_for('indexItem', idProyecto=idProyecto, idFase=idFase))


@app.route('/item/revivir')
@app.route('/item/revivir/<idProyecto>/<idFase>/<idUsuario>/<id>')
def revivirItem(idProyecto=None, idFase= None, idUsuario = None,id=None):
    item = control.getItemById(id)
    item.eliminado = False
    control.modificarItem(item)
    
    #historial para revivir
    historial = HistorialItems()
    historial.idUsuario = idUsuario
    historial.tipoModificacion = "revivir item"
    historial.fechaModificacion = str(datetime.date.today())
    historial.idItem = item.idItemActual
    controlHistorialItems.nuevoHistorialItems(historial)
    
    
    
    dato = control.getDatoActualByIdItemActual(id)
    dato.estado = "listo"
    controladorDatosItem.modificarDatosItem(dato)
    #historial del dato
    historialN = HistorialItems()
    historialN.idUsuario = idUsuario
    historialN.tipoModificacion = "estado de item a listo"
    historialN.fechaModificacion = str(datetime.date.today())
    historialN.idItem = item.idItemActual
    controlHistorialItems.nuevoHistorialItems(historialN)
    
    
    # control para cambiar el estado de la fase y del proyecto
    estadoDeLaFase(idFase, idProyecto)

    return redirect(url_for('datos', idProyecto = idProyecto, idItemActual = id ))

#@app.route("/item/buscar")
#@app.route("/item/buscar/<nombrebuscado>")
#def buscarTipoItem(nombrebuscado):
#    ''' Devuelve una lista de tipo de items que coincidan con el nombre proporcionado '''
#    print "Helloooooowww"
#    tipoItems = busquedaPorNombre(nombrebuscado);
#    return render_template('indexTipoItem.html', tipoItems = tipoItems)

# se agrego importar tipoItem entre fases
def corroborarFaseFinal(idFase):
    valor = False
    listaItem = listadoItem(idFase);
    
    for i in listaItem:
        if i.eliminado == False:
            if( not control.comprobarItemEstadofinal(i) ):
                valor = True
    
    return valor
              

def corroborarSiTieneItem(idFase):
    valor = False
    listaDeItem = listadoItem(idFase);
    for i in listaDeItem:
        if i.eliminado == False: 
                valor = True
    
    return valor 

def corroborarSiTieneLB(idFase):
    ''' corroborar si tiene una linea base '''
    valor = False
    listaLB = controlLineaBase.getLBByFase(idFase)
    
    
    for l in listaLB:
        #si la linea base no esta liberada
        if l.estado != 1:
            valor = True
    
    return valor    
   
    
def estadoDeLaFase(idFase, idProyecto):
    faseActual = controlFase.getFaseById(idFase)
    proyecto = controlProyecto.getProyectoById(idProyecto)
    #if faseActual.estado == 'final':    
    if corroborarSiTieneLB(idFase):
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





def eliminarRelacionPorItem(idItemActual):
         
        itemActual = control.getItemById(idItemActual)
        listaDeRelacion = controlRelacion.getRelaciones()
        
        for r in listaDeRelacion:
            if (r.idAntecesor == itemActual.idItemActual or r.idSucesor == itemActual.idItemActual ):
                controlRelacion.eliminarRelacion(r)



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