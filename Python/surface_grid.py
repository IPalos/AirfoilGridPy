"""
Crea la malla
"""
import util
import eliptic_surface_grid as esg
import vardef as v
import numpy as np
import math


def createGrid(AirfoilClass,file):

    """
    Crea la malla eliptica asociada al perfil dado y sus opciones
    """

    options = v.setOptions(AirfoilClass)
    # DEBUG:
    print "Carga las opciones bien"

    grid = v.GridClass()
    # DEBUG:
    print "instancia bien a GridClass"

    #Establece el tamanio de la malla
    grid.imax = options["imax"]
    grid.jmax = options["jmax"]
    grid.x =np.zeros([grid.imax,grid.jmax])
    grid.y =np.zeros([grid.imax,grid.jmax])
    # DEBUG:
    print "tamanio del grid: "+str(grid.imax)+" "+str(grid.jmax)


    #toma las fronteras de la malla
    grid.surfbounds[0] = 1
    grid.surfbounds[1] = grid.imax

    # DEBUG:
    print "gridbounds: "+ str(grid.surfbounds)

    #guarda las fronteras en una variable local
    srf1, srf2 = grid.surfbounds

    #Coloca los puntos del perfil en la malla
    grid.x[:,0] = AirfoilClass.x
    grid.y[:,0] = AirfoilClass.y

    # DEBUG:
    print "Coloca correctamente los puntos del perfil en la malla"
    # A=v.AirfoilSurfaceClass(grid.imax,grid.x,grid.y)
    # util.PlotAirfoil(A)

    #Establece las esquinas
    AirfoilClass.topcorner = srf1
    AirfoilClass.botcorner = srf2

    grid.xicut[0] = 1
    grid.xicut[1] = grid.jmax
    grid.etacut[0] = 1
    grid.etacut[1] = 0

    #Crea la frontera exterior de la malla
    util.createFarfield(grid,options["radi"], options["fdst"])

    # DEBUG:
    print "Funciona bien la funcion createFarfield"
    # B=v.AirfoilSurfaceClass(grid.imax, grid.x, grid.y)
    # util.PlotAirfoil(B)


    #Crea la malla algebraica
    esg.algebraicGrid(grid)

    # DEBUG:
    print "Funciona bien la funcion algebraicGrid"
    # C=v.AirfoilSurfaceClass(grid.imax, grid.x, grid.y)
    # util.PlotAirfoil(C)

    nrm1 = options["nrmt"] + srf1-1
    nrm2 = srf2 - options["nrmb"]+1

    #Crea la malla eliptica (CHECAR SI FUNCIONA BIEN)
    # esg.ellipticGrid(grid, options, nrm1, nrm2)

    # copyEdges(grid)

    #Crea archivo p3d
    return util.writeSrfGrid(grid,file)


def copyEdges(gridClass):
    """
    Copia las orillas de la malla del inicio al final
    No devuelve nada, solo modifica la instancia de gridClass
        que toma como argumento
    """

    imax = gridClass.imax
    jmax = gridClass.jmax
    srf1 = gridClass.surfbounds[0]

    gridClass.x[imax-1,:] = gridClass.x[1,:]
    gridClass.y[imax-1,:] = gridClass.y[1,:]
