'''
Created on 03/04/2013

@author: mauren
'''

from app import db

relacionxitem = db.Table('relacion_x_item',
    db.Column('id', db.Integer, primary_key = True),
    db.Column('idItem', db.Integer, db.ForeignKey('datos_item.idItem')),
    db.Column('idRelacion', db.Integer, db.ForeignKey('relacion.idRelacion')),
    db.Column('revisar', db.Boolean)
)

atributoDeItemxitem = db.Table('atributo_de_item_x_item',
    db.Column('id', db.Integer, primary_key = True),
    db.Column('idItem', db.Integer, db.ForeignKey('datos_item.idItem')),
    db.Column('idAtributosDeItem', db.Integer, db.ForeignKey('atributo_de_item.idAtributosDeItem'))
)


itemxlineaBase = db.Table('item_x_linea_base',
    db.Column('id', db.Integer, primary_key = True),
    db.Column('idItem', db.Integer, db.ForeignKey('datos_item.idItem')),
    db.Column('idLB', db.Integer, db.ForeignKey('linea_base.idLB'))
)


class DatosItem(db.Model):
    idItem = db.Column(db.Integer, primary_key = True)
    version = db.Column( db.Integer, nullable = False)
    complejidad = db.Column(db.Integer)
    prioridad = db.Column(db.Integer)
    estado = db.Column(db.String(45))
    
    relaciones = db.relationship('Relacion', secondary=relacionxitem,
        backref=db.backref('items', lazy='dynamic'))
    
    atributosDeItem = db.relationship('AtributoDeItem', secondary=atributoDeItemxitem,
        backref=db.backref('items', lazy='dynamic'))
    
    itemLB = db.relationship('LineaBase', secondary=itemxlineaBase,
        backref=db.backref('items', lazy='dynamic'))



    #Relaciones
    #idItemActual agregado por yo. corroborar hace cliclos
    
    #idItemActual = db.Column(db.Integer, db.ForeignKey('item.idItemActual'))
        #idItemActual agregado por yo. corroborar
    idItemActual = db.Column(db.Integer, db.ForeignKey('item.idItemActual'))




#    def setNombreTipoItem(self,nombre):
 #       self.nombre = nombre

  #  def __repr__(self):
   #     return '<Tipo item %r>' % (self.nombre)