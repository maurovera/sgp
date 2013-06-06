from app.modelo import SolicitudDeCambio
from app.modelo import Item

from app import db

class ControlSolicitud():
    """ clase control sol """
    def getSolicitudById(self,idSol):
        """ funcion get solbyid """
        return SolicitudDeCambio.query.get(idSol)
    def getSolicitudes(self):
        """ funcion getsol """
        return SolicitudDeCambio.query.all()
    def nuevaSolicitud(self, solicitud):
        """ funcion nuevosol """
        resultado = {"estado" : True, "mensaje" : "exito"}
        try:
            db.session.add(solicitud)
            #print "Hice el add"
            db.session.commit()
            #print "Hice el commit"
        except Exception, error :
            #print "Capturo exp" + str(error)
            resultado = {"estado" : False, "mensaje" : str(error)}
            db.session.rollback()

        return resultado

    def eliminarSolicitud(self, solicitud):
        """ funcion eliminarSol """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un delete de sol """
            db.session.delete(solicitud)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado


    def modificarSolicitud(self, solicitud):
        """ funcion modificarsol """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un merge de solicitud """
            db.session.merge(solicitud)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado

    def buscarPorNombre(self,nombre):
        retorno = db.session.query(SolicitudDeCambio).filter(SolicitudDeCambio.nombreSolicitud.ilike("%"+nombre+"%")).all()
        return retorno

