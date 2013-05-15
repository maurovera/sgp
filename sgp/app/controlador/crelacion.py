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
    def nuevoRelacion(self, relacion):
        """ funcion nuevoRelacion """
        resultado = {"estado" : True, "mensaje" : "exito"}
        try:
            db.session.add(relacion)
            #print "Hice el add"
            db.session.commit()
            #print "Hice el commit"
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



   
#    def buscarPorNombre(self,nombre):
#        retorno = db.session.query(Usuario).filter(Usuario.nombre.ilike("%"+nombre+"%")).all()
        #retorno = db.session.query(Usuario).filter_by(nombre=nombre).all()
#        return retorno

 