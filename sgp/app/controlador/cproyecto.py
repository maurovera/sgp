'''
Created on 10/04/2013

@author: cathesanz
'''
from app.modelo import Proyecto
from app import db

class ControlProyecto():
    """ clase control Proyecto """
    def getProyectoById(self,id):
        """ funcion get proyectobyid """
        return Proyecto.query.get(id)
    def getProyectos(self):
        """ funcion getrol """
        return Proyecto.query.all()
    def nuevoProyecto(self, proyecto):
        """ funcion nuevoProyecto """
        resultado = {"estado" : True, "mensaje" : "exito"}
        try:
            db.session.add(proyecto)
            #print "Hice el add"
            db.session.commit()
            #print "Hice el commit"
        except Exception, error :
            #print "Capturo exp" + str(error)
            resultado = {"estado" : False, "mensaje" : str(error)}
            db.session.rollback()

        return resultado

    def eliminarProyecto(self, proyecto):
        """ funcion eliminarrol """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un delete de rol """
            proyecto.estado = 'eliminado'
            db.session.merge(proyecto)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado


    def modificarProyecto(self, proyecto):
        """ funcion modificarrol """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un merge de rol """
            db.session.merge(proyecto)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado




    def buscarPorNombre(self,nombre):
        retorno = db.session.query(Proyecto).filter(Proyecto.nombre.ilike("%"+nombre+"%")).all()
        #retorno = db.session.query(rol).filter_by(nombre=nombre).all()
        return retorno

    def agregarFase(self,proyecto,fase):
        nohay = True
        for f in proyecto.fases :
            if(fase == f):
                print "YA HAY ESTA FASE"
                nohay = False

        if (nohay):
            print "Agregamos!"
            proyecto.fases.append(fase)
            return self.modificarProyecto(proyecto)
        else :
            resultado = {"estado" : False, "mensaje" : "El proyecto ya posee esa fase"}
            return resultado

    def quitarFase(self,proyecto,fase):
        proyecto.fases.remove(fase)
        return self.modificarProyecto(proyecto)
    
    
    
    