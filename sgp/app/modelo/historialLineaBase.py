'''
Created on 01/05/2013

@author: mauren
'''

from app import db



class HistorialLineaBase(db.Model):
    idHistorialLB = db.Column(db.Integer, primary_key = True)
    tipoOperacion = db.Column( db.String(45), nullable = False)
    fechaModificacion = db.Column(db.Date)

    #Relaciones
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'))
    idLB = db.Column(db.Integer, db.ForeignKey('linea_base.idLB'))




    # def setNombreTipoItem(self,nombre):
    #     self.nombre = nombre

    # def __repr__(self):
    #     return '<Tipo item %r>' % (self.nombre)