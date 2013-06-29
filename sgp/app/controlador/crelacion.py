from app.modelo import Relacion
from app import db

class ControlRelacion():
    """ clase control Relacion """
    def getRelacionById(self,id):
        """ funcion get Relacionbyid """
        return Relacion.query.get(id)
    def getRelaciones(self):
        """ funcion getRelacion """
        return Relacion.query.all()
    def getRelacionesByIdProyecto(self,idProyecto):
        retorno = list(db.session.query(Relacion).filter(Relacion.idProyecto == idProyecto ).all())
        return retorno
    
    def getItemsAntecesores(self,idItem):
        
        retorno = list(db.session.query(Relacion).filter(Relacion.idSucesor == idItem ).all())
        return retorno
    
    def nuevoRelacion(self, relacion):
        """ funcion nuevoRelacion """
        resultado = {"estado" : True, "mensaje" : "exito"}
        try:
            if(not self.detectarCiclo(relacion.idAntecesor, relacion.idSucesor)):
                db.session.add(relacion)
                #print "Hice el add"
                db.session.commit()
                #print "Hice el commit"
            else :
                resultado = {"estado" : False, "mensaje" : "Se formara un ciclo"}
        except Exception, error :
            #print "Capturo exp" + str(error)
            resultado = {"estado" : False, "mensaje" : str(error)}
            db.session.rollback()

        return resultado

    def eliminarRelacion(self, relacion):
        """ funcion eliminarRelacion """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un delete de usuario """
            db.session.delete(relacion)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado


    def modificarRelacion(self, relacion):
        """ funcion modificarRelacion """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un merge de Relacion """
            db.session.merge(relacion)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado


    def getRelacionByIdItemActual(self,idItem):
        """ funcion que filtra solo por las fases """
        retorno = list(db.session.query(Relacion).filter(Relacion.idAntecesor == idItem ).all())
        retorno += list(db.session.query(Relacion).filter(Relacion.idSucesor == idItem ).all())
        return retorno
    
    def getAntecesores(self,idItem):
        retorno = list(db.session.query(Relacion).filter(Relacion.idSucesor == idItem ).all())
        antecesores = []
        for r in retorno:
            antecesores.append(r.idAntecesor)
            antecesores += self.getAntecesores(r.idAntecesor)
        return antecesores
    
    def getSucesores(self,idItem):
        retorno = list(db.session.query(Relacion).filter(Relacion.idAntecesor == idItem ).all())
        sucesores = []
        for r in retorno:
            sucesores.append(r.idSucesor)
            sucesores += self.getSucesores(r.idSucesor)
        
        return sucesores
    
    def detectarCiclo(self, idAntecesor, idSucesor):
        #Se busca los sucesores del sucesor, y los 
        #antecesores del antecesor, si se encuentra alguna coincidencia
        #se retorna true
        r = False
        
        a = self.getAntecesores(idAntecesor)
        b = self.getSucesores(idSucesor)
        
        for isgte in a:
            for iant in b:
                if( isgte == iant):
                    r = True
                    break
        
        # no detecta cuando es a uno mismo
        # entonces hacemos eso aca
        if idAntecesor == idSucesor:
            r = True
        
        # tampoco detecta cuando es 
        # antecesor->sucesor     Sucesor->antecesor
        #entonces hacemos eso aca
        # si sucesor tiene un antecesor igual al antecesor
        #ciclo
      
        
        for ante in a:
            print "antecesores de 2"
            print ante
            if str(ante) == str(idSucesor):
                r = True
                break
                
                 
        
        
        return r


        

        
    
#     def eliminarRelacionPorItem(self, idItemActual):
#         import citem
#         controlItem = citem.ControlItem()
#         itemActual = controlItem.getItemById(idItemActual)
#         listaDeRelacion = self.getRelaciones()
#         for r in listaDeRelacion:
#             if (r.idAntecesor == itemActual.idItemActual or r.idSucesor == itemActual.idItemActual ):
#                 self.eliminarRelacion(r)
#                 
        
        
    
#    def buscarPorNombre(self,nombre):
#        retorno = db.session.query(Usuario).filter(Usuario.nombre.ilike("%"+nombre+"%")).all()
        #retorno = db.session.query(Usuario).filter_by(nombre=nombre).all()
#        return retorno

 