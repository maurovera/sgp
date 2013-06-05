'''
Created on 21/05/2013

@author: mauren
'''

from app import db



class SolicitudDeCambio(db.Model):
    idSolicitud = db.Column(db.Integer, primary_key = True)
    nombreSolicitud = db.Column( db.String(45), index = True, nullable = False)
    descripcion = db.Column( db.String(160) , nullable = False)
    estado = db.Column( db.String(45) )
    costo = db.Column( db.Integer )
    impacto = db.Column( db.Integer )
    
    idItem = db.Column(db.Integer, db.ForeignKey('item.idItemActual'))
    accionSol = db.Column( db.String(45) , nullable = False)
    
    cantidadVotos = db.Column( db.Integer , nullable = False)
    votoPositivo =  db.Column( db.Integer , nullable = False)
    votoNegativo = db.Column( db.Integer , nullable = False)


    def setnombreSolicitud(self,nombre):
        self.nombreUsuario = nombre

    def __repr__(self):
        return '<SolcitudDeCambio %r>' % (self.nombreSolicitud)
