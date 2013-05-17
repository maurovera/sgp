'''
Created on 01/05/2013

@author: cathesanz
'''
from app.modelo import AtributoDeItem
from app import db

class ControlAtributoDeItem():
    """ clase control Atributo De Item """
    def getAtributoDeItemById(self,id):
        """ funcion get proyectobyid """
        return AtributoDeItem.query.get(id)
    def getAtributoDeItem(self):
        """ funcion getrol """
        return AtributoDeItem.query.all()

    def getAtributoDeItemByTipoItem(self,idTipoItem):
        """ funcion que filtra solo por las fases """
        retorno = db.session.query(AtributoDeItem).filter(AtributoDeItem.idTipoItem == idTipoItem ).all()
        return retorno

    def nuevoAtributoDeItem(self, atributoDeItem):
        """ funcion nuevoProyecto """
        resultado = {"estado" : True, "mensaje" : "exito"}
        try:
            db.session.add(atributoDeItem)
            #print "Hice el add"
            db.session.commit()
            #print "Hice el commit"
        except Exception, error :
            #print "Capturo exp" + str(error)
            resultado = {"estado" : False, "mensaje" : str(error)}
            db.session.rollback()

        return resultado

    def eliminarAtributoDeItem(self, atributoDeItem):
        """ funcion eliminarrol """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un delete de rol """
            db.session.delete(atributoDeItem)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado


    def modificarAtributoDeItem(self, atributoDeItem):
        """ funcion modificarrol """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un merge de rol """
            db.session.merge(atributoDeItem)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado




    def buscarPorNombre(self,nombre):
        retorno = db.session.query(AtributoDeItem).filter(AtributoDeItem.nombre.ilike("%"+nombre+"%")).all()
        #retorno = db.session.query(rol).filter_by(nombre=nombre).all()
        return retorno