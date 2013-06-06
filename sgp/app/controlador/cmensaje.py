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
        """ funcion getMensaje """
        return Mensaje.query.order_by(Mensaje.fecha.desc()).all()

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

    def eliminarMensaje(self, mensaje):
        """ funcion eliminarItem """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
#           db.session.delete(item)
#            db.session.commit()
#---------------------------------------
            """ hacemos un delete de item, que lo unico que cambia sera su eliminado """
            db.session.delete(mensaje)
            """ se comitea el cambio """
            db.session.commit()

#----------------------------------------
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

    def modificarMensaje(self,mensaje):
        """ funcion modificarMensaje """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un merge de mensaje """
            db.session.merge(mensaje)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado
