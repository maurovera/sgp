import unittest  
import os
from app import db
from app.controlador import ControlProyecto
from app.modelo import Proyecto

basedir = os.path.abspath(os.path.dirname(__file__))



class TestProyectos(unittest.TestCase):  
        def setUp(self):
            self.controlador = ControlProyecto()
            self.proyecto1 = Proyecto(nombre="proyecto4", descripcion="pro", fechaCreacion = '2013-04-20')
            #self.proyectodistinto = proyecto(nombre="proyecto5", descripcion="pro", fechaCreacion='2013-04-19', complejidadtotal=0, estado="No iniciado")
            self.proyectoigual = Proyecto(nombre="proyecto4", descripcion="pro", fechaCreacion='2013-04-19')
            self.contador = 0
      
        def testGuarda(self):  
            r = self.controlador.nuevoProyecto(self.proyecto1)
            print "Creamos un proyecto nuevo" + self.proyecto1.nombre
            self.assertEqual(r["estado"], True )  
            self.contador = 1
            
        def testGuardaRepetido(self):
            print "Creamos un proyecto nuevo:" + self.proyecto1.nombre
            r = self.controlador.nuevoProyecto(self.proyecto1)
            self.assertEqual(r["estado"], True)
            print "Creamos un proyecto nuevo:" + self.proyectoigual.nombre 
            r = self.controlador.nuevoProyecto(self.proyectoigual)
            # para la prueba se dice que estado sea true, osea el correcto. y 
            # tirara una excepcion porque el nombre es unique
            
            self.assertEqual(r["estado"], False)
            print "No deberia guardar porque son iguales" 
            self.contador = 2
             
        #def testGuardarDistinto(self):
            #print "Creamos un proyecto nuevo:" + self.proyecto1.nombre
            #r = self.controlador.nuevoProyecto(self.proyecto1)
            #self.assertEqual(r["estado"], True )
            #print "Creamos un proyecto nuevo:" + self.proyectodistinto.nombre
            #r = self.controlador.nuevoProyecto(self.proyectodistinto)
            #self.assertEqual(r["estado"], True )
            #print "Se guardan ambos con exito"
            #self.contador = 3
            
        def tearDown(self):  
            if self.contador == 1 :
                print "Eliminamos el proyecto nuevo" + self.proyecto1.nombre
                db.session.delete(self.proyecto1)
                db.session.commit()
                
            if self.contador == 2 :
                 print "Eliminamos el proyecto nuevo" + self.proyecto1.nombre
                 db.session.delete(self.proyecto1)
                 db.session.commit()
            #if self.contador == 3 :
                #print "Eliminamos el proyecto nuevo" + self.proyecto1.nombre
                #self.controlador.eliminarProyecto(self.proyecto1)
                #print "Eliminamos el proyecto nuevo distinto" + self.proyectodistinto.nombre
                #self.controlador.eliminarProyecto(self.proyectodistinto)