'''
Created on 03/05/2013

@author: Mauro
'''

from app.modelo import Item
from app.modelo import DatosItem
from app import db
from crelacion import ControlRelacion


class ControlItem():
    """ clase control  item """
    def getItemById(self,id):
        """ funcion getItembyid """
        return Item.query.get(id)
    def getItems(self):
        """ funcion getItems """
        return Item.query.all()
    def getItemByFase(self,idFase):
        """ funcion que filtra solo por las fases """
        retorno = db.session.query(Item).filter(Item.idFase == idFase ).all()
        return retorno
        
    def nuevoItem(self, item):
        """ funcion nuevoItem """
        resultado = {"estado" : True, "mensaje" : "exito"}
        try:
            db.session.add(item)
            #print "Hice el add"
            db.session.commit()
            #print "Hice el commit"
        except Exception, error :
            #print "Capturo exp" + str(error)
            resultado = {"estado" : False, "mensaje" : str(error)}
            db.session.rollback()

        return resultado

    def eliminarItem(self, item):
        """ funcion eliminarItem """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
#           db.session.delete(item)
#            db.session.commit()
#---------------------------------------
            """ hacemos un delete de item, que lo unico que cambia sera su eliminado """
            item.eliminado = True
            db.session.merge(item)
            """ se comitea el cambio """
            db.session.commit()

#----------------------------------------
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()



        return resultado


    def modificarItem(self, item):
        """ funcion modificarUsuario """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un merge de usuario """
            db.session.merge(item)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado


#    def getItemByIdItemActual(self,idItemActual):

#        retorno = db.session.query(Item).filter(Item.idItemActual == idItemActual ).all()
#        return retorno
#-------- 03052013-------------------
# luego se agrega los atributos por tipo item

    def agregarDatosItem(self,item,datosItem):
        ''' agrega datos al item '''
        nohay = True
        for f in item.datos:
            if(datosItem == f):
                print "YA HAY eSte dato item"
                nohay = False
                break

        if (nohay):
            print "Agregamos!"
            self.verificarRelacion(datosItem)
            item.datos.append(datosItem)
            return self.modificarItem(item)
        else :
            resultado = {"estado" : False, "mensaje" : "El item ya posee estos datos"}
            return resultado

    def quitarDatosItem(self,item,datosItem):
        ''' quitar datos  '''
        item.datos.remove(datosItem)
        return self.modificarItem(item)

    def verificarRelacion(self,datosItem):
        idItemActual = datosItem.idItemActual
        cRelacion = ControlRelacion()
        relaciones = cRelacion.getRelacionByIdItemActual(idItemActual)
        datosItem.relaciones = relaciones
        print datosItem.relaciones

    def comprobarAprobado(self,item):
        datos = item.datos
        for d in datos:
            if (d.version == item.ultimaVersion):
                if(d.estado == "aprobado"):
                    return True

        return False

    def getItemAprobadoByFase(self,idFase):
        listaRetorno = []
        listaFase = self.getItemByFase(idFase)
        for i in listaFase:
            if(self.comprobarAprobado(i)):
                listaRetorno.append(i)

        return listaRetorno

    def getDatoActualByIdItemActual(self,idItemActual):
        item = self.getItemById(idItemActual)
        for dato in item.datos:
            if (dato.version == item.ultimaVersion):
                return dato


    # esta funcion fue agregada para comprobar todo los items en estado final
    def comprobarItemEstadofinal(self,item):
        ''' item en estado final '''
        datos = item.datos
        for d in datos:
            if (d.version == item.ultimaVersion):
                if(d.estado == "final"):
                    return True

        return False

    # esto se agrego en fecha 23052013
    # por mauro
    # listado de item con estado final segun esto

    def getItemFinal(self):
        ''' listado de item final '''
        listaRetorno = []
        listaitem = self.getItems()
        for i in listaitem:
            if(self.comprobarItemEstadofinal(i)):
                listaRetorno.append(i)

        return listaRetorno

    def pasarRevision(self,idItemActual, idItemOriginal, direccion):
        #Realizamos las operaciones para habilitar la modificacion
        # El item solicitado pasa a revision y su red (antecesores sucesores)
        # Los otros item en la misma LB de final a aprobado
        # La LB pasa a un estado LIBERADO
        # Las LB de su Red pasan a NO VALIDO
        #
        import crelacion, clineaBase, cdatosItem
        item = self.getItemById(idItemActual)

        print item.nombreItemActual

        #Primero modificamos los item de su LB
        datoActual = self.getDatoActualByIdItemActual(idItemActual)
        lb = list(datoActual.itemLB)[0]
        controlLB = clineaBase.ControlLineaBase()
        datosItemLB = lb.items
        for dato in datosItemLB:
            if (dato.idItemActual != idItemActual):
                dato.estado = 'aprobado'
                cdatosItem.ControlDatosItem().modificarDatosItem(dato)

        #Cambiamos su estado a revision
        datoActual.estado = 'revision'
        cdatosItem.ControlDatosItem().modificarDatosItem(dato)

        antecesores = crelacion.ControlRelacion().getAntecesores(idItemActual)
        sucesores = crelacion.ControlRelacion().getSucesores(idItemActual)

        if (direccion == -1 or direccion == 0):
            for ant in antecesores:
                if (ant == idItemOriginal):
                    break
                self.pasarRevision(ant,idItemOriginal,-1)

        if (direccion == 1 or direccion == 0):
            for suc in sucesores:
                if (suc == idItemOriginal):
                    break
                self.pasarRevision(suc,idItemOriginal, 1)


        #Cambiamos el estado de la LB
        #Liberado
        if (idItemActual == idItemOriginal):
            lb.estado = 1
        #Invaldio
        else :
            lb.estado = -1

        controlLB.modificarLineaBase(lb)

    def calcularImpacto(self,idItemActual):
        
        #Acumulador de complejidad
        complejidad = 0
        #Acumulador de costo
        costo = 0
        #Lista de Items
        listadoItem = []
        
        import crelacion
        item = self.getItemById(idItemActual)

        print item.nombreItemActual

        #Primero modificamos los item de su LB
        datoActual = self.getDatoActualByIdItemActual(idItemActual)
        complejidad += datoActual.complejidad
        #costo += datoActual.costo
        
        listadoItem.append(item.nombreItemActual)
        
        antecesores = crelacion.ControlRelacion().getAntecesores(idItemActual)
        sucesores = crelacion.ControlRelacion().getSucesores(idItemActual)

        for ant in antecesores:
            idItem = ant
            item = self.getItemById(idItem)
            datoActual = self.getDatoActualByIdItemActual(idItem)
            complejidad += datoActual.complejidad
            #costo += datoActual.costo
            listadoItem.append(item.nombreItemActual)
        for suc in sucesores:
            idItem = suc
            item = self.getItemById(idItem)
            datoActual = self.getDatoActualByIdItemActual(idItem)
            complejidad += datoActual.complejidad
            #costo += datoActual.costo
            listadoItem.append(item.nombreItemActual)

        print "IMPACTO CAMBIO"
        print [complejidad,costo,listadoItem]
        
        return [complejidad,costo,listadoItem]



