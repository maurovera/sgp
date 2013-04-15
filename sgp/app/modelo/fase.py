'''
Created on 10/04/2013

@author: cathesanz
'''

from app import db

class Fase(db.Model):
    idFase = db.Column(db.Integer, primary_key = True)
    nombre = db.Column( db.String(45), index = True, unique = True, nullable = False)
    descripcion = db.Column( db.String(100) , nullable = False)
    estado = db.Column(db.String(45))

    #Relaciones
    idProyecto = db.Column(db.Integer, db.ForeignKey('proyecto.idProyecto'))

    #Referencia a Relaciones

    def __repr__(self):
        return '<Fase %r>' % (self.nombre)
