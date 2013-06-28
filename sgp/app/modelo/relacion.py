'''
Created on 01/05/2013

@author: mauren
'''

from app import db



class Relacion(db.Model):
    idRelacion = db.Column(db.Integer, primary_key = True)
    tipo = db.Column( db.String(45), index = True, nullable = False)

    #corroborar si un archivo binario se representa asi 
    #Relaciones
    
    idSucesor = db.Column(db.Integer, db.ForeignKey('item.idItemActual'))
    idAntecesor = db.Column(db.Integer, db.ForeignKey('item.idItemActual'))
    idProyecto = db.Column(db.Integer, db.ForeignKey('proyecto.idProyecto'))
    idFase = db.Column(db.Integer, db.ForeignKey('fase.idFase'))


    #def setNombreArchivosAjuntosItem(self,nombre):
         #self.nombre = nombre

    #def __repr__(self):
         #return '<Nombre Archivo Adjunto %r>' % (self.nombre)