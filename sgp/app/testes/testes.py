import unittest  
import os
basedir = os.path.abspath(os.path.dirname(__file__))



class EjemploFixture(unittest.TestCase):  
        def setUp(self):  
            print "Preparando el uri del la base datos"  
            self.rv =  'postgresql://postgres:mauro@localhost/sgp' 
      
        def test(self):  
            print "Ejecutando prueba"  
            SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mauro@localhost'
            
            #r = [cuadrado(n) for n in self.lista]  
            self.assertEqual(SQLALCHEMY_DATABASE_URI, self.rv)  
      
        def tearDown(self):  
            print "Desconstruyendo uri"  
            del self.rv      
            
          
if __name__ == "__main__":  
    unittest.main()  