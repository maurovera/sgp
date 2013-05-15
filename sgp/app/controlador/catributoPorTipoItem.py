'''
Created on 01/05/2013

@author: cathesanz
'''
from app.modelo import AtributoPorTipoItem
from app import db

class ControlAtributoPorTipoItem():
    """ clase control Fase """
    def getAtributoPorTipoItemById(self,id):
        """ funcion get proyectobyid """
        return AtributoPorTipoItem.query.get(id)
    def getAtributoPorTipoItem(self):
        """ funcion getrol """
        return AtributoPorTipoItem.query.all()
    
    def getAtributoPorTipoItemByTipoItem(self,idTipoItem):
        """ funcion que filtra solo por las fases """
        retorno = db.session.query(AtributoPorTipoItem).filter(AtributoPorTipoItem.idTipoItem == idTipoItem ).all()
        return retorno
    
    def nuevaAtributoPorTipoItem(self, atributoPorTipoItem):
        """ funcion nuevoProyecto """
        resultado = {"estado" : True, "mensaje" : "exito"}
        try:
            db.session.add(atributoPorTipoItem)
            #print "Hice el add"
            db.session.commit()
            #print "Hice el commit"
        except Exception, error :
            #print "Capturo exp" + str(error)
            resultado = {"estado" : False, "mensaje" : str(error)}
            db.session.rollback()

        return resultado

    def eliminarAtributoPorTipoItem(self, atributoPorTipoItem):
        """ funcion eliminarrol """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un delete de rol """
            db.session.delete(atributoPorTipoItem)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado


    def modificarAtributoPorTipoItem(self, atributoPorTipoItem):
        """ funcion modificarrol """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un merge de rol """
            db.session.merge(atributoPorTipoItem)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado




    def buscarPorNombre(self,nombre):
        retorno = db.session.query(AtributoPorTipoItem).filter(AtributoPorTipoItem.nombre.ilike("%"+nombre+"%")).all()
        #retorno = db.session.query(rol).filter_by(nombre=nombre).all()
        return retorno