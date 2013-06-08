'''
Created on 01/05/2013

@author: mauren
'''

from app import db

 



class LineaBase(db.Model):
    idLB = db.Column(db.Integer, primary_key = True)
    numero = db.Column( db.Integer)
    estado = db.Column(db.Integer)
    idFase=  db.Column(db.Integer, db.ForeignKey('fase.idFase'))
    idUsuario = db.Column(db.Integer)

    #def setNombreLineaBase(self,nombre):
         #self.nombre = nombre

    #def __repr__(self):
         #return '<Nombre Archivo Adjunto %r>' % (self.nombre)