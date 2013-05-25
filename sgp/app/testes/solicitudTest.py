import unittest  
import os
from app import db
from app.controlador import ControlSolicitud
from app.modelo import SolicitudDeCambio

basedir = os.path.abspath(os.path.dirname(__file__))



class TestSol(unittest.TestCase):  
        def setUp(self):
            self.controlador = ControlSolicitud()
            self.sol1 = SolicitudDeCambio(idSolicitud=1000, nombreSolicitud="SOL1", descripcion="BLA", estado="creado")
            self.soldistinto = SolicitudDeCambio(idSolicitud=2001, nombreSolicitud="SOLDISTINTO", descripcion="BLE", estado="creado")
            self.soligual = SolicitudDeCambio(idSolicitud=1000, nombreSolicitud="SOLIGUAL", descripcion="BLI", estado="creado")
            self.contador = 0
            
#             idSolicitud = db.Column(db.Integer, primary_key = True)
#     nombreSolicitud = db.Column( db.String(45), index = True, nullable = False)
#     descripcion = db.Column( db.String(160) , nullable = False)
#     estado = db.Column( db.String(45) )
            
            
            
      
        def testGuarda(self):  
            r = self.controlador.nuevaSolicitud(self.sol1)
            print "Creamos una Solicitud nueva" + self.sol1.nombreSolicitud
            self.assertEqual(r["estado"], True )  
            self.contador = 1
            
        def testGuardaRepetido(self):
            print "Creamos una Solicitud nueva:" + self.sol1.nombreSolicitud
            r = self.controlador.nuevaSolicitud(self.sol1)
            self.assertEqual(r["estado"], True)
            print "Creamos una Solicitud nueva:" + self.soligual.nombreSolicitud 
            r = self.controlador.nuevaSolicitud(self.soligual)
            self.assertEqual(r["estado"], False)
            print "No deberia guardar porque son iguales" 
            self.contador = 2
             
        def testGuardarDistinto(self):
            print "Creamos una Solicitud nueva:" + self.sol1.nombreSolicitud
            r = self.controlador.nuevaSolicitud(self.sol1)
            self.assertEqual(r["estado"], True )
            print "Creamos una Solicitud nueva:" + self.soldistinto.nombreSolicitud
            r = self.controlador.nuevaSolicitud(self.soldistinto)
            self.assertEqual(r["estado"], True )
            print "Se guardan ambos con exito"
            self.contador = 3
            
        def tearDown(self):  
            if self.contador == 1 :
                print "Eliminamos una Solicitud nueva " + self.sol1.nombreSolicitud
                self.controlador.eliminarSolicitud(self.sol1)
            if self.contador == 2 :
                print "Eliminamos una Solicitud nueva " + self.sol1.nombreSolicitud
                self.controlador.eliminarSolicitud(self.sol1)
            if self.contador == 3 :
                print "Eliminamos  una Solicitud nueva " + self.sol1.nombreSolicitud
                self.controlador.eliminarSolicitud(self.sol1)
                print "Eliminamos  una Solicitud nueva " + self.soldistinto.nombreSolicitud
                self.controlador.eliminarSolicitud(self.soldistinto)