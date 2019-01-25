"""
Automatiza todo el pipeline de I/O
"""

def createSH(rootPath, file, profileSize):
    f=open(rootPath+"/Python/mayn.sh","w+")

    f.write( "#!/usr/bin\n")
    f.write( "#CAM- variable que se tiene que llenar dinamicamente -directorio de trabajo\n")
    f.write( "CAM="+rootPath+"\n")
    f.write( "#FI - variable que se tiene que llenar dinamicamente -nombre del archivo\n")
    f.write( "FI="+file+".dat\n")
    f.write( "cd $CAM\n")
    f.write( "./wiuwiu $CAM/sample_airfoils/$FI\n")
    f.write( "mkdir -p $CAM/renders\n")
    f.write( "mv $CAM/*.p3d $CAM/renders\n")
    f.write( "mv $CAM/*.nmf $CAM/renders\n")
    # f.write( "cd $CAM/renders\n")
    f.write( "python $CAM/Python/visualizeGrid.py "+file+"\n")

    f.close()
