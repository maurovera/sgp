from app.modelo import HistorialLineaBase
from app import db

class ControlHistorialLineaBase():
    """ clase control HistorialLineaBase """
    def getHistorialLineaBaseById(self,id):
        """ funcion get HistorialLineaBasebyid """
        return HistorialLineaBase.query.get(id)
    def getHistorialLineaBase(self):
        """ funcion getHistorialLineaBase """
        return HistorialLineaBase.query.all()
    def nuevoHistorialLineaBase(self, hLB):
        """ funcion nuevoHistorialLineaBase """
        resultado = {"estado" : True, "mensaje" : "exito"}
        try:
            db.session.add(hLB)
            #print "Hice el add"
            db.session.commit()
            #print "Hice el commit"
        except Exception, error :
            #print "Capturo exp" + str(error)
            resultado = {"estado" : False, "mensaje" : str(error)}
            db.session.rollback()

        return resultado

    def eliminarHistorialLineaBase(self, hLB):
        """ funcion eliminarHistorialLineaBase """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un delete de HistorialLineaBase """
            db.session.delete(hLB)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado


    def modificarHistorialLineaBase(self, hLB):
        """ funcion modificarHistorialLineaBase """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un merge de HistorialLineaBase """
            db.session.merge(hLB)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado