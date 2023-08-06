# -*-coding:utf-8 -*-
 
"""
        * * * Module Akima Interpolation * * *
 
Ce module contient: 
	* la définition de la classe Signal : interpolation spatiale utilisant la méthode Akima développé sous fortran.


"""
from numpy import f2py
import os
import sys
import glob
# info
__version__ = "0.1"
__author__  = "G.Gassier and S.Meulé"
__date__    = "Janvier 2020"
 
#from Akima import Akima

# import subprocess
# result = subprocess.run(['./parentbash'], stdout=subprocess.PIPE)
# """ Import fortran files and compile them, then import it"""
# os.environ["PYTHONWARNINGS"] = "ignore"
#print(os.path.join(os.path.dirname(__file__)))
#(not glob.glob(os.path.join(os.path.dirname(__file__)),"*AKnew3*"))
#dirname=  os.path.dirname(__file__).split('/geoakima')[0]
#Fichier=glob.glob("*AKnew3*")
#Fic=dirname+"/"+Fichier[0]
directory=os.path.dirname(__file__).split('/geoakima')[0]
#import pdb; pdb.set_trace()
if (not(glob.glob(directory+"/*AKnew3*"))):
	print("............................................read")
	with open(os.path.join(os.path.dirname(__file__), 'src/akima.new.f'))as sourcefile:#open('Akima/src/akima.new.f')
			sourcecode1 = sourcefile.read()
	with open(os.path.join(os.path.dirname(__file__),'src/tripack.f') ) as sourcefilee:
			sourcecode2 = sourcefilee.read()
##                with open(os.path.join(os.path.dirname(__file__),'src/idbvip.f') ) as sourcefilee:
##                        sourcecode3 = sourcefilee.read()
	sourcecode=sourcecode1+sourcecode2#+sourcecode3
	# import subprocess
	# output = subprocess.check_output(['ls', '-1'])
	# save_stderr = sys.stderr
	# fh = open("errors.txt", "w")
	# sys.stdout = open('file.txt', 'w')
	saveerr = sys.stderr
	#sys.stderr= open('OutErr.txt', 'w')
	print("............................................Compile")
	#
	# warnings.filterwarnings("ignore", category=UserWarning, append=True)
	# warnings.simplefilter('ignore', UserWarning)
	dirname=  os.path.dirname(__file__).split('/geoakima')[0]
	#import pdb; pdb.set_trace()
	#print(dirname)
	
	
	f2py.compile(sourcecode,modulename='AKnew3', verbose=1)#, extra_args='--build-dir dirname' 
	Fichier=glob.glob("*AKnew3*")
	#print( Fichier)
	import shutil
	shutil.move(os.getcwd()+"/"+Fichier[0],dirname+"/"+Fichier[0])
	print("............................................Fin de Compile")
	#sys.stderr = saveerr
	# sys.stdout.close()
	# sys.stdout = sys.__stdout__
	# sys.stderr = save_stderr
	# fh.close()
###################################
