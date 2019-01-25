'''
Declaracion de algunas clases necesarias
Como fortran utiliza declaracion de tipos, que no es soportado por python
es necesario utilizar clases
'''
import numpy as np

class AirfoilSurfaceClass(object):
    """
    npoints -> int
    x -> list
    y -> list
    topcorner -> int
    botcorner -> int
    """
    def __init__(self, npoints=None, x=None , y=None, name=None):
        super(AirfoilSurfaceClass, self).__init__()

        if npoints is None:
            npoints =0
        if x is None:
            x=[]
        if y is None:
            y=[]
        if name is None:
            name=''

        self.npoints = npoints
        self.topcorner = None
        self.botcorner=None
        self.x=x
        self.y=y
        self.name=name

def setOptions(AirfoilClass):
    options={
            "name":str(AirfoilClass.name),  #nombre del perfil
            "jmax":100,                     #numero de puntos por normal
            "ntedefault":13,                #numero
            "nsrfdefault":250,
            "nte":0,
            "imax":AirfoilClass.npoints,
            "lesp": 0.008/2.0,
            "tesp": 0.008/1.5,
            "fdst":.5,                     #espaciamiento de las normales
            "fwkl":1.0,
            "fwki":10.0,
            "yplus":0.9,
            "Re": 1e6,
            "cfrac":0.5,
            "maxsteps":10,                #numero de iteraciones
            "radi":15.0,                    #radio del circulo exterior
            "fsteps":20,
            "nwake":50,
            "nrmt":1,
            "nrmb":1,
            "alfa":1.0,
            "epsi":15.0,
            "epse":0.0,
            "funi":0.2,
            "asmt":20
            }
    return options

class GridClass(object):
    """ Define las propiedades de la malla.
    imax, jmax -> int -> tamanio de la malla
    x,y -> matrices tamanio [imax,jmax]
        almacenan imax normales con jmax puntos cada una
    xz, yz , xn, yn, xzz, yzz, xnn, ynn, jac -> matrices que
        aun no se que hacen

    surfnorm -> matriz -> indica las noramles a la superficie
    surfbounds -> lista de enteros con la forma [a,b]
    xicut, etacut -> listas de enteros con la forma [a,b]
    """
    def __init__(self):
        super(GridClass, self).__init__()
        self.imax = 0
        self.jmax = 0
        self.x= np.zeros([self.imax,self.jmax])
        self.y= np.zeros([self.imax,self.jmax])
        self.surfbounds = [0,0]
        self.surfnorm= np.zeros([0,0])
        self.xicut= [0,0]
        self.etacut= [0,0]
        self.xz = 0
        self.yz = 0
        self.xn = 0
        self.yn = 0
        self.xzz = 0
        self.yzz = 0
        self.xnn = 0
        self.ynn = 0
        self.jac = 0

class GridParamsClass(object):
    def __init__(self):
        self.A1=None
        self.A2=None
        self.A3 =None
        self.phi=None
        self.psi=None
