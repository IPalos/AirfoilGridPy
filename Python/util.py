"""
Maneja las utilidades y funciones auxiliares del programa
"""
import sys
import csv
import subprocess as sp
import matplotlib.pyplot as plt
import math
import numpy as np
import math_deps as m

#INSERTAR DIRECCION DE DONDE IMPORTAR LOS ARCHIVOS

a=sp.Popen("pwd", stdout=sp.PIPE)
user = a.stdout.read()
rootPath=user[:-1]


def greeting(version):
    print ("\n\n\nEste es Construct2D, edicion Python2\n\n\n")
    print ('Version: '+str(version)+"\n\n\n")


def read_cl(path):
    """
    Utiliza el primer agrumento como archivo input
    """
    filename=''
    cpath=path+'/sample_airfoils'
    while filename == '':
        if len(sys.argv) > 1 and sys.argv[1] != '':
            filename= str(sys.argv[1])

        else:
            print "Directorio actual: "+ str(cpath)
            pathCorrect = raw_input("Desea cambiarlo?:(y/n)")

            if (pathCorrect=='y' or pathCorrect =='yes' or pathCorrect=='Y'):
                cpath =raw_input("Intgrese un nuevo directorio: ")

            print "Archivos encontrados en el directorio actual: "
            sp.call(['ls', cpath, '-l'])
            filename= raw_input("Ingresa el nombre del archivo del perfil: \n(sin la extension) ")

    return cpath, filename


def createProfileInput(path,file):
    """
    Crea una lista de duplas (x,y) a partir de
    el archivo de input
    path -> string, la direccion donde se encuentra el arhicvo
    file -> string, el nombre del archivo
    OUTPUT:(listaDePuntosDelPerfil, numeroDePuntos)
    """
    with open(path+"/"+file , 'rb') as f:
        reader = csv.reader(f)
        profileList = map(list, reader)

    profileTitle= profileList[0][0]
    profileList=profileList[1:]
    profileSize=len(profileList)

    for i in range(len(profileList)):
        for j in range(len(profileList[i])):
            profileList[i][j]=float(profileList[i][j])

    x=[]
    y=[]
    for i in profileList:
        x.append(i[0])
        y.append(i[1])

    print "============DATOS DEL ARCHIVO======================"
    print "Nombre del perfil: "+ profileTitle
    print "Numero de puntos: "+ str(profileSize)


    return (x,y, profileSize, profileTitle)


def transformAirfoil(AirfoilClass):
    """
    Normaliza el perfil alar y coloca el frente en 0
    """
    x=AirfoilClass.x
    y=AirfoilClass.y
    xtemp=[]
    ytemp=[]
    dist=min(x)

    for i in x:
        xtemp.append(i-dist)

    npoint=max(xtemp)
    ratio=(max(xtemp)-min(xtemp))

    for i in range(AirfoilClass.npoints):
        xtemp[i]=xtemp[i]/ratio
        ytemp.append(y[i]/ratio)


def PlotAirfoil(AirfoilClass):

    plt.scatter(AirfoilClass.x,AirfoilClass.y)
    plt.axis([-1.0,2.0,-1.5,1.5]) #define en espacio a graficar con las medidas anteriores
    # plt.axis("equal") #grafica a la misma escala en eje x y y
    plt.show()
    plt.axis
    plt.xlabel(AirfoilClass.name)


def createFarfield(gridClass, radi, fdst):
    """
    Crea la frontera exterior de la malla
    """

    imax = gridClass.imax
    jmax= gridClass.jmax
    srf1 = gridClass.surfbounds[0]
    srf2 = gridClass.surfbounds[1]

    tol = 1e-12
    errval=1000.0
    d0=0.0

    #Calcula la calidad de la malla
    #checar si is_even es necesario
    # while errval > tol:
    #     lguess = 2.0 * math.pi * radi + float(m.isEven(imax)) * d0
    #     d0 = 1.0/fdst*lguess/float(imax-1)
    #     lcirc = 2.0 * math.pi * radi + float(m.isEven(imax))*d0
    #     errval = math.sqrt((lguess-lcirc)**2)/lguess

    # d0=1.0/fdst*lcirc/float(imax-1)

    gridClass.x[0,-1]=radi +0.5
    gridClass.y[0,-1]= 0.0
    gridClass.x[-1,-1] = gridClass.x[0,jmax-1]
    gridClass.y[-1,-1]=0.0

    ang=0.0
    ## DEBUG: si hay que regresar a la normalidad, descomentar esto y
    #los gridClass de abajo
    # nouter = int(math.ceil(float(imax)/2))
    nouter = imax

    nfaux = nouter -1 + m.isEven(imax)

    for i in range(nouter):


        space = 2.0*math.pi*radi/float(imax-1)

        ang= ang + space/radi
        gridClass.x[i,-1]=radi*math.cos(ang)+0.5
        gridClass.y[i,-1]=radi*math.sin(ang)
        # gridClass.x[imax-i,-1] = gridClass.x[i-1,-1]
        # gridClass.y[imax-i,-1] = -gridClass.y[i-1,-1]


def writeSrfGrid(gridClass,file):
    """
    Funcion para escribir el archivo .p3d
    gridClass -> instancia de un objeto GridClass
    """
    imax = gridClass.imax
    jmax = gridClass.jmax

    renderPath=rootPath+"/renders/"+file+".p3d"

    f=open(renderPath,"w")

    f.write(str(imax)+"   "+str(jmax)+"\n")

    for j in range(jmax):
        for i in range(imax):
            f.write(str(gridClass.x[i,j])+'\n')

    for j in range(jmax):
        for i in range(imax):
            f.write(str(gridClass.y[i,j])+'\n')

    return renderPath
