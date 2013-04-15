'''
Created on 10/04/2013

@author: cathesanz
'''

from app import db

class Permiso(db.Model):
    idPermiso = db.Column(db.Integer, primary_key = True)
    nombre = db.Column( db.String(45), index = True, unique = True, nullable = False)
    valor = db.Column(db.Integer, nullable = False)


    def __repr__(self):
        return '<Permiso %r>' % (self.nombre)
