'''
Traduccion de Fortran90 a python del archivo elliptic_surface_grid.f90 del programa Construct2D
'''
import math_deps
import surface_util
import math
import numpy as np
import vardef as v


def algebraicGrid(gridClass):
    '''
    Genera un gridClass
    gridClass -> objeto con atributos
        gridClass.imax -> int -> longitud maxima de la malla
        gridClass.jmax -> int -> altura maxima de la malla
        gridClass.surfnorm -> matriz (2 x #puntos)
                      -> guarda las normales de la superficie

    '''

    nlen=0.001
    n=[0,0]
    x=y=[0]*gridClass.jmax
    CPmat=np.zeros([2,2])
    intervalo=0.0

    # surface_util.surfaceNormals(gridClass, 0)
    # DEBUG:
    print "Funciona bien la funcion surfaceNormals"

    for i in range(gridClass.imax):
        surface_util.surfaceNormals(gridClass, gridClass.jmax-1)
        n[0],n[1]=gridClass.surfnorm[i]

        #Crea una normal interior (hacia el centro)
        gridClass.x[i,1]=gridClass.x[i,0]-(nlen*n[0])
        gridClass.y[i,1]=gridClass.y[i,0]-(nlen*n[1])

        #intercambia sus lugares (cambia normales)
        gridClassTemp=[gridClass.x[i,0],gridClass.y[i,0]]
        gridClass.x[i,0]=gridClass.x[i,1]
        gridClass.y[i,0]=gridClass.y[i,1]
        gridClass.x[i,1],gridClass.y[i,1]=gridClassTemp

        #calcula la distancia entre el farfield y la segunda normal
        #y obtiene el intervalo para colocar cada punto
        xdist= gridClass.x[i,1] - gridClass.x[i,-1]
        ydist= gridClass.y[i,1] - gridClass.y[i,-1]
        dist= math.sqrt(xdist**2+ydist**2)

        for j in range(1,gridClass.jmax-1):
            gridClass.x[i,j]=gridClass.x[i,j-1]+((dist/(gridClass.jmax-2))*n[0])
            gridClass.y[i,j]=gridClass.y[i,j-1]+((dist/(gridClass.jmax-2))*n[1])


def ellipticGrid(grid,options,topcorner,botcorner):
    '''
    Preocesa la malla algebraica utilizando un generador
    de mallas de Laplace
    grid -> objeto con los atributos:
            grid.imax -> int -> longitud maxima de la malla
            grid.jmax -> int -> altura maxima de la malla
            grid.x -> lista -> coordenadas x de la malla
            grid.Y -> lista -> coordenadas y de la malla
    '''
    maxits= options["maxsteps"]
    jacobian=False

    imax=grid.imax
    jmax=grid.jmax

    print "Malla eliptica"

    RMSr=1000.0
    n=0

    xold=[]
    yold=[]

    params = v.GridParamsClass()

    while n< maxits :
        xold=grid.x
        yold = grid.y

        surface_util.computeInverseMetrics(grid,jacobian)

        computeParams(grid,params, n)

        for j in range (jmax-1):
            updateOgrid(grid, params, j, 'x',topcorner, botcorner)
            updateOgrid(grid, params, j, 'y',topcorner, botcorner)

        #FUNCION AUN NO TRADUCIDA
        # gridResidual(grid.x, xold, grid.y, yold, RMSr)

        print "Iteracion: "+str(n)+"de "+str(maxits+20)
        n+=1

    print'Aplicando espaciado normal'

    #FUNCION AUN NO TRADUCIDA
    # applyNormalSpacing(grid, options)

    maxits= n+20

    print 'Aplicando smoothing final'

    while n < maxits:

        xold = grid.x
        yold = grid.y

        # computeInverseMetrics(grid, jacobian)

        # computeParams(grid, params, n)
        #
        # for j in range(1,jmax):
        #     updateOgrid(grid, params, j, 'x', topcorner, botcorner)
        #     updateOgrid(grid, params, j, 'y', topcorner, botcorner)

        print "Iteracion: "+str(n)+"de "+str(maxits)

        n+=1

    #FUNCION AUN NO TRADUCIDA
    # applyNormalSpacing(grid, options)


def computeParams(grid, params, n):
    '''
    Calcula los parametros de A1, A2, A3, phi, psi
    '''

    imax = grid.imax
    jmax = grid.jmax
    srf1 = grid.surfbounds[0]
    srf2 = grid.surfbounds[1]
    params.A1 = params.A2 = params.A3 = params.phi = params.psi = np.zeros([imax,jmax])

    le = min(grid.x[:,0])
    chord = grid.x[srf1,0] - le

    for j in range(0,jmax,jmax-1):

        for i in range(imax-1):
            params.A1[i,j] = grid.xn[i,j]**2+ grid.yn[i,j]**2
            params.A2[i,j] = grid.xz[i,j] *grid.xn[i,j] +grid.yz[i,j] *grid.yn[i,j]
            params.A3[i,j]= grid.xz[i,j]**2 + grid.yz[i,j]**2

            if n == 1:
                if abs(grid.xz[i,j]) > abs(grid.yz[i,j]):
                    params.phi[i,j] = -grid.xzz[i,j]/grid.xz[i,j]
                elif abs(grid.yz[i,j])> 0.0:
                    params.phi[i,j] = -grid.yzz[i,j]/grid.yz[i,j]
                else:
                    params.phi[i,j] = 0.0

                if j==1 and i >= srf1 and i<= srf2:
                    params.phi[i,j]=0.0

    for i in range(0,imax,imax-1):

        for j in range(jmax):

            params.A1[i,j] = grid.xn[i,j]**2.0 + grid.yn[i,j]**2.0
            params.A2[i,j] = grid.xz[i,j]*grid.xn[i,j] + grid.yz[i,j]*grid.yn[i,j]
            params.A3[i,j] = grid.xz[i,j]**2.0 + grid.yz[i,j]**2.0

            if n == 1:
                if abs(grid.xn[i,j]) > abs(grid.yn[i,j] ):
                    params.psi[i,j] = -grid.xnn[i,j]/grid.xn[i,j]

                elif abs(grid.yn[i,j]) > 0.0:
                    params.psi[i,j] = -grid.ynn[i,j]/grid.yn[i,j]
                else:
                    params.psi[i,j] = 0.0

                if j != i and j != jmax:
                    params.phi[i,j]=0.0

            else:
                params.psi[i,j]=0.0

    for j in range(jmax):
        for i in range(imax):

            params.A1[i,j] = grid.xn[i,j]**2.0 + grid.yn[i,j]**2.0
            params.A2[i,j] = grid.xz[i,j]*grid.xn[i,j] + grid.yz[i,j]*grid.yn[i,j]
            params.A3[i,j] = grid.xz[i,j]**2.0 + grid.yz[i,j]**2.0

        if n == 1:
            params.phi[i,j] = params.phi[i,0] + float(j-1)/float(jmax-1) * (params.phi[i,jmax-1] - params.phi[i,1])

            params.psi[i,j] = params.psi[1,j] + float(i-1)/float(imax-1) * (params.psi[imax-1,j] - params.psi[0,j])


def updateOgrid(grid, params, j, variable, topcorner, botcorner):
    '''
    Modifica los valores de X y Y para obtener la Ogrid
    '''

    imax= grid.imax

    #matriz bidimensional
    Amat=np.zeros([imax,imax])
    Amat[imax-1,imax-1]=1.0
    Cvec = Bvec = np.zeros([imax])
    c=0.0

    if variable == 'x':
        Cvec[imax-1]= grid.x[0,j]
    else:
        Cvec[imax-1]=grid.y[0,j]

    for i in range(imax-1):

        b = params.A1[i,j]*(1.0 - 0.5*params.phi[i,j])
        d = -2.0*(params.A1[i,j] + params.A3[i,j])
        a = params.A1[i,j]*(1.0 + 0.50*params.phi[i,j])


        if variable == 'x' and i > 0:
            c = 0.50 * params.A2[i,j] * grid.x[i+1,j+1] - grid.x[i+1,j-1] - grid.x[i-1,j+1] + grid.x[i-1,j-1] - params.A3[i,j]*( 1.0 +  0.50 * params.psi[i,j] * grid.x[i,j+1] + 1.0 - 0.50 * params.psi[i,j] * grid.x[i,j-1])

        elif (variable == 'x') and (i == 0):

            c = 0.50 * params.A2[i,j]*(grid.x[i+1,j+1] - grid.x[i+1,j-1] - grid.x[imax-1,j+1] + grid.x[imax-1,j-1]) - params.A3[i,j]*((1.0 + 0.50*params.psi[i,j]) * grid.x[i,j+1] + (1.0 - 0.50*params.psi[i,j]) * grid.x[i,j-1])

        elif variable == 'y' and i > 0:

            c = 0.5 * params.A2[i,j]*(grid.y[i+1,j+1] - grid.y[i+1,j-1] - grid.y[i-1,j+1] + grid.y[i-1,j-1]) - params.A3[i,j] * ((1.0 + 0.5*params.psi[i,j]) * grid.y[i,j+1] + (1.0 - 0.50 * params.psi[i,j]) * grid.y[i,j-1])


        else:
            c = 0.50 * params.A2[i,j] * (grid.y[i+1,j+1] - grid.y[i+1,j-1] - grid.y[imax-1,j+1] +  grid.y[imax-1,j-1]) - params.A3[i,j]*((1.0 + 0.50 * params.psi[i,j])*grid.y[i,j+1] + (1.0 - 0.5*params.psi[i,j])*grid.y[i,j-1])

        if i == 1:
            Amat[i,imax-1] = b
        else:
            Amat[i,i-1] = b

            Amat[i,i]=d
            Amat[i,i+1]=a
            Cvec[i]=c

        #FUNCION AUN NO TRADUCIDA
        # Bcec= math_deps.tridiagMod(Amat, Cvec)

        if variable == 'x':
            grid.x[range(0,imax),j] = Bvec[range(0,imax)]
            grid.x[imax-1,j]=grid.x[1,j]

        else:
            grid.y[range(0,imax),j] = Bvec[range(0,imax)]
            grid.y[imax-1,j]=grid.y[1,j]

            if j == 2:
                if topcorner > 0 and botcorner > 0:
                    for i in range(topcorner,botcorner):
                        length = math.sqrt((grid.x[i,2] - grid.x[i,1]) ** 2 + (grid.y[i,2] - grid.y[i,1]) ** 2)
                        grid.x[i,2] = grid.x[i,1] + grid.surfnorm[i,1]*length
                        grid.y[i,2] = grid.y[i,1] + grid.surfnorm[i,1]*length
