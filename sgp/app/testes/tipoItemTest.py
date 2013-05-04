import unittest  
import os
from app import db
from app.controlador import ControlTipoItem
from app.modelo import TipoItem

basedir = os.path.abspath(os.path.dirname(__file__))



class TestTipoItem(unittest.TestCase):  
        def setUp(self):
            self.controlador = ControlTipoItem()
            self.tipoItem1 = TipoItem(nombre="tipoDeItem", codigo= "12401", descripcion="pro1")
            #self.tipoItemDistinto = tipoItem(nombre="tipoDeItem44", codigo= "1240", descripcion="pro")
            self.tipoItemIgual = TipoItem(nombre="tipoDeItem", codigo= "1240", descripcion="pro2")
            self.contador = 0
      
        def testGuarda(self):  
            r = self.controlador.nuevoTipoItem(self.tipoItem1)
            print "Creamos un tipo nuevo" + self.tipoItem1.nombre
            self.assertEqual(r["estado"], True )  
            self.contador = 1
            
        def testGuardaRepetido(self):
            print "Creamos un tipo item nuevo:" + self.tipoItem1.nombre
            r = self.controlador.nuevoTipoItem(self.tipoItem1)
            self.assertEqual(r["estado"], True)
            print "Creamos un tipo item nuevo:" + self.tipoItemIgual.nombre 
            r = self.controlador.nuevoTipoItem(self.tipoItemIgual)
            # para la prueba se dice que estado sea true, osea el correcto. y 
            # tirara una excepcion porque el nombre es unique
            
            self.assertEqual(r["estado"], False)
            print "No deberia guardar porque son iguales" 
            self.contador = 2
             
      
            
        def tearDown(self):  
            if self.contador == 1 :
                print "Eliminamos el tipo de item nuevo" + self.tipoItem1.nombre
                db.session.delete(self.tipoItem1)
                db.session.commit()
                
            if self.contador == 2 :
                 print "Eliminamos el tipo de item nuevo" + self.tipoItem1.nombre
                 db.session.delete(self.tipoItem1)
                 db.session.commit()
           