'''
Created on 03/04/2013

@author: mauren
'''

from app import db

rolesxusuario = db.Table('roles_x_usuario',
    db.Column('id', db.Integer, primary_key = True),
    db.Column('idUsuario', db.Integer, db.ForeignKey('usuario.idUsuario')),
    db.Column('idRol', db.Integer, db.ForeignKey('rol.idRol'))
)


class Usuario(db.Model):
    idUsuario = db.Column(db.Integer, primary_key = True)
    nombreUsuario = db.Column( db.String(45), index = True, unique = True, nullable = False)
    contrasena = db.Column( db.String(160) , nullable = False)
    nombre = db.Column( db.String(45) )
    apellido = db.Column( db.String(45) )
    telefono = db.Column( db.String(20) )
    CI = db.Column(db.Integer)
    email = db.Column(db.String(45), unique = True)
    roles = db.relationship('Rol', secondary=rolesxusuario,
        backref=db.backref('usuarios', lazy='dynamic'))
    #role = db.Column(db.SmallInteger, default = ROLE_USER)
    #posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')





    def setnombreUsuario(self,nombre):
        self.nombreUsuario = nombre

    def __repr__(self):
        return '<Usuario %r>' % (self.nombreUsuario)
