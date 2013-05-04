'''
Created on 03/04/2013

@author: mauren
'''

from app import db



class AtributoDeItem(db.Model):
    idAtributosDeItem = db.Column(db.Integer, primary_key = True)
    valorPorDefecto = db.Column( db.String(100) , nullable = False)

    #Relaciones
    idAtributoPorTipoItem = db.Column(db.Integer, db.ForeignKey('atributo_por_tipo_item.idAtributosPorTipoItem'))





    # def setNombreTipoItem(self,nombre):
    #     self.nombre = nombre

    # def __repr__(self):
    #     return '<Atributo por Tipo item %r>' % (self.nombre)