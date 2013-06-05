'''
Created on 10/04/2013

@author: cathesanz
'''
from app.modelo import Mensaje
from app import db

class ControlMensaje():
    """ clase control rol """
    def getMensajeById(self,id):
        """ funcion get rolbyid """
        return Mensaje.query.get(id)
    def getMensaje(self):
        """ funcion getrol """
        return Mensaje.query.all()
    
    def getMensajePorUsuario(self,idUsuario):
        """ funcion que filtra los roles por el id del Proyecto """
        retorno = db.session.query(Mensaje).filter(Mensaje.idUsuario == idUsuario ).all()
        return retorno
    
    
    
    def nuevoMensaje(self, mensaje1):
        """ funcion nuevoRol """
        resultado = {"estado" : True, "mensaje" : "exito"}
        try:
            db.session.add(mensaje1)
            #print "Hice el add"
            db.session.commit()
            #print "Hice el commit"
        except Exception, error :
            #print "Capturo exp" + str(error)
            resultado = {"estado" : False, "mensaje" : str(error)}
            db.session.rollback()

        return resultado

