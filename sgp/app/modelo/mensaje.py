'''
Created on 21/05/2013

@author: mauren
'''

from app import db



class Mensaje(db.Model):
    idMensaje = db.Column(db.Integer, primary_key = True)
    titulo = db.Column( db.String(150) , nullable = False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'))
    cuerpo = db.Column( db.String(500) , nullable = False)
    fecha = db.Column(db.Date)
    estado = db.Column(db.String(45), nullable = False)


    def __repr__(self):
        return '<Mensaje %r>' % (self.titulo)