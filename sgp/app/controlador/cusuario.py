from app.modelo import Usuario
from app import db

class ControlUsuario():
    def getUsuarioById(self,id):
        return Usuario.query.get(id)
    def getUsuarios(self):
        return Usuario.query.all()
    def nuevoUsuario(self, usuario):
        db.session.add(usuario)
        db.session.commit()
    def eliminarUsuario(self, usuario):
        db.session.delete(usuario)
        db.session.commit()
    def modificarUsuario(self, usuario):
        db.session.merge(usuario)
        db.session.commit()
    def comprobarLogin(self, usuario):
        retorno = db.session.query(Usuario).filter_by(nombreUsuario=usuario.nombreUsuario, contrasena=usuario.contrasena).first()
        print retorno
        return retorno
        
