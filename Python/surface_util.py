"""
Funciones auxiliares para el procesamiento de las superficies
"""
import math
import numpy as np
from math_deps import derv1c, derv2c, derv1f, derv2f, derv1b, derv2b

def surfaceNormals(gridClass, j):
    """
    Obtiene las normales de la superficie
    grid -> instancia de GridClass
    j -> entero
    normals -> matriz -> [imax,2]
    """

    imax=gridClass.imax
    v= [0.0,0.0]
    length=0.0
    gridClass.surfnorm=np.zeros([imax,2])

    # # DEBUG:
    # print "gridClass.x: "
    # print gridClass.x[1,j]


    for k in range(imax):
        if k==0 or k == imax-1:
            v[0]=gridClass.x[1,j] - gridClass.x[-1,j]
            v[1]=gridClass.y[1,j] - gridClass.y[-1,j]

        else:
            v[0]=gridClass.x[k+1,j] - gridClass.x[k-1,j]
            v[1]=gridClass.y[k+1,j] - gridClass.y[k-1,j]

        length = math.sqrt(v[0]**2 + v[1]**2)

        # DEBUG:
        # print "\n length \n"
        # print length

        gridClass.surfnorm[k,0]=v[1]/length
        gridClass.surfnorm[k,1]=-v[0]/length


def computeInverseMetrics(grid, jacobian):
    """
    Funcion necesaria en ellipticGrid
    """
    grid.xz = grid.yz = grid.xzz = grid.yzz =grid.xn = grid.yn = grid.jac =  grid.xnn = grid.ynn =  np.zeros([grid.imax,grid.jmax])

    imax = grid.imax

    for j in range(1,grid.jmax-1):
        for i in range(1,grid.imax-1):

            #FUNCION AUN NO TRADUCIDA
            grid.xn[i,j]=derv1c(grid.x[i,j+1], grid.x[i,j-1], 1.0)
            grid.yn[i,j] = derv1c(grid.y[i,j+1], grid.y[i,j-1], 1.0)

            grid.xnn[i,j] = derv2c(grid.x[i,j+1], grid.x[i,j], grid.x[i,j-1], 1.0)
            grid.ynn[i,j] = derv2c(grid.y[i,j+1], grid.y[i,j], grid.y[i,j-1], 1.0)

            grid.xz[i,j] = derv1c(grid.x[i+1,j], grid.x[i-1,j], 1.0 )
            grid.yz[i,j] = derv1c(grid.y[i+1,j], grid.y[i-1,j], 1.0 )

            grid.xzz[i,j] = derv2c(grid.x[i+1,j], grid.x[i,j], grid.x[i-1,j], 1.0)
            grid.xzz[i,j] = derv2c(grid.y[i+1,j], grid.y[i,j], grid.y[i-1,j], 1.0)

    for i in range(0,imax, imax-1):
        for j in range(1, grid.jmax):
            if j>grid.xicut[1]:
                if i == 0:
                    grid.xz[i,j] = derv1f(grid.x[i+1,j], grid.x[i,j], 1.0 )
                    grid.yz[i,j] = derv1f(grid.y[i+1,j], grid.y[i,j], 1.0 )
                    derv2f(grid.x[i+2,j], grid.x[i+1,j], grid.x[i,j], 1.0, grid.xzz[i,j])
                    derv2f(grid.y[i+2,j], grid.y[i+1,j], grid.y[i,j], 1.0, grid.yzz[i,j])
                else:
                    derv1b(grid.x[i-1,j], grid.x[i,j], 1.0, grid.xz[i,j] )
                    derv1b(grid.y[i-1,j], grid.y[i,j], 1.0, grid.yz[i,j] )
                    derv2b(grid.x[i-2,j], grid.x[i-1,j], grid.x[i,j], 1.0, grid.xzz[i,j])
                    derv2b(grid.y[i-2,j], grid.y[i-1,j], grid.y[i,j], 1.0, grid.yzz[i,j] )

                if j < grid.jmax:
                    derv1c(grid.x[i,j+1], grid.x[i,j-1], 1.0, grid.xn[i,j] )
                    derv1c(grid.y[i,j+1], grid.y[i,j-1], 1.0, grid.yn[i,j] )
                    derv2c(grid.x[i,j+1], grid.x[i,j], grid.x[i,j-1], 1.0, grid.xnn[i,j] )
                    derv2c(grid.y[i,j+1], grid.y[i,j], grid.y[i,j-1], 1.0, grid.ynn[i,j] )
                else:
                    derv1b(grid.x[i,j-1], grid.x[i,j], 1.0, grid.xn[i,j])
                    derv1b(grid.y[i,j-1], grid.y[i,j], 1.0, grid.yn[i,j])
                    derv2b(grid.x[i,j-2], grid.x[i,j-1], grid.x[i,j], 1.0, grid.xnn[i,j])
                    derv2b(grid.y[i,j-2], grid.y[i,j-1], grid.y[i,j], 1.0, grid.ynn[i,j])

    j=0
    for i in range(grid.imax):
        grid.xn[i,j] = derv1f(grid.x[i,j+1], grid.x[i,j], 1.0)
        grid.yn[i,j] = derv1f(grid.y[i,j+1], grid.y[i,j], 1.0)
        grid.xnn[i,j] = derv2f(grid.x[i,j+2], grid.x[i,j+1], grid.x[i,j], 1.0)
        grid.ynn[i,j] = derv2f(grid.y[i,j+2], grid.y[i,j+1], grid.y[i,j], 1.0)

        if i > 0 and i < imax-1:
            grid.xz[i,j] = derv1c(grid.x[i+1,j], grid.x[i-1,j], 1.0)
            grid.yz[i,j] = derv1c(grid.y[i+1,j], grid.y[i-1,j], 1.0)
            grid.xzz[i,j] = derv2c(grid.x[i+1,j], grid.x[i,j], grid.x[i-1,j], 1.0 )
            grid.yzz[i,j] = derv2c(grid.y[i+1,j], grid.y[i,j], grid.y[i-1,j], 1.0 )

        elif (i == 0):
            grid.xz[i,j] = derv1f(grid.x[i+1,j], grid.x[i,j], 1.0 )
            grid.yz[i,j] = derv1f(grid.y[i+1,j], grid.y[i,j], 1.0 )
            grid.xzz[i,j] = derv2f(grid.x[i+2,j], grid.x[i+1,j], grid.x[i,j], 1.0 )
            grid.yzz[i,j] = derv2f(grid.y[i+2,j], grid.y[i+1,j], grid.y[i,j], 1.0 )

        else:
            grid.xz[i,j] = derv1b(grid.x[i-1,j], grid.x[i,j], 1.0 )
            grid.yz[i,j] = derv1b(grid.y[i-1,j], grid.y[i,j], 1.0 )
            grid.xzz[i,j] = derv2b(grid.x[i-2,j], grid.x[i-1,j], grid.x[i,j], 1.0 )
            grid.yzz[i,j] = derv2b(grid.y[i-2,j], grid.y[i-1,j], grid.y[i,j], 1.0 )

    j= grid.jmax-1
    for i in range(1,imax-2):
        grid.xz[i,j] = derv1c(grid.x[i+1,j], grid.x[i-1,j], 1.0 )
        grid.yz[i,j] = derv1c(grid.y[i+1,j], grid.y[i-1,j], 1.0 )
        grid.xzz[i,j] = derv2c(grid.x[i+1,j], grid.x[i,j], grid.x[i-1,j], 1.0)
        grid.yzz[i,j] = derv2c(grid.y[i+1,j], grid.y[i,j], grid.y[i-1,j], 1.0)

        grid.xn[i,j] = derv1b(grid.x[i,j-1], grid.x[i,j], 1.0)
        grid.yn[i,j] = derv1b(grid.y[i,j-1], grid.y[i,j], 1.0)
        grid.xnn[i,j] = derv2b(grid.x[i,j-2], grid.x[i,j-1], grid.x[i,j], 1.0)
        grid.ynn[i,j] = derv2b(grid.y[i,j-2], grid.y[i,j-1], grid.y[i,j], 1.0)

    i=0
    for j in range(grid.jmax):

        grid.xz[i,j] = derv1c(grid.x[i+1,j], grid.x[imax-2,j], 1.0)
        grid.yz[i,j] = derv1c(grid.y[i+1,j], grid.y[imax-2,j], 1.0)

        grid.xzz[i,j] = derv2c(grid.x[i+1,j], grid.x[i,j], grid.x[imax-2,j], 1.0)
        grid.yzz[i,j] = derv2c(grid.y[i+1,j], grid.y[i,j], grid.y[imax-2,j], 1.0)

        if j==0:
            grid.xn[i,j] = derv1f(grid.x[i,j+1], grid.x[i,j], 1.0 )
            grid.yn[i,j] = derv1f(grid.y[i,j+1], grid.y[i,j], 1.0 )

            grid.xnn[i,j] = derv2f(grid.x[i,j+2], grid.x[i,j+1], grid.x[i,j], 1.0 )
            grid.ynn[i,j] = derv2f(grid.y[i,j+2], grid.y[i,j+1], grid.y[i,j], 1.0 )

        elif j == grid.jmax-1:
            grid.xn[i,j] = derv1b(grid.x[i,j-1], grid.x[i,j], 1.0 )
            grid.yn[i,j] = derv1b(grid.y[i,j-1], grid.y[i,j], 1.0 )

            grid.xnn[i,j] = derv2b(grid.x[i,j-2], grid.x[i,j-1], grid.x[i,j], 1.0 )
            grid.ynn[i,j] = derv2b(grid.y[i,j-2], grid.y[i,j-1], grid.y[i,j], 1.0 )

        else:
            grid.xn[i,j] = derv1c(grid.x[i,j+1], grid.x[i,j-1], 1.0 )
            grid.yn[i,j] = derv1c(grid.y[i,j+1], grid.y[i,j-1], 1.0 )

            grid.xnn[i,j] = derv2c(grid.x[i,j+1], grid.x[i,j], grid.x[i,j-1], 1.0 )
            grid.ynn[i,j] = derv2c(grid.y[i,j+1], grid.y[i,j], grid.y[i,j-1], 1.0 )

        grid.xz[imax-1,j] = grid.xz[i,j]
        grid.yz[imax-1,j] = grid.yz[i,j]
        grid.xzz[imax-1,j] = grid.xzz[i,j]
        grid.yzz[imax-1,j] = grid.yzz[i,j]
        grid.xn[imax-1,j] = grid.xn[i,j]
        grid.yn[imax-1,j] = grid.yn[i,j]
        grid.xnn[imax-1,j] = grid.xnn[i,j]
        grid.ynn[imax-1,j] = grid.ynn[i,j]

    if jacobian:
        for i in range(grid.imax):
            for j in range(grid.jmax):
                grid.jac[i,j] = gridJacobian(grid.xz[i,j], grid.xn[i,j], grid.yz[i,j], grid.yn[i,j])

    # DEBUG: imprime el jacobiano
    # print grid.jac

def gridJacobian(xz, xn, yz, yn):
    return 1.0/(xz*yn-xn*yz)
