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
        db.session.add(usuario)
        db.session.commit()
    def eliminarUsuario(self, usuario):
        """ funcion eliminarUsuario """
        db.session.delete(usuario)
        db.session.commit()
    def modificarUsuario(self, usuario):
        """ funcion modificarUsuario """
        db.session.merge(usuario)
        db.session.commit()
    def comprobarLogin(self, usuario):
        """ funcion comprobar usuario """
        retorno = db.session.query(Usuario).filter_by(nombreUsuario=usuario.nombreUsuario, contrasena=usuario.contrasena).first()
        print retorno
        return retorno
        
