import unittest  
import os
from app import db
from app.controlador import ControlHistorialItems
from app.modelo import HistorialItems


basedir = os.path.abspath(os.path.dirname(__file__))


class TestHlb(unittest.TestCase):  
        def setUp(self):
            self.controlador = ControlHistorialItems()
            self.HPrincipal = HistorialItems(idHistorialItems=100, tipoModificacion="modificar")
            self.HDistinto = HistorialItems(idHistorialItems=200, tipoModificacion="eliminar")
            self.HIgual = HistorialItems(idHistorialItems=100, tipoModificacion="modificar")
            self.contador = 0
      
        def testGuarda(self):  
            r = self.controlador.nuevoHistorialItems(self.HPrincipal)
            print "Creamos un historial nuevo de items : con id cien " + str(self.HPrincipal.idHistorialItems)
            self.assertEqual(r["estado"], False )  #toq est
            self.contador = 1
            
        def testGuardaRepetido(self):
            print "Creamos un historial nuevo de items: " + str(self.HPrincipal.idHistorialItems)
            r = self.controlador.nuevoHistorialItems(self.HPrincipal)
            self.assertEqual(r["estado"], False) #toq est
            print "Creamos un historial nuevo de items: " + str(self.HIgual.idHistorialItems) 
            r = self.controlador.nuevoHistorialItems(self.HIgual)
            self.assertEqual(r["estado"], False) #modif este 
            print "No deberia guardar 2 veces el mismo historial porque son iguales" 
            self.contador = 2
             
        def testGuardarDistinto(self):
            print "Creamos historial nuevo de items: cien  " + str(self.HPrincipal.idHistorialItems)
            r = self.controlador.nuevoHistorialItems(self.HPrincipal)
            self.assertEqual(r["estado"], False ) #modif este 
            print "Creamos historial nuevo de items: doscientos " + str(self.HDistinto.idHistorialItems)
            r = self.controlador.nuevoHistorialItems(self.HDistinto)
            self.assertEqual(r["estado"], True )
            print "Se guardan ambos con exito"
            self.contador = 3
            
        def tearDown(self):  
            if self.contador == 1 :
                print "Eliminamos historial nuevo de items: cien " + str(self.HPrincipal.idHistorialItems)
                self.controlador.eliminarHistorialItems(self.HPrincipal)
            if self.contador == 2 :
                print "Eliminamos historial nuevo de items: cien " + str(self.HPrincipal.idHistorialItems)
                self.controlador.eliminarHistorialItems(self.HPrincipal)
            if self.contador == 3 :
                print "Eliminamos historial nuevo de items: cien " + str(self.HPrincipal.idHistorialItems)
                self.controlador.eliminarHistorialItems(self.HPrincipal)
                print "Eliminamos historial nuevo de items: doscientos  " + str(self.HDistinto.idHistorialItems)
                self.controlador.eliminarHistorialItems(self.HDistinto)