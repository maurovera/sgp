'''
Created on 01/05/2013

@author: mauren
'''

from app import db



class AtributosPorItem(db.Model):
    idAtributosPorItem = db.Column(db.Integer, primary_key = True)
    
    
    #Relaciones
    idAtributosDeItem = db.Column(db.Integer, db.ForeignKey('atributo_de_item.idAtributosDeItem'))
    idItem = db.Column(db.Integer, db.ForeignKey('datos_item.idItem'))


    # def setNombreTipoItem(self,nombre):
    #     self.nombre = nombre

    # def __repr__(self):
    #     return '<Tipo item %r>' % (self.nombre)