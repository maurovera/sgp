'''
Created on 03/04/2013

@author: mauren
'''

from app import db


class TipoItem(db.Model):
    idTipoItem = db.Column(db.Integer, primary_key = True)
    nombre = db.Column( db.String(45), index = True, unique = True, nullable = False)
    codigo = db.Column( db.String(45), index = True, unique = True, nullable = False)
    descripcion = db.Column( db.String(100) , nullable = False)
    
    #roles = db.relationship('Rol', secondary=rolesxusuario,
    #    backref=db.backref('usuarios', lazy='dynamic'))
    #role = db.Column(db.SmallInteger, default = ROLE_USER)
    #posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    #Relaciones
    idProyecto = db.Column(db.Integer, db.ForeignKey('proyecto.idProyecto'))
    # se le agrega tambien un id fase fecha 02052013
    idFase = db.Column(db.Integer, db.ForeignKey('fase.idFase')) 
    #************************
    
    # Referencias a relaciones
    # se agrego esto a prueba 
    atributosPorTipoItem= db.relationship('AtributoPorTipoItem', backref='tipoItem',
                                lazy='dynamic')



    def setNombreTipoItem(self,nombre):
        self.nombreTipoItem = nombre

    def __repr__(self):
        return '<Tipo item %r>' % (self.nombre)
