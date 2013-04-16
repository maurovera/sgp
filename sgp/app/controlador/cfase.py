'''
Created on 10/04/2013

@author: cathesanz
'''
from app.modelo import Fase
from app import db

class ControlFase():
    """ clase control Fase """
    def getFaseById(self,id):
        """ funcion get proyectobyid """
        return Fase.query.get(id)
    def getFase(self):
        """ funcion getrol """
        return Fase.query.all()
    def nuevaFase(self, fase):
        """ funcion nuevoProyecto """
        resultado = {"estado" : True, "mensaje" : "exito"}
        try:
            db.session.add(fase)
            #print "Hice el add"
            db.session.commit()
            #print "Hice el commit"
        except Exception, error :
            #print "Capturo exp" + str(error)
            resultado = {"estado" : False, "mensaje" : str(error)}
            db.session.rollback()

        return resultado

    def eliminarFase(self, fase):
        """ funcion eliminarrol """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un delete de rol """
            db.session.delete(fase)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado


    def modificarFase(self, fase):
        """ funcion modificarrol """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un merge de rol """
            db.session.merge(fase)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado




    def buscarPorNombre(self,nombre):
        retorno = db.session.query(Fase).filter(Fase.nombre.ilike("%"+nombre+"%")).all()
        #retorno = db.session.query(rol).filter_by(nombre=nombre).all()
        return retorno