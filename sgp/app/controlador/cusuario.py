from app.modelo import Usuario
from app import db

class ControlUsuario():
    """ clase control usuario """
    def getUsuarioById(self,id):
        """ funcion get usuariobyid """
        return Usuario.query.get(id)
    def getUsuarios(self):
        """ funcion getusuario """
        return Usuario.query.all()
    def nuevoUsuario(self, usuario):
        """ funcion nuevoUsuario """
        resultado = {"estado" : True, "mensaje" : "exito"}
        try:
            db.session.add(usuario)
            #print "Hice el add"
            db.session.commit()
            #print "Hice el commit"
        except Exception, error :
            #print "Capturo exp" + str(error)
            resultado = {"estado" : False, "mensaje" : str(error)}
            db.session.rollback()
        
        return resultado
            
    def eliminarUsuario(self, usuario):
        """ funcion eliminarUsuario """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un delete de usuario """
            db.session.delete(usuario)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()
        
        return resultado
    
        
    def modificarUsuario(self, usuario):
        """ funcion modificarUsuario """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un merge de usuario """
            db.session.merge(usuario)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()
        
        return resultado
    
    
    
    def comprobarLogin(self, usuario):
        """ funcion comprobar usuario """
        retorno = db.session.query(Usuario).filter_by(nombreUsuario=usuario.nombreUsuario, contrasena=usuario.contrasena).first()
        print retorno
        return retorno
        
