'''
Created on 10/04/2013

@author: cathesanz
'''
from app.modelo import Rol
from app import db
from cproyecto import ControlProyecto
class ControlRol():
    """ clase control rol """
    def getRolById(self,id):
        """ funcion get rolbyid """
        return Rol.query.get(id)
    def getRoles(self):
        """ funcion getrol """
        return Rol.query.all()
    def nuevoRol(self, rol):
        """ funcion nuevoRol """
        resultado = {"estado" : True, "mensaje" : "exito"}
        try:
            db.session.add(rol)
            #print "Hice el add"
            db.session.commit()
            #print "Hice el commit"
        except Exception, error :
            #print "Capturo exp" + str(error)
            resultado = {"estado" : False, "mensaje" : str(error)}
            db.session.rollback()

        return resultado

    def eliminarRol(self, rol):
        """ funcion eliminarrol """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """Comprobamos que el rol no tenga asociado un proyecto"""
            if (rol.idProyecto ):
                cp = ControlProyecto()
                p = cp.getProyectoById(rol.idProyecto)
                if(not p.estado == "eliminado"):
                    """Si esta asociado pasamos avisamos que no es posible eliminar"""
                    resultado = {"estado" : False, "mensaje" : "No se puede eliminar un rol asociado a un proyecto no eliminado"}
                    return resultado
            """ hacemos un delete de rol """
            db.session.delete(rol)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado


    def modificarRol(self, rol):
        """ funcion modificarrol """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un merge de rol """
            db.session.merge(rol)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado




    def buscarPorNombre(self,nombre):
        retorno = db.session.query(Rol).filter(Rol.nombre.ilike("%"+nombre+"%")).all()
        #retorno = db.session.query(rol).filter_by(nombre=nombre).all()
        return retorno

    def permisosPorRol(self,rol):
        return list(rol.permisos)

    def quitarPermiso(self,rol,permiso):
        rol.permisos.remove(permiso)
        return self.modificarRol(rol)

    def agregarPermiso(self,rol,permiso):
        nohay = True
        for p in rol.permisos :
            if(permiso == p):
                print "YA HAY ESTE! PERMISO"
                nohay = False

        if (nohay):
            print "Agregamos!"
            rol.permisos.append(permiso)
            return self.modificarRol(rol)
        else :
            resultado = {"estado" : False, "mensaje" : "El rol ya posee este permiso"}
            return resultado
    
    def getRolByIdProyecto(self,idProyecto):
        lista = self.getRoles()
        for r in lista :
            print str(r.idProyecto) + " - " + idProyecto
            if str(r.idProyecto) == str(idProyecto) :
                print "--------ENTRO Y RETORNA EL PROYECTO " + r.nombre
                return r
        
        