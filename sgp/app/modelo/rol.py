'''
Created on 10/04/2013

@author: cathesanz
'''

from app import db

class Rol(db.Model):
    idRol = db.Column(db.Integer, primary_key = True)
    nombre = db.Column( db.String(45), index = True, unique = True, nullable = False)
    descripcion = db.Column( db.String(100) , nullable = False)
        

    def __repr__(self):
        return '<Rol %r>' % (self.nombre)
