from app.modelo import Usuario
from app import db


class ControlUsuario():
    """ clase control usuario """
    def getUsuarioById(self,id):
        """ funcion get usuariobyid """
        return Usuario.query.get(id)
    def getUsuarios(self):
        """ funcion getusuario """
        return Usuario.query.all()
    def nuevoUsuario(self, usuario):
        """ funcion nuevoUsuario """
        resultado = {"estado" : True, "mensaje" : "exito"}
        try:
            db.session.add(usuario)
            #print "Hice el add"
            db.session.commit()
            #print "Hice el commit"
        except Exception, error :
            #print "Capturo exp" + str(error)
            resultado = {"estado" : False, "mensaje" : str(error)}
            db.session.rollback()

        return resultado

    def eliminarUsuario(self, usuario):
        """ funcion eliminarUsuario """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un delete de usuario """
            
            if usuario.nombreUsuario == "root" :
                resultado = {"estado" : False, "mensaje" :  "el usuario root no se puede eliminar"}
                return resultado
        
            ''' lista de roles '''
            import crol
            controlRol = crol.ControlRol()
            lista = controlRol.buscarPorNombre("Administrador")
            siTengoUnAdmin = False
            for rol in lista:
                if rol in usuario.roles:
                    siTengoUnAdmin = True
                    break
                
            # si la lista tiene al menos un admin no se borra
            if(siTengoUnAdmin):
              resultado = {"estado" : False, "mensaje" :  "no se puede eliminar un usuario que es Admin en un Proyecto dado"}       
              return resultado
          
            else:
                db.session.delete(usuario)
                """ se comitea el cambio """
                db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado


    def modificarUsuario(self, usuario):
        """ funcion modificarUsuario """
        resultado = {"estado": True, "mensaje" : "exito"}
        try:
            """ hacemos un merge de usuario """
            db.session.merge(usuario)
            """ se comitea el cambio """
            db.session.commit()
        except Exception, error:
            """ se captura el error con un exception """
            resultado = {"estado" : False, "mensaje" :  str(error)}
            db.session.rollback()

        return resultado



    def comprobarLogin(self, usuario):
        """ funcion comprobar usuario """
        retorno = db.session.query(Usuario).filter_by(nombreUsuario=usuario.nombreUsuario, contrasena=usuario.contrasena).first()
        print retorno
        return retorno

    def buscarPorNombre(self,nombre):
        retorno = db.session.query(Usuario).filter(Usuario.nombre.ilike("%"+nombre+"%")).all()
        #retorno = db.session.query(Usuario).filter_by(nombre=nombre).all()
        return retorno

    def agregarRol(self,usuario,rol):

        nohay = True
        for r in usuario.roles :
            if(rol == r):
                print "YA HAY ESTE! ROL"
                nohay = False

        if (nohay):
            print "Agregamos!"
            usuario.roles.append(rol)
            return self.modificarUsuario(usuario)
        else :
            resultado = {"estado" : False, "mensaje" : "El usuario ya posee ese rol"}
            return resultado

    def quitarRol(self,usuario,rol):
        ''' quitamos un rol '''
        
        lista = usuario.roles
        if len(lista) > 1:
            usuario.roles.remove(rol)
            return self.modificarUsuario(usuario)
        else:
            resultado = {"estado" : False, "mensaje" : "El rol no se puede eliminar, el usuario tiene que tener al menos un rol"}
            return resultado
            
        
    def getPermisos(self,usuario) :
        ''' Retorna una lista con todos los "valores/codigo"
            de permisos que posee un usuari '''
        permisos = []
        r = usuario.roles
        for rol in r :
            permisos += rol.permisos
            valorpermisos = []
        for p in permisos:
            valorpermisos.append(p.valor)
        return valorpermisos

    def getPermisosByIdProyecto(self,usuario,idProyecto):
        ''' Retorna la lista de permisos que posee un usuario en un Proyecto'''
        permisos = []
        r = usuario.roles
        for rol in r :
            if ( rol.idProyecto == idProyecto):
                permisos += rol.permisos
        valorpermisos = []
        for p in permisos:
            valorpermisos.append(p.valor)
        return valorpermisos

    def getPermisosByIdFase(self,usuario,idFase):
        ''' Retorna la lista de permisos que posee un usuario en un Proyecto'''
        permisos = []
        r = usuario.roles
        for rol in r :
            if ( rol.idFase == idFase):
                permisos += rol.permisos
        valorpermisos = []
        for p in permisos:
            valorpermisos.append(p.valor)
        return valorpermisos

    def getUsuarioByRol(self, rol):
        print ">>>>>>>>>>>>,,,,,,,"
        print rol
        usuarios = self.getUsuarios()
        print usuarios
        for usuario in usuarios:
            print usuario
            print usuario.roles
            if rol in usuario.roles :
                print "Entro"
                return usuario
    
    def getUsuariosByRol(self, rol):
        print "IN getUsuariosByRol"
        print rol
        usuarios = self.getUsuarios()
        print usuarios
        retorno = []
        for usuario in usuarios:
            print usuario
            print usuario.roles
            if rol in usuario.roles :
                retorno.append( usuario )
            
        return retorno 
    
    def esUsuarioRoot(self, usuario):
        
        if usuario.nombreUsuario == "root":
            return True
        else:
            return False  