'''
Created on 10/04/2013

@author: cathesanz
'''
#INDEX

import datetime
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlProyecto
from app.modelo import Proyecto
from app.modelo import Rol
from app.controlador import ControlUsuario
from app.controlador import ControlPermiso
from app.modelo import Usuario
from contextlib import closing

controlador = ControlProyecto()
controladorusuario = ControlUsuario()


def busquedaPorNombre(nombre):
    ''' Devuelve un listado de los proyectos que coincidan con un nombre '''
    lista = None
    r = True
    if(r):
        lista = controlador.buscarPorNombre(nombre)
    else:
        flash("Error. Lista no devuelta")
    return lista

def listadoProyectos():
    ''' Devuelve un listado de los Proyectos '''
    lista = None
    r = True
    if(r):
        lista = controlador.getProyectos()
    else:
        flash("Error. Lista no devuelta")
    return lista



@app.route('/proyecto')
def indexProyecto():
    ''' Devuelve los datos de un proyecto en Concreto '''
    proyectos = listadoProyectos();
    usuarios = controladorusuario.getUsuarios()
    return render_template('indexProyecto.html', proyectos = proyectos, usuarios = usuarios)


@app.route('/proyecto/eliminar')
@app.route('/proyecto/eliminar/<id>')
def eliminarProyecto(id=None):
    if(id):
        proyecto = controlador.getProyectoById(id)

        if(proyecto):

            r= controlador.eliminarProyecto(proyecto)
            if(r["estado"] == True):
                flash("Se elimino con exito el proyecto: " + proyecto.nombre + " : " + proyecto.descripcion)
            else:
                flash("Ocurrio un error: "+ r["mensaje"])
        else :
            flash("Ocurrio un error durante la eliminacion")

    return redirect(url_for('indexProyecto'))




@app.route('/proyecto/nuevo', methods=['GET','POST'])
def nuevoProyecto():
    ''' Crea un nuevo proyecto '''
    #Si recibimos algo por post



    if request.method == 'POST' :

        print request.form['nombre']
        print request.form['descripcion']
        print request.form['idUsuario']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        idUsuario = request.form['idUsuario']
        # fechaCreacion = request.form['fechaCreacion']
        # complejidadTotal = request.form['complejidadTotal']
        # estado = request.form['estado']


        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente
        #con un metodo kachiai
        if(nombre and descripcion and idUsuario ):
            proyecto = Proyecto()
            proyecto.nombre = nombre
            proyecto.descripcion = descripcion
            proyecto.fechaCreacion = str(datetime.date.today())
            proyecto.complejidadTotal = 0
            proyecto.estado = "no iniciado"


            r = controlador.nuevoProyecto(proyecto)




            if(r["estado"] == True):
                #Creamos el rol con los permisos para el proyecto.
                u = controladorusuario.getUsuarioById(idUsuario)
                rolNuevo = crearRolProyecto(proyecto)
                r2 = controladorusuario.agregarRol(u,rolNuevo)
                if(r2["estado"] == True ):
                    flash("Exito, se creo un nuevo proyecto")
                else:
                    flash("Ocurrio un error : " + r2["mensaje"])
            else :
                flash("Ocurrio un error : " + r["mensaje"])

    return redirect(url_for('indexProyecto'))


@app.route('/proyecto/modificar', methods=['GET','POST'])
def modificarProyecto():
    ''' Modifica un proyecto '''



    if request.method == 'POST' :

        print request.form['nombre']
        print request.form['descripcion']
        print request.form['idProyecto']

        id = request.form['idProyecto']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']

        print "Estoy aca adentro del form..."
        #Si esta todo completo (Hay que hacer una verificacion probablemente
        #con un metodo kachiai
        if(id and nombre and descripcion ):
            proyecto = controlador.getProyectoById(id)
            if (proyecto):

                proyecto.nombre = nombre
                proyecto.descripcion = descripcion

                r = controlador.modificarProyecto(proyecto)
                if( r["estado"] == True ):
                    flash("modficamos con exito")
                else:
                    flash("Ocurrio un error : " + r["mensaje"])


    return redirect(url_for('indexProyecto'))

@app.route("/proyectos/buscar")
@app.route("/proyectos/buscar/<nombrebuscado>")
def buscarProyecto(nombrebuscado):
    ''' Devuelve una lista de proyectos que coincidan con el nombre proporcionado '''
    print "Helloooooowww"
    proyectos = busquedaPorNombre(nombrebuscado);
    return render_template('indexProyecto.html', proyectos = proyectos)

@app.route("/proyecto/iniciar")
@app.route("/proyecto/iniciar/<idProyecto>")
def iniciarProyecto(idProyecto):
    print "HOLA VITEH!" + idProyecto
    return redirect(url_for('indexProyecto'))

def crearRolProyecto(proyecto):
    ''' Se encarga de la creacion de un Rol con los permisos para administrar
        un Proyecto dado @return Rol'''
    r = Rol()
    r.nombre = "Administrador Proyecto " + proyecto.nombre
    r.descripcion = "Administrar el Proyecto " + proyecto.nombre
    r.idProyecto = proyecto.idProyecto
    #Agregamos los permisos en duro
    #Primero instanciamos el controlador
    cp = ControlPermiso()
    #Y vamos agregando los permisos respectivos a proyectos
    r.permisos.append(cp.buscarPorValor(7))
    r.permisos.append(cp.buscarPorValor(8))
    r.permisos.append(cp.buscarPorValor(9))
    r.permisos.append(cp.buscarPorValor(10))

    return r