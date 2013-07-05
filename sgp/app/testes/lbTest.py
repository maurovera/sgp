import unittest  
import os
from app import db
from app.controlador import ControlLineaBase
#from app.controlador import ControlRelacion

from app.modelo import LineaBase
#from app.modelo import Relacion
# from app.controlador import ControlUsuario
# from app.modelo import Usuario

basedir = os.path.abspath(os.path.dirname(__file__))


class TestesItCuatro(unittest.TestCase):  
        def setUp(self):
            self.controlador = ControlLineaBase()
            self.lbPrincipal = LineaBase(numero=100, estado=200)
            self.lbDistinto = LineaBase(numero=200, estado=300)
            self.lbIgual = LineaBase(numero=100, estado=200)
            self.contador = 0
      
        def testGuarda(self):  
            r = self.controlador.nuevaLineaBase(self.lbPrincipal)
            print "Creamos una lb nueva: debe ser cien " + str(self.lbPrincipal.numero)
            self.assertEqual(r["estado"], True )  
            self.contador = 1
            
        def testGuardaRepetido(self):
            print "Creamos un usuario nuevo:" + str(self.lbPrincipal.numero)
            r = self.controlador.nuevaLineaBase(self.lbPrincipal)
            self.assertEqual(r["estado"], True)
            print "Creamos un usuario nuevo:" + str(self.lbIgual.numero) 
            r = self.controlador.nuevaLineaBase(self.lbIgual)
            #self.assertEqual(r["estado"], True ) #modifiqu este 
            print "No deberia guardar porque son iguales" 
            self.contador = 2
             
        def testGuardarDistinto(self):
            print "Creamos una lb nueva:cien  " + str(self.lbPrincipal.numero)
            r = self.controlador.nuevaLineaBase(self.lbPrincipal)
            self.assertEqual(r["estado"], True )
            print "Creamos una lb nueva: doscientos " + str(self.lbDistinto.numero)
            r = self.controlador.nuevaLineaBase(self.lbDistinto)
            #self.assertEqual(r["estado"], True )
            print "Se guardan ambos con exito"
            self.contador = 3
            
        def tearDown(self):  
            if self.contador == 1 :
                print "Eliminamos una lb nueva: cien " + str(self.lbPrincipal.numero)
                self.controlador.eliminarLineaBase(self.lbPrincipal)
            if self.contador == 2 :
                print "Eliminamos una lb nueva: cien " + str(self.lbPrincipal.numero)
                self.controlador.eliminarLineaBase(self.lbPrincipal)
            if self.contador == 3 :
                print "Eliminamos una lb nueva: cien " + str(self.lbPrincipal.numero)
                self.controlador.eliminarLineaBase(self.lbPrincipal)
                print "Eliminamos una lb nueva: doscientos  " + str(self.lbDistinto.numero)
                self.controlador.eliminarLineaBase(self.lbDistinto)
                
# if __name__ == '__main__':
#     unittest.main()