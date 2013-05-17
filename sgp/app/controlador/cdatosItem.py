'''
Created on 03/05/2013

@author: mauro
'''
from app.modelo import DatosItem
from app import db

class ControlDatosItem():
    """ clase control datosItem """
    def getDatosItemById(self,id):
        """ funcion get proyectobyid """
        return DatosItem.query.get(id)
    def getDatosItem(self):
        """ funcion getDatosItem """
        return DatosItem.query.all()
    def nuevaDatosItem(self, datosItem):
        """ funcion nuevodatosItem """
        resultado = {"estado" : True, "mensaje" : "exito"}
        try:
            db.session.add(datosItem)
            #print "Hice el add"
            db.session.commit()
            #print "Hice el commit"
        except Exception, error :
            #print "Capturo exp" + str(error)
            resultado = {"estado" : False, "mensaje" : str(error)}
            db.session.rollback()

        return resultado

    def eliminarDatosItem(self, datosItem):
        """ funcion eliminar datos de item """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un delete de datos item """
            db.session.delete(datosItem)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado


    def modificarDatosItem(self, datosItem):
        """ funcion modificarDatosItem """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un merge de DatosItem """
            db.session.merge(datosItem)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado
    def agregarAtributoDeItem(self,item,atributo):
        nohay = True
        for a in item.atributosDeItem :
            if(atributo == a):
                print "YA HAY ESTE! ATRIBUTO"
                nohay = False

        if (nohay):
            print "Agregamos!"
            item.atributosDeItem.append(atributo)
            return self.modificarDatosItem(item)
        else :
            resultado = {"estado" : False, "mensaje" : "El rol ya posee este permiso"}
            return resultado


#
#    def buscarPorNombre(self,nombre):
#       retorno = db.session.query(AtributoPorTipoItem).filter(AtributoPorTipoItem.nombre.ilike("%"+nombre+"%")).all()
#        #retorno = db.session.query(rol).filter_by(nombre=nombre).all()
#        return retorno



