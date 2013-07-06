'''
Created on 03/04/2013

@author: mauren
'''

from app import db




class Item(db.Model):
    idItemActual = db.Column(db.Integer, primary_key = True)
    nombreItemActual =  db.Column( db.String(45), index = True, nullable = False)
    numero = db.Column(db.Integer, nullable=False)
    eliminado = db.Column(db.Boolean)
    ultimaVersion = db.Column( db.Integer, nullable = False)
        
    

    #Relaciones
    idFase = db.Column(db.Integer, db.ForeignKey('fase.idFase'))
    idTipoItem = db.Column(db.Integer, db.ForeignKey('tipo_item.idTipoItem'))
    datos = db.relationship('DatosItem', backref='item',
                                lazy='dynamic')




    # def setNombreTipoItem(self,nombre):
    #     self.nombre = nombre

    def __repr__(self):
         return '<item %r>' % (self.nombreItemActual)