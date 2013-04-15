'''
Created on 10/04/2013

@author: cathesanz
'''

from app import db


permisosxrol = db.Table('permisos_x_rol',
    db.Column('id', db.Integer, primary_key = True),
    db.Column('idRol', db.Integer, db.ForeignKey('rol.idRol')),
    db.Column('idPermiso', db.Integer, db.ForeignKey('permiso.idPermiso'))
)

class Rol(db.Model):
    idRol = db.Column(db.Integer, primary_key = True)
    nombre = db.Column( db.String(45), index = True, unique = True, nullable = False)
    descripcion = db.Column( db.String(100) , nullable = False)
    permisos = db.relationship('Permiso', secondary=permisosxrol,
        backref=db.backref('roles', lazy='dynamic'))
    idProyecto = db.Column(db.Integer, db.ForeignKey('proyecto.idProyecto'))
    idFase = db.Column(db.Integer, db.ForeignKey('fase.idFase'))
    #idTipoItem = db.Column(db.Integer, db.ForeignKey('tipoItem.idTipoItem'))

    def __repr__(self):
        return '<Rol %r>' % (self.nombre)
