'''
Programa principal de la Traduccion de Fortran90->Python2.7
'''

import vardef as v
import util
import subprocess as sp
import surface_grid as sg
import visualizeGrid as vg



version='Py 1.0.0'

#empieza el programa
util.greeting(version)
tpath=util.rootPath
path,file = util.read_cl(tpath)

#prof[0] -> x
#prof[1] -> y
#prof[2] -> profileSize
#prof[3] -> profileTitle
prof=util.createProfileInput(path,file+".dat")

# npoints -> int
# x -> list
# y -> list
# topcorner -> int
# botcorner -> int
#name -> string
WingSurf=v.AirfoilSurfaceClass(prof[2], prof[0], prof[1],prof[3])
util.transformAirfoil(WingSurf) #normaliza y centra los puntos del perfil (coloca el frente en 0)


#Muestra el perfil antes de empezar a procesarlo
graf= raw_input("Desea visualizar el perfil ingresado?:(y/n)")
if (graf=='y' or graf =='yes' or graf=='Y'):
    util.PlotAirfoil(WingSurf)

data = sg.createGrid(WingSurf,file)


imax, jmax, x, y = vg.readGrid(data)

#Grafica
vg.plot_grid(x, y)
