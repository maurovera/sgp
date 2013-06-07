import unittest  
import os
from app import db
from app.controlador import ControlHistorialLineaBase
from app.modelo import HistorialLineaBase


basedir = os.path.abspath(os.path.dirname(__file__))


class TestHlb(unittest.TestCase):  
        def setUp(self):
            self.controlador = ControlHistorialLineaBase()
            self.HlbPrincipal = HistorialLineaBase(idHistorialLB=100, tipoOperacion="modificar")
            self.HlbDistinto = HistorialLineaBase(idHistorialLB=200, tipoOperacion="eliminar")
            self.HlbIgual = HistorialLineaBase(idHistorialLB=100, tipoOperacion="modificar")
            self.contador = 0
      
        def testGuarda(self):  
            r = self.controlador.nuevoHistorialLineaBase(self.HlbPrincipal)
            print "Creamos una hlb nueva: con id cien " + str(self.HlbPrincipal.idHistorialLB)
            self.assertEqual(r["estado"], False )  #toq est
            self.contador = 1
            
        def testGuardaRepetido(self):
            print "Creamos un hlb nuevo: " + str(self.HlbPrincipal.idHistorialLB)
            r = self.controlador.nuevoHistorialLineaBase(self.HlbPrincipal)
            self.assertEqual(r["estado"], False) #toq est
            print "Creamos un HLB nuevo: " + str(self.HlbIgual.idHistorialLB) 
            r = self.controlador.nuevoHistorialLineaBase(self.HlbIgual)
            self.assertEqual(r["estado"], False) #modif este 
            print "No deberia guardar 2 veces el mismo historial porque son iguales" 
            self.contador = 2
             
        def testGuardarDistinto(self):
            print "Creamos una Hlb nueva: cien  " + str(self.HlbPrincipal.idHistorialLB)
            r = self.controlador.nuevoHistorialLineaBase(self.HlbPrincipal)
            self.assertEqual(r["estado"], False ) #modif este 
            print "Creamos una Hlb nueva: doscientos " + str(self.HlbDistinto.idHistorialLB)
            r = self.controlador.nuevoHistorialLineaBase(self.HlbDistinto)
            self.assertEqual(r["estado"], True )
            print "Se guardan ambos con exito"
            self.contador = 3
            
        def tearDown(self):  
            if self.contador == 1 :
                print "Eliminamos una hlb nueva: cien " + str(self.HlbPrincipal.idHistorialLB)
                self.controlador.eliminarHistorialLineaBase(self.HlbPrincipal)
            if self.contador == 2 :
                print "Eliminamos una hlb nueva: cien " + str(self.HlbPrincipal.idHistorialLB)
                self.controlador.eliminarHistorialLineaBase(self.HlbPrincipal)
            if self.contador == 3 :
                print "Eliminamos una hlb nueva: cien " + str(self.HlbPrincipal.idHistorialLB)
                self.controlador.eliminarHistorialLineaBase(self.HlbPrincipal)
                print "Eliminamos una hlb nueva: doscientos  " + str(self.HlbDistinto.idHistorialLB)
                self.controlador.eliminarHistorialLineaBase(self.HlbDistinto)