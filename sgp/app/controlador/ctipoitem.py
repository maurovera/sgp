from app.modelo import TipoItem
from app import db

class ControlTipoItem():
    """ clase control tipo item """
    def getTipoItemById(self,id):
        """ funcion get TipoItembyid """
        return TipoItem.query.get(id)
    def getTipoItems(self):
        """ funcion getTipoItem """
        return TipoItem.query.all()
    def nuevoTipoItem(self, tipoItem):
        """ funcion nuevoTipoItem """
        resultado = {"estado" : True, "mensaje" : "exito"}
        try:
            db.session.add(tipoItem)
            #print "Hice el add"
            db.session.commit()
            #print "Hice el commit"
        except Exception, error :
            #print "Capturo exp" + str(error)
            resultado = {"estado" : False, "mensaje" : str(error)}
            db.session.rollback()

        return resultado

    def eliminarTipoItem(self, tipoItem):
        """ funcion eliminarTipoItem """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un delete de tipoItem """
            db.session.delete(tipoItem)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado


    def modificarTipoItem(self, tipoItem):
        """ funcion modificarUsuario """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un merge de usuario """
            db.session.merge(tipoItem)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado



    def buscarPorNombre(self,nombre):
        retorno = db.session.query(TipoItem).filter(TipoItem.nombre.ilike("%"+nombre+"%")).all()
        #retorno = db.session.query(Usuario).filter_by(nombre=nombre).all()
        return retorno

