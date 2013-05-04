'''
Created on 01/05/2013

@author: mauren
'''

from app import db



class HistorialItems(db.Model):
    idHistorialItems = db.Column(db.Integer, primary_key = True)
    tipoModificacion = db.Column( db.String(45), nullable = False)
    fechaModificacion = db.Column(db.Date)

    #Relaciones
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'))
    idItem = db.Column(db.Integer, db.ForeignKey('datos_item.idItem'))




    # def setNombreTipoItem(self,nombre):
    #     self.nombre = nombre

    # def __repr__(self):
    #     return '<Tipo item %r>' % (self.nombre)