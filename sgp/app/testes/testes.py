import unittest  
import os
from app import db
from app.controlador import ControlUsuario
from app.modelo import Usuario

basedir = os.path.abspath(os.path.dirname(__file__))



class TestUsuarios(unittest.TestCase):  
        def setUp(self):
            self.controlador = ControlUsuario()
            self.usuario1 = Usuario(nombreUsuario="Nombre1", contrasena="puto", nombre="Mauro", apellido="Korea", telefono="123-321-123", CI = 123321, email="un@email.com")
            self.usuariodistinto = Usuario(nombreUsuario="NomnbreOtro", contrasena="puto", nombre="Mauro", apellido="Korea", telefono="123-321-123", CI = 123321, email="otro@email.com")
            self.usuarioigual = Usuario(nombreUsuario="Nombre1", contrasena="puto", nombre="Mauro", apellido="Korea", telefono="123-321-123", CI = 123321, email="un@email.com")
            self.contador = 0
      
        def testGuarda(self):  
            r = self.controlador.nuevoUsuario(self.usuario1)
            print "Creamos un usuario nuevo" + self.usuario1.nombreUsuario
            self.assertEqual(r["estado"], True )  
            self.contador = 1
            
        def testGuardaRepetido(self):
            print "Creamos un usuario nuevo:" + self.usuario1.nombreUsuario
            r = self.controlador.nuevoUsuario(self.usuario1)
            self.assertEqual(r["estado"], True)
            print "Creamos un usuario nuevo:" + self.usuarioigual.nombreUsuario 
            r = self.controlador.nuevoUsuario(self.usuarioigual)
            self.assertEqual(r["estado"], False)
            print "No deberia guardar porque son iguales" 
            self.contador = 2
             
        def testGuardarDistinto(self):
            print "Creamos un usuario nuevo:" + self.usuario1.nombreUsuario
            r = self.controlador.nuevoUsuario(self.usuario1)
            self.assertEqual(r["estado"], True )
            print "Creamos un usuario nuevo:" + self.usuariodistinto.nombreUsuario
            r = self.controlador.nuevoUsuario(self.usuariodistinto)
            self.assertEqual(r["estado"], True )
            print "Se guardan ambos con exito"
            self.contador = 3
            
        def tearDown(self):  
            if self.contador == 1 :
                print "Eliminamos el usuario nuevo" + self.usuario1.nombreUsuario
                self.controlador.eliminarUsuario(self.usuario1)
            if self.contador == 2 :
                print "Eliminamos el usuario nuevo" + self.usuario1.nombreUsuario
                self.controlador.eliminarUsuario(self.usuario1)
            if self.contador == 3 :
                print "Eliminamos el usuario nuevo" + self.usuario1.nombreUsuario
                self.controlador.eliminarUsuario(self.usuario1)
                print "Eliminamos el usuario nuevo" + self.usuariodistinto.nombreUsuario
                self.controlador.eliminarUsuario(self.usuariodistinto)