from app.modelo import HistorialItems
from app import db

class ControlHistorialItems():
    """ clase control HistorialItems """
    def getHistorialItemsById(self,id):
        """ funcion get HistorialItems """
        return HistorialItems.query.get(id)
    def getHistorialItems(self):
        """ funcion HistorialItems """
        return HistorialItems.query.all()
    def nuevoHistorialItems(self, hItem):
        """ funcion nuevoHistorialItems """
        resultado = {"estado" : True, "mensaje" : "exito"}
        try:
            db.session.add(hItem)
            #print "Hice el add"
            db.session.commit()
            #print "Hice el commit"
        except Exception, error :
            #print "Capturo exp" + str(error)
            resultado = {"estado" : False, "mensaje" : str(error)}
            db.session.rollback()

        return resultado

    def eliminarHistorialItems(self, hItem):
        """ funcion eliminarHistorialItems """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un delete de HistorialItems """
            db.session.delete(hItem)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado


    def modificarHistorialItems(self, hItem):
        """ funcion modificarHistorialItems """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un merge de HistorialItems """
            db.session.merge(hItem)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado
    