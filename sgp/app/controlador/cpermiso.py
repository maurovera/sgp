'''
Created on 10/04/2013

@author: cathesanz
'''
from app.modelo import Permiso
from app import db

class ControlPermiso():
    """ clase control rol """
    def getPermisoById(self,id):
        """ funcion get rolbyid """
        return Permiso.query.get(id)
    def getPermisos(self):
        """ funcion getrol """
        return Permiso.query.all()
    def nuevoPermiso(self, permiso):
        """ funcion nuevoRol """
        resultado = {"estado" : True, "mensaje" : "exito"}
        try:
            db.session.add(permiso)
            #print "Hice el add"
            db.session.commit()
            #print "Hice el commit"
        except Exception, error :
            #print "Capturo exp" + str(error)
            resultado = {"estado" : False, "mensaje" : str(error)}
            db.session.rollback()

        return resultado

    def eliminarPermiso(self, permiso):
        """ funcion eliminarrol """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un delete de rol """
            db.session.delete(permiso)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado


    def modificarPermiso(self, permiso):
        """ funcion modificarrol """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un merge de rol """
            db.session.merge(permiso)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado




    def buscarPorNombre(self,nombre):
        retorno = db.session.query(Permiso).filter(Permiso.nombre.ilike("%"+nombre+"%")).all()
        #retorno = db.session.query(rol).filter_by(nombre=nombre).all()
        return retorno

    def buscarPorValor(self,valor):
        retorno = db.session.query(Permiso).filter(Permiso.valor == valor).first()

        return retorno