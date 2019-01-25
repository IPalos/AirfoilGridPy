"""
Programa para visualizar la malla
INPUT   ->  archivo .p3d
OUTPUT  ->  grafica de la malla tipo O-grid, calculada
            con un solucionador eliptico

USO RECOMENDADO ->  Se abre automaticamente cuando
                    se ejecuta main.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import math
import sys
import util

"""
MAIN
"""
def main():
    path=util.rootPath+"/renders"

    if len(sys.argv)> 1 and sys.argv[1]!= '':
        filename = str(sys.argv[1])
    gridfile = filename + '.p3d'
    print path+'/'+gridfile

    #Checa si existe el archivo
    try:
      f = open(path+'/'+ gridfile)
    except IOError:
      print 'NO HAY ARCHIVO ' + gridfile +'\n'
      return
    else:
      f.close

    #almacena los datos del archivo en el programa
    imax, jmax, x, y = readGrid(path+'/'+gridfile)

    #Grafica
    plot_grid(x, y)

"""
Desmenuza el archivo para formar una malla
"""
def readGrid(file):

  f = open(file)

  line1 = f.readline()

  #obtiene imax y jmax a partir de los primeros
  #numeros del archivo.p3d
  imax, jmax = [int(x) for x in line1.split()]

  #Crea matrices tamanio imax, jmax
  x = np.zeros((imax,jmax))
  y = np.zeros((imax,jmax))

  #llena a x de valores del archivo
  for j in range(0, jmax):
    for i in range(0, imax):
      x[i,j] = float(f.readline())

  #llena a y de valores del archivo
  for j in range(0, jmax):
    for i in range(0, imax):
        y[i,j] = float(f.readline())

  f.close()

  return (imax, jmax, x, y)

"""
Cambia los vectores x,y a segmentos de linea que entiende numpy
"""
def Line2Segment(x, y):

  points = np.array([x, y]).T.reshape(-1, 1, 2)
  segments = np.concatenate([points[:-1], points[1:]], axis=1)
  return segments

"""
Funcion para graficar la malla
"""
def plot_grid(x, y, colormap='jet', plaincolor='black',
              varname=None, var=None, minvar=None, maxvar=None):


  print 'Graficanding'

  #Determina tamanio de la matriz
  imax = x.shape[0]
  jmax = x.shape[1]

  #Guarda la grafica en el buffer
  fig = plt.figure()
  ax = fig.add_subplot(111)

  for j in range(0, jmax):
    segments = Line2Segment(x[:,j], y[:,j])
    lc = LineCollection(segments, colors=plaincolor)
    ax.add_collection(lc)
  for i in range(0, imax):
    segments = Line2Segment(x[i,:], y[i,:])
    lc = LineCollection(segments, colors=plaincolor)
    ax.add_collection(lc)

  title = 'Geometria de la malla'

  #Muestra la grafica
  plt.title(title)
  plt.xlabel('x')
  plt.ylabel('y')
  # plt.axis([-2,2,-2,2])
  plt.axis("equal")
  plt.show()


"""
Arranca el programa
"""
# main()
