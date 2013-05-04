'''
Created on 03/04/2013

@author: mauren
'''

from app import db



class AtributoPorTipoItem(db.Model):
    idAtributosPorTipoItem = db.Column(db.Integer, primary_key = True)
    nombre = db.Column( db.String(45), index = True, unique = True, nullable = False)
    tipo = db.Column( db.String(45), index = True, nullable = False)
    valorPorDefecto = db.Column( db.String(45) , nullable = False)

    #Relaciones
    idTipoItem = db.Column(db.Integer, db.ForeignKey('tipo_item.idTipoItem'))





    def setNombreTipoItem(self,nombre):
        self.nombre = nombre

    def __repr__(self):
        return '<Atributo por Tipo item %r>' % (self.nombre)