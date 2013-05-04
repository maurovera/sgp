'''
Created on 03/05/2013

@author: Mauro
'''

from app.modelo import Item
from app import db

class ControlItem():
    """ clase control  item """
    def getItemById(self,id):
        """ funcion getItembyid """
        return Item.query.get(id)
    def getItems(self):
        """ funcion getItems """
        return Item.query.all()
    def getItemByFase(self,idFase):
        """ funcion que filtra solo por las fases """
        retorno = db.session.query(Item).filter(Item.idFase == idFase ).all()
        return retorno
    def nuevoItem(self, item):
        """ funcion nuevoItem """
        resultado = {"estado" : True, "mensaje" : "exito"}
        try:
            db.session.add(item)
            #print "Hice el add"
            db.session.commit()
            #print "Hice el commit"
        except Exception, error :
            #print "Capturo exp" + str(error)
            resultado = {"estado" : False, "mensaje" : str(error)}
            db.session.rollback()

        return resultado

    def eliminarItem(self, item):
        """ funcion eliminarItem """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
#           db.session.delete(item)
#            db.session.commit()
#---------------------------------------
            """ hacemos un delete de item, que lo unico que cambia sera su eliminado """
            item.eliminado = True
            db.session.merge(item)
            """ se comitea el cambio """
            db.session.commit()

#----------------------------------------        
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()
            
            

        return resultado


    def modificarItem(self, item):
        """ funcion modificarUsuario """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un merge de usuario """
            db.session.merge(item)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado


#    def getItemByIdItemActual(self,idItemActual):
        
#        retorno = db.session.query(Item).filter(Item.idItemActual == idItemActual ).all()
#        return retorno
#-------- 03052013-------------------
# luego se agrega los atributos por tipo item 

    def agregarDatosItem(self,item,datosItem):
        ''' agrega datos al item '''
        nohay = True
        for f in item.datos:
            if(datosItem == f):
                print "YA HAY eSte dato item"
                nohay = False

        if (nohay):
            print "Agregamos!"
            item.datos.append(datosItem)
            return self.modificarItem(item)
        else :
            resultado = {"estado" : False, "mensaje" : "El item ya posee estos datos"}
            return resultado

    def quitarDatosItem(self,item,datosItem):
        ''' quitar datos  '''
        item.datos.remove(datosItem)
        return self.modificarItem(item)
    
    