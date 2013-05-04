'''
Created on 01/05/2013

@author: mauren
'''

from app import db



class ArchivosAdjuntosItem(db.Model):
    idArchivosPorItem = db.Column(db.Integer, primary_key = True)
    nombreFichero = db.Column( db.String(45), index = True, unique = True, nullable = False)
    fichero = db.Column(db.Binary)
    #corroborar si un archivo binario se representa asi 
    #Relaciones
    
    idItem = db.Column(db.Integer, db.ForeignKey('datos_item.idItem'))




    def setNombreArchivosAjuntosItem(self,nombre):
         self.nombre = nombre

    def __repr__(self):
         return '<Nombre Archivo Adjunto %r>' % (self.nombre)