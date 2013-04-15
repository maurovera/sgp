'''
Created on 10/04/2013

@author: cathesanz
'''

from app import db



class Proyecto(db.Model):
    idProyecto = db.Column(db.Integer, primary_key = True)
    nombre = db.Column( db.String(45), index = True, unique = True, nullable = False)
    descripcion = db.Column( db.String(100) , nullable = False)
    fechaCreacion = db.Column(db.Date)
    complejidadTotal = db.Column(db.Integer)
    estado = db.Column(db.String(45))

    # Referencias a relaciones
    fases = db.relationship('Fase', backref='proyecto',
                                lazy='dynamic')


    def __repr__(self):
        return '<Proyecto %r>' % (self.nombre)
