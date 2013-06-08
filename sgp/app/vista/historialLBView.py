#INDEX
from flask import render_template, flash, redirect, request, session, g, url_for, abort
from app import app
from app.controlador import ControlHistorialLineaBase
from app.modelo import HistorialLineaBase
from contextlib import closing

control = ControlHistorialLineaBase()

def listadoHistorialLineaBase():
    ''' Devuelve un listado de los HistorialLineaBase '''
    lista = None
    r = True
    if(r):
        lista = control.getHistorialLineaBase()
    else:
        flash("Error. Lista no devuelta")
    return lista



@app.route('/hLB')
def indexHistorialLineaBase():
    ''' Devuelve los datos de un HLB en Concreto '''
    hLB = listadoHistorialLineaBase();
    return render_template('indexHistorialLineaBase.html', hLB = hLB)

