"""
Traduccion del archivo math_deps
Contiene herramientas matematicas utiles para el
    funcionamiento del programa
"""
import math
import numpy as np


def bspline(Pin, degree, npoints):
    """
    Pin -> matriz [2,2]
    degree -> int
    npoints -> numero de puntos -> jmax
    OUTPUT -> x,y,z list(len(npoints))
    """

    n = np.shape(Pin)[1]
    m = np.shape(Pin)[0]

    P=np.zeros([2,2])

    T=np.zeros([degree+n+2])
    tvec=[]
    Nvec=[0.0]*(n)
    Q=np.zeros([2,npoints])

    # DEBUG:
    # print P
    # print Pin

    #almacena en buffer a Pin, y lo convierte en una matriz 3x3
    #sin importar si es 2D o 3D
    if m < 2:
        print "ERROR en math_deps.bspline"
        print "MATRIZ MUY CHICA"
    elif m == 2 or m == 3 :
        P=Pin
    else:
        print "ERROR en math_deps.bspline"
        print "MATRIZ MUY GRANDE"

    #checa si la dimensionalidad es correcta
    if degree > n or degree <1:
        print "ERROR en math_deps.bspline"
        print "DEGREE RARITO"

    #almacena algo en T
    for i in range(1,degree+n+3):
        if i < degree+2:
            T[:] = 0.0
        elif i == 4:
            T[3]= 1
        elif i == 5:
            T[3:5]= 1
        else:
            T[3:6] = 1

    # DEBUG:
    # print "T funciona bien"

    for i in range(npoints):
        tvec.append(float(i)/float(npoints-1))

    ## DEBUG:
    # print "tvec funciona bien"
    # print tvec

    bolsillo=open("pynvec.csv","w")

    for j in range(npoints):
        for i in range(n):
            #Nvec funciona bien
                Nvec[i]= basisFunc(degree, i, T, tvec[j])
                Q[:,j]= Q[:,j]+ (P[:,i]*abs(Nvec[i]))


    # for j in range(npoints):
    #     #Nvec funciona bien
    #     Nvec[0]= basisFunc(degree, 0, T, tvec[j])
    #     Q[0,j]= Q[0,j]+ (P[0,1]*Nvec[0])
    #     Nvec[1] = basisFunc(degree, 1, T, tvec[j])
    #     Q[1,j]= Q[1,j]+ (P[1,1]*Nvec[1])

        bolsillo.write( str(Nvec)[1:-1]+"\n" )

    bolsillo.close()

    x,y = Q

    return x,y


def basisFunc(j,i,x,t):
    """
    No se que hace esta funcion, pero los parametros son:
    x -> lista -> vector T =[0,0,0,1,1,1]
    i -> int -> indice del Nvec
    j -> int -> grado (2)
    t -> float -> tvec[l] = (i)/(jmax-1)
    La funcion es recursiva y regresa:
    val -> int
    """
    m=len(x)

    if j == 0:
        if (x[i] <= t) and (t< x[i+1]):
            val = 1.0
        elif (x[i] <= t ) and (t == x[i+1]) and (x[i+1] == 1.0):
            val = 1.0
        else:
            val=0.0
    else:
        if x[i] < x[i+j]:
            val = (t-x[i])/(x[i+j]-x[i]) * basisFunc(j-1,i,x,t)
        else:
            val=0

        if i < m:
            if (x[i+1] < x[i+j+1]):
                val = val + (x[i+j+1]-t) / (x[i+j+1]-x[i+1]) *basisFunc(j-1,i+1,x,t)

    return val


def isEven(num):
    if math.ceil(float(num)/2.0) == math.floor(float(num)/2):
        val = 1
    else:
        val = 0
    return val


def derv1f(U,u,h):
    return float(U-u)/float(h)


def derv1b(u,U,h):
    return float(U-u)/float(h)


def derv1c(U,u,h):
    return float(U-u)/float(h*2)


def derv2f(U2,U,u,h):
    return float(u-(2*U)+U2)/float(h**2)


def derv2b(u2,u,U,h):
    return float(U-(2*u)+u2)/float(h**2)


def derv2c(U,u,mu,h):
    return float(U-(2*u)+mu)/float(h**2)


def tridiagMod(A,C):
    N = len(C)
    X=np.zeros([len(C)])
    Q=np.zeros([len(C),len(C)+1])
    pivot = elim  = rscale =rsum = 0.0

    Q[:,0:N] = A
    Q[:,N] = C

    for R in range(N-1):
        pivot = Q[R,R]
        for i in range(R+1,R+1): ###wat?
            elim = Q[i,R]
            if abs(elim) > eps:
                rscale = elim/pivot
                Q[i,:] = Q[i,:]-rscale*Q[R,:]
    for i in range(N-1,0,-1):
        rsum = Q[i,N]
        if i<N :
            for j in range(i+1, i+1, -1): ###wat?
                rsum -= Q[i,j]*X[j]
    if i< N-2:
        rsum-= Q[i,N-1]*X[N-1]

    if Q[i,i] == 0.0:
        print "ERROR EN tridiagMod"
    else:
        X[i]=rsum/Q[i,i]
