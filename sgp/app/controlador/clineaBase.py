from app.modelo import LineaBase
from app import db

class ControlLineaBase():
    """ clase control linea base """
    def getLineaBaseById(self,idLB):
        """ funcion get lb_by_id """
        return LineaBase.query.get(idLB)
    def getLineaBase(self):
        """ funcion get_lb """
        return LineaBase.query.all()
    def nuevaLineaBase(self, lineaBase):
        """ funcion nueva_lb """
        resultado = {"estado" : True, "mensaje" : "exito"}
        try:
            db.session.add(lineaBase)
            #print "Hice el add"
            db.session.commit()
            #print "Hice el commit"
        except Exception, error :
            #print "Capturo exp" + str(error)
            resultado = {"estado" : False, "mensaje" : str(error)}
            db.session.rollback()

        return resultado

    def eliminarLineaBase(self, lineaBase):
        """ funcion eliminarLinea base """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un delete de lb """
            db.session.delete(lineaBase)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado


    def modificarLineaBase(self, lineaBase):
        """ funcion modificar LB """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un merge de usuario """
            db.session.merge(lineaBase)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado


    def buscarPorIdLB(self,idLB):
        id = int(idLB)
        print id
        retorno = db.session.query(LineaBase).filter(LineaBase.idLB == id ).all()
        #retorno = db.session.query(Usuario).filter_by(nombre=nombre).all()
        print retorno
        return retorno
    
    def getLBByFase(self,idFase):
        """ funcion que filtra solo por las fases """
        retorno = db.session.query(LineaBase).filter(LineaBase.idFase == idFase ).all()
        return retorno
    