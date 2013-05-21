import unittest  
import os
from app import db
from app.controlador import ControlRelacion
from app.modelo import Relacion


basedir = os.path.abspath(os.path.dirname(__file__))


# idRelacion = db.Column(db.Integer, primary_key = True)
#     tipo = db.Column( db.String(45), index = True, nullable = False)


class TestesRelacion(unittest.TestCase):  
        def setUp(self):
            self.controlador = ControlRelacion()
            self.Principal = Relacion(tipo="Antecesor-Sucesor" , idSucesor=1,  idAntecesor=2)
            self.Distinto = Relacion(tipo="Antecesor-Sucesor" , idSucesor=1000,  idAntecesor=2000)
            self.Igual = Relacion(tipo="Antecesor-Sucesor" , idSucesor=1,  idAntecesor=2)
            self.contador = 0
      
        def testGuarda(self):  
            r = self.controlador.nuevoRelacion(self.Principal)
            print "Creamos una relacion en test Guarda:  " + str(self.Principal.idSucesor)
            self.assertEqual(r["estado"], True )  #modifiq este cambiar 
            self.contador = 1
            
        def testGuardaRepetido(self):
            print "Creamos una relacion en Guarda Repetido: " + str(self.Principal.idSucesor)
            r = self.controlador.nuevoRelacion(self.Principal)
            self.assertEqual(r["estado"], True )#modifiq este cambiar 
            print "Creamos una relacion igual en guarda repetido: " + str(self.Igual.idSucesor) 
            r = self.controlador.nuevoRelacion(self.Igual)
            self.assertEqual(r["estado"], True) #modifiq este cambiar 
            print "No deberia guardar porque son iguales" 
            self.contador = 2
             
        def testGuardarDistinto(self):
            print "Creamos una relacion principal en guarda distinto  " + str(self.Principal.idSucesor)
            r = self.controlador.nuevoRelacion(self.Principal)
            self.assertEqual(r["estado"], True )#este
            print "Creamos una relacion distinta en guarda distinto " + str(self.Distinto.idSucesor)
            r = self.controlador.nuevoRelacion(self.Distinto)
            self.assertEqual(r["estado"], False ) # este
            print "Se guardan ambos con exito"
            self.contador = 3
            
        def tearDown(self):  
            if self.contador == 1 :
                print "Eliminamos la relacion principal " + str(self.Principal.idSucesor)
                self.controlador.eliminarRelacion(self.Principal)
            if self.contador == 2 :
                print "Eliminamos la relacion principal 2 " + str(self.Principal.idSucesor)
                self.controlador.eliminarRelacion(self.Principal)
            if self.contador == 3 :
                print "Eliminamos la relacion principal 3 " + str(self.Principal.idSucesor)
                self.controlador.eliminarRelacion(self.Principal)
                print "Eliminamos la relacion distinta   " + str(self.Distinto.idSucesor)
                self.controlador.eliminarRelacion(self.Distinto)