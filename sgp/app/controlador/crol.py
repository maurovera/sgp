'''
Created on 10/04/2013

@author: cathesanz
'''
from app.modelo import Rol
from app import db

class ControlRol():
    """ clase control rol """
    def getRolById(self,id):
        """ funcion get rolbyid """
        return Rol.query.get(id)
    def getRoles(self):
        """ funcion getrol """
        return Rol.query.all()
    def nuevoRol(self, rol):
        """ funcion nuevoRol """
        resultado = {"estado" : True, "mensaje" : "exito"}
        try:
            db.session.add(rol)
            #print "Hice el add"
            db.session.commit()
            #print "Hice el commit"
        except Exception, error :
            #print "Capturo exp" + str(error)
            resultado = {"estado" : False, "mensaje" : str(error)}
            db.session.rollback()

        return resultado

    def eliminarRol(self, rol):
        """ funcion eliminarrol """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un delete de rol """
            db.session.delete(rol)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado


    def modificarRol(self, rol):
        """ funcion modificarrol """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un merge de rol """
            db.session.merge(rol)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado




    def buscarPorNombre(self,nombre):
        retorno = db.session.query(Rol).filter(Rol.nombre.ilike("%"+nombre+"%")).all()
        #retorno = db.session.query(rol).filter_by(nombre=nombre).all()
        return retorno

