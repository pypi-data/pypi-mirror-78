# coding: utf-8

from shapely.ops import cascaded_union, polygonize,unary_union,polygonize_full
from matplotlib.collections import LineCollection
from scipy.spatial import distance_matrix
import shapely.geometry as geometry
from descartes import PolygonPatch
from scipy.spatial import Delaunay
from shapely.geometry import Point, MultiPoint, MultiLineString, MultiPolygon, box
import matplotlib.pyplot as plt
from matplotlib import cm
import itertools
from numpy import f2py
import pandas as pd
import pylab as py
import numpy as np
import warnings
import glob
import math
import sys
import os
import re
from scipy.interpolate import SmoothBivariateSpline,RectBivariateSpline


################################################################################################################################# 
class geoakima:
        def __init__(self):
            self.filename=None
            self.Directory=None
            os.environ["PYTHONWARNINGS"] = "ignore"
            warnings.filterwarnings("ignore", category=UserWarning, append=True)
            print('version package')
            #self.compilefortran()
################################################################################################################################# 
        def compilefortran(self):
            # import subprocess
            # result = subprocess.run(['./parentbash'], stdout=subprocess.PIPE)
            # """ Import fortran files and compile them, then import it"""
            # os.environ["PYTHONWARNINGS"] = "ignore"
            #print(os.path.join(os.path.dirname(__file__)))
            #(not glob.glob(os.path.join(os.path.dirname(__file__)),"*AKnew3*"))
            if (True==True):
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
                #import pdb; pdb.set_trace()print(dirname)
                
                
                f2py.compile(sourcecode,modulename='AKnew3', verbose=1)#, extra_args='--build-dir dirname' 
                #import pdb; pdb.set_trace()
                Fichier=glob.glob("*AKnew3*")
                #print( Fichier)
                import shutil
                shutil.move(os.getcwd()+"/"+Fichier[0],dirname+"/"+Fichier[0])
                #print("............................................Fin de Compile")
                sys.stderr = saveerr
                # sys.stdout.close()
                # sys.stdout = sys.__stdout__
                # sys.stderr = save_stderr
                # fh.close()
###################################
        def read(self,filename= os.path.join(os.path.dirname(__file__), './DataTrain.txt'),px=1,py=2,pz=3) :

            '''Open ascii data file with pandas and read data'''

            message='{:.<40}{:.>20}'.format('Read ascii file (using pandas):', 'running')
            print (message)
            contenu=pd.read_csv(filename,sep='\t+|,',names=([ 'X', 'Y', 'Z']),skiprows=[0],engine='python')#,usecols = [px,py,pz]
            contenu=contenu.dropna()
            NbLine=len(contenu)
            # Eliminate duplicates
            contenu=contenu.drop_duplicates(subset=['X','Y'], keep='first', inplace=False)
            co=len(contenu)
            if(filename==os.path.join(os.path.dirname(__file__), './DataTrain.txt')):
                self.filename='DataTrain.txt'
            else:
                self.filename = filename
                
            self.outputfolder=self.filename[:-4]+'_Output'
            try:
                os.mkdir(self.outputfolder)
            except: 
                pass

            # attributes x,y,z
            self.x=np.transpose(contenu.X.values[np.newaxis])
            self.y=np.transpose(contenu.Y.values[np.newaxis])
            self.z=np.transpose(contenu.Z.values[np.newaxis])


            # Writes a output file
##                df=pd.DataFrame({'X': contenu.X, 'Y': contenu.Y, 'Z':contenu.Z})
##                df.to_csv(self.filename+'.npy', sep = ',')
            m=np.amax(self.z)

            # Output messages
            message='{:.<40}{:.>20}'.format(filename, 'Ok')
            print (message)
            message='{:.<40}{:.>20}'.format('Number of data lines: ', NbLine-1)
            print (message)
            message='{:.<40}{:.>20}'.format('Number of identical lines suppressed: ', NbLine-co)
            print (message)
            message='{:.<40}{:.>20}'.format('Maximum of altimetry: ', m)
###################################
        def alpha_shape(self):
            """
            Compute the alpha shape (concave hull) of a set of points.
            """


            coords = np.concatenate((self.x, self.y), axis=1)
            tri = Delaunay(coords)
            edges = set()
            edge_points = []

            # Loop over triangles
            for ia, ib, ic in tri.vertices:
                pa = coords[ia]
                pb = coords[ib]
                pc = coords[ic]

                # Lengths of sides of triangle
                a = math.sqrt((pa[0] - pb[0])**2 + (pa[1] - pb[1])**2)
                b = math.sqrt((pb[0] - pc[0])**2 + (pb[1] - pc[1])**2)
                c = math.sqrt((pc[0] - pa[0])**2 + (pc[1] - pa[1])**2)

                # Semiperimeter of triangle
                s = (a + b + c) * 0.5

                # Area of triangle by Heron's formula
                # Precompute value inside square root to avoid unbound math error in case of 
                # 0 area triangles. 
                area = s * (s - a) * (s - b) * (s - c)
                
                if area > 0:
                    area = math.sqrt(area)
                    
                    # Radius Filter
                    if a * b * c / (4.0 * area) < self.rayonZone:
                        for i, j in itertools.combinations([ia, ib, ic], r=2):
                            if (i, j) not in edges and (j, i) not in edges:
                                edges.add((i, j))
                                edge_points.append(coords[[i, j]])

            # Create the resulting polygon from the edge points
            m = MultiLineString(edge_points)
            triangles = list(polygonize(m))
            result = cascaded_union(triangles)


             # Output figure
           
            fig1 = plt.figure(figsize=(10,10))
            ax = fig1.add_subplot(111)
            margin = .3            
            x_min, y_min, x_max, y_max = result.bounds
            ax.set_xlim([x_min-margin, x_max+margin])
            ax.set_ylim([y_min-margin, y_max+margin])
            patch = PolygonPatch(result, fc='#999999',
                                         ec='#000000', fill=True,
                                         zorder=-1)
            ax.add_patch(patch)
            plt.plot(self.x,self.y,'o', color='#f16824',alpha=0.1 )
            #plt.gca().add_collection(LineCollection())
            titre='Concave Hull, distance: ' + str(self.rayonZone)
            plt.title(titre)
            st=self.outputfolder+'/'+titre+'.png'
            fig1.savefig(st)
            message='{:.<40}{:.>20}'.format('Alpha Shape', 'Ok')
            print (message)
            return result, edge_points

            


###################################
        def alpha_shape_opt(self):
            """
            Compute the alpha shape (concave hull) of a set
            of points.
            """

            coords = np.concatenate((self.x, self.y), axis=1)
            if len(coords) < 4:
                # When you have a triangle, there is no sense
                # in computing an alpha shape.
                return geometry.MultiPoint(list(points)).convex_hull          
            tri = Delaunay(coords)
            
            triangles = coords[tri.vertices]
            a = ((triangles[:,0,0] - triangles[:,1,0]) ** 2 + (triangles[:,0,1] - triangles[:,1,1]) ** 2) ** 0.5
            b = ((triangles[:,1,0] - triangles[:,2,0]) ** 2 + (triangles[:,1,1] - triangles[:,2,1]) ** 2) ** 0.5
            c = ((triangles[:,2,0] - triangles[:,0,0]) ** 2 + (triangles[:,2,1] - triangles[:,0,1]) ** 2) ** 0.5
            
            s = ( a + b + c ) / 2.0
            areas = np.sqrt(s*(s-a)*(s-b)*(s-c))
            circums = a * b * c / (4.0 * areas)            
            #indi=np.where((a<self.rayonZone)&(b<self.rayonZone)&(c<self.rayonZone)|(circums < self.rayonZone/2))
            indi=np.where((areas>0)&(circums < self.rayonZone))
            #indi=np.where(circums < self.rayonZone)
            filtered = triangles[indi]
            edge1 = filtered[:,(0,1)]
            edge2 = filtered[:,(1,2)]
            edge3 = filtered[:,(2,0)]                
            edge_points = np.concatenate([edge1,edge2,edge3], axis=0).tolist()
            m = geometry.MultiLineString(edge_points)     
            triangles = list(polygonize(filtered))
            polygon= cascaded_union(triangles)
            
            # Output figure
           
            fig1 = plt.figure(figsize=(10,10))
            ax = fig1.add_subplot(111)
            margin = .3            
            x_min, y_min, x_max, y_max = polygon.bounds
            ax.set_xlim([x_min-margin, x_max+margin])
            ax.set_ylim([y_min-margin, y_max+margin])
            patch = PolygonPatch(polygon, fc='#999999',
                                         ec='#000000', fill=True,
                                         zorder=-1)
            ax.add_patch(patch)
            plt.plot(self.x,self.y,'o', color='#f16824',alpha=0.1 )
            plt.gca().add_collection(LineCollection(filtered))
            titre='Concave Hull, distance: ' + str(self.rayonZone)
            plt.title(titre)
            st=self.outputfolder+'/'+titre+'.png'
            fig1.savefig(st)
            message='{:.<40}{:.>20}'.format('Alpha Shape', 'Ok')
            print (message)
            return polygon, edge_points

###################################
        def DomaineInterpolation(self):
            # Create the grid for interpolation from min x,y to max x,y with a spatial step deltaxy
            Xmin=int(np.min(self.x))
            Xmax=int(np.max(self.x))
            Ymin=int(np.min(self.y))
            Ymax=int(np.max(self.y))
            self.nbx_interpol=int((Xmax-Xmin)/self.deltaxy)
            self.nby_interpol=int((Ymax-Ymin)/self.deltaxy)
            xInt= np.arange(Xmin,Xmax,self.deltaxy)
            yInt= np.arange(Ymin,Ymax,self.deltaxy)
            xv,yv=np.meshgrid(xInt, yInt)
            self.xInt=np.expand_dims(xv.flatten(),axis=0).T
            self.yInt=np.expand_dims(yv.flatten(),axis=0).T
            self.zInt=np.array([np.zeros(len(self.xInt))]).T

            # Output messages
            message='{:.<40}{:.>20}'.format('Interpolated Grid', 'Ok')
            print (message)
###################################
        def AjoutPointReferenceContour(self):
            #------------------------------------------
            # From a alpha shape method, keep the point to be interpolated
            # see shapely et hull concave
            #------------------------------------------
            #
            concave_hull, edge_points = self.alpha_shape()
            #concave_hull, edge_points = self.alpha_shape_opt()
            #
            Grille=np.concatenate((self.xInt,self.yInt,self.zInt),axis=1)
            Grillexy=np.concatenate((self.xInt,self.yInt),axis=1)

            # Test to get point only inside the concave hull polygon:
            xc=[]
            yc=[]
            maskz=[]
            masq=[]
            testz=[]
            for xyint in Grille:
                    pointgrille = Point(xyint[0],xyint[1])
                    if concave_hull.contains(pointgrille)==True:
                            xc.append(pointgrille.x)
                            yc.append(pointgrille.y)
                            maskz.append(xyint[2])
                            masq=np.append(masq,1)
                            testz.append(xyint[2])

                    else:
                            masq=np.append(masq,0)
                            testz.append(np.nan)              

            self.xIntc =np.array(np.expand_dims(np.asarray(xc), axis=0).T, dtype='f8', order='F')#
            self.yIntc = np.array(np.expand_dims(np.asarray(yc), axis=0).T, dtype='f8', order='F')#
            self.zIntc = np.array(np.expand_dims(np.asarray(maskz), axis=0).T, dtype='f8', order='F')#
            self.maskz= np.array(np.expand_dims(np.asarray(masq), axis=0).T, dtype='f8', order='F')#
            self.testz= np.array(np.expand_dims(np.asarray(testz), axis=0).T, dtype='f8', order='F')#

            # Output figures
            fig1 = plt.figure(figsize=(10,10))
            ax = fig1.add_subplot(111)
            plt.plot(self.xIntc, self.yIntc, 'o')
            # plt.show()
            # Output messages
            message='{:.<40}{:.>20}'.format('Concave Hull', 'Ok')
            print (message)
###################################
        def Akima(self,deltaxy = 5,rayonZone=30):
            

            self.deltaxy=deltaxy
            self.rayonZone=rayonZone
            #self.compilefortran()
            self.DomaineInterpolation()
            self.AjoutPointReferenceContour()     
            #import pdb; pdb.set_trace()      
            import AKnew3
            Xmin=int(np.min(self.x))
            Xmax=int(np.max(self.x))
            Ymin=int(np.min(self.y))
            Ymax=int(np.max(self.y))
        
            self.x = np.array(self.x, dtype='f8', order='F')
            self.y = np.array(self.y, dtype='f8', order='F')
            self.z = np.array(self.z, dtype='f8', order='F')

            nbrx=int((Xmax-Xmin)/self.deltaxy)
            nbry=int((Ymax-Ymin)/self.deltaxy)

            MD = 1         
            WK = np.array(np.zeros((self.x.shape[0], 17)), dtype='f8', order='F')           
            IWK = np.array(np.zeros((self.x.shape[0], 25)), dtype='f8', order='F')
            extrpi =np.array(np.zeros(self.xIntc.shape[0]), dtype='f8', order='F')
            near = np.array(np.zeros((self.x.shape[0])), dtype='f8', order='F')
            nex = np.array(np.zeros((self.x.shape[0])), dtype='f8', order='F')
            dist =np.array(np.zeros((self.x.shape[0])), dtype='f8', order='F')
            IER=0
            ########################################################################################## 
            # CALL SDBI3P:  * This subroutine performs bivariate interpolation when the data
            #               * points are scattered in the x-y plane.  It is based on the
            #               * revised Akima method that has the accuracy of a cubic (third-
            #               * degree) polynomial.
            ########################################################################################## 
            message='{:.<40}{:.>20}'.format('Akima method sdbi3p', 'running')
            print (message)
            AKnew3.sdbi3p(MD, self.x, self.y, self.z, self.xIntc, self.yIntc, self.zIntc, IER, WK, IWK, extrpi, near, nex,  dist)


            ########################################################################################## 
            # CALL IDBVIP:  * THIS SUBROUTINE PERFORMS BIVARIATE INTERPOLATION WHEN THE PRO-
            #               * JECTIONS OF THE DATA POINTS IN THE X-Y PLANE ARE IRREGULARLY
            #               * DISTRIBUTED IN THE PLANE.     
            ########################################################################################## 
##            AKnew3.idbvip(MD,NCP,NDP,self.x, self.y, self.z, self.xIntc, self.yIntc, self.zIntc,I,IWK,WK)
##            message='{:.<40}{:.>20}'.format('Akima method idbvip', 'Ok')
##            print (message)
            
###################################         
        def filter(self):
           self.zfilter()
           #self.SmoothBivariateSpline()
###################################
        def zfilter(self):
           self.zIntc[np.where((self.zIntc<np.min(self.z)) | (self.zIntc>np.max(self.z)))]=np.nan
           self.xIntc[np.where((self.zIntc<np.min(self.z)) | (self.zIntc>np.max(self.z)))]=np.nan
           self.yIntc[np.where((self.zIntc<np.min(self.z)) | (self.zIntc>np.max(self.z)))]=np.nan
           self.maskz[np.where((self.zIntc<np.min(self.z)) | (self.zIntc>np.max(self.z)))]=np.nan
           message='{:.<40}{:.>20}'.format('Filter akima interpolation', 'Ok')
           print (message)
                
###################################       
        def SmoothBivariateSpline(self):
                message='{:.<40}{:.>20}'.format('Smooth Bivariate Spline', 'running')
                print (message)
                kx = 2
                ky = 2              
                s=2000
                fit = SmoothBivariateSpline( self.x, self.y, self.z, kx=kx, ky=ky,s=s)
                self.zIntc = fit(self.xIntc, self.yIntc,grid=False)  # .T ??
                message='{:.<40}{:.>20}'.format('Smooth Bivariate Spline', 'Ok')
                print (message)
                #import pdb; pdb.set_trace()
               
#########################################################################################              
#################################################################################################################################                  
        def output(self):
           os.chdir(self.outputfolder+'/')
           self.outputlog()
           self.RepresentationData()
           self.RepresentationInterpole()
           self.export_asciigrid()
           self.export_shp()
#########################################################################################   

        def outputlog(self):                
            outname = self.outputfolder+"_log.txt"
            with open(outname, "w") as outfile:
                    message='{:.<40}{:.>20}'.format('Fortran Compilation', 'Ok')
                    outfile.write(message+"\n")                   
                    message='{:.<40}{:.>20}'.format(self.filename, 'Ok')
                    outfile.write (message+"\n")
                    message='{:.<40}{:.>20}'.format('dx=dy', self.deltaxy)
                    outfile.write  (message+"\n")    
                    message='{:.<40}{:.>20}'.format('Radius area', self.rayonZone)
                    outfile.write  (message+"\n")                    
                    message='{:.<40}{:.>20}'.format('Alpha Shape', 'Ok')
                    outfile.write (message+"\n")
                    message='{:.<40}{:.>20}'.format('Interpolated Grid', 'Ok')
                    outfile.write (message+"\n")
                    message='{:.<40}{:.>20}'.format('Concave Hull', 'Ok')
                    outfile.write (message+"\n")
                    message='{:.<40}{:.>20}'.format('Akima method sdbi3p', 'Ok')
                    outfile.write (message+"\n")
                    message='{:.<40}{:.>20}'.format('Figures', 'Ok')
                    outfile.write (message+"\n")
                    message='{:.<40}{:.>20}'.format('Akima figures', 'Ok')
                    outfile.write (message+"\n")
                    message='{:.<40}{:.>20}'.format('Export ascii', 'Ok')
                    outfile.write (message+"\n")
                    message='{:.<40}{:.>20}'.format('Export shp for GIS', 'Ok')
                    outfile.write (message+"\n")
                    message='{:.<40}{:.>20}'.format('Filter akima interpolation', 'Ok')
                    outfile.write (message+"\n")
                
#########################################################################################   

        def RepresentationData(self) :                
            fig1 = plt.figure()
            ax1 = plt.subplot(111)
            plt.scatter(self.x,self.y,c=self.z,cmap='terrain')
            plt.colorbar()
            #plt.contour(self.x,self.y,self.z, levels=[245], colors='black')
            plt.title('Data GPS')
            namefig=self.outputfolder+'_Data.png'
            fig1.savefig(namefig)
            message='{:.<40}{:.>20}'.format('Figures', 'Ok')
            print (message)
#########################################################################################   

        def RepresentationInterpole(self):
                
            cmap=cm.terrain
            colors_undersea = plt.cm.terrain(np.linspace(0, 0.17, 50))
            colors_land = plt.cm.terrain(np.linspace(0.25, 1, 50))
            colors = np.vstack((colors_undersea, colors_land))
            cma = cmap.from_list('Custom cmap', colors, cmap.N)

            bounds = np.linspace(np.floor(np.min(self.z)),np.round(np.max(self.z)),100)
            nor = cm.colors.BoundaryNorm(bounds, cmap.N)
            fig1 = plt.figure()
            ax1 = plt.subplot(111)
            plt.scatter(self.xIntc,self.yIntc,c=self.zIntc,cmap=cma, norm=nor, alpha=0.5)#10*np.log(,cmap='terrain'terrain', edgecolor=''
            plt.colorbar()
            namefig=self.outputfolder+'_InterpolationAkima.png'
            plt.title('Akima Interpolation')
            fig1.savefig(namefig)

            message='{:.<40}{:.>20}'.format('Akima figures', 'Ok')
            print (message)
                

#########################################################################################   
        

        def export_asciigrid(self):            
                
            outname = self.outputfolder+"_raster.asc"
            xllcorner = int(min(self.xInt))
            yllcorner = int(min(self.yInt))
            cellsize = int(self.deltaxy)
            ncols = int((np.max(self.xInt)-np.min(self.xInt))/cellsize +1)
            nrows = int((np.max(self.yInt)-np.min(self.yInt))/cellsize +1)
            nodataval = int(-9999)
            
                
            arr=np.copy(np.array(self.maskz))
            locnodata=np.where(arr==0)
            locdata=np.where(arr==1)
            arr[locnodata[0]]=int(nodataval)
            arr[locdata[0]]=self.zIntc.astype(float)
            Zout=arr.reshape(nrows, ncols)
            Zout=np.flipud(Zout)

            # write the header and grid to an ascii file
            with open(outname, "w") as outfile:

                # write ascii raster header
                outfile.write("ncols " + str(int(ncols))+ "\n")
                outfile.write("nrows " + str(int(nrows))+ "\n")
                outfile.write("xllcorner " + str(xllcorner) + "\n")
                outfile.write("yllcorner " + str(yllcorner) + "\n")
                outfile.write("cellsize " + str(cellsize) + "\n")
                outfile.write("nodata " + str(nodataval) + "\n")

                # write grid to outfile
                np.savetxt(outfile,Zout, fmt='%1.2f', delimiter= " ")
                #
                #Zout.tofile(outfile,sep=" ", format="%s")
            message='{:.<40}{:.>20}'.format('Export ascii', 'Ok')
            print (message)

#########################################################################################   

        def export_shp(self):            
            from shapely.geometry import Point
            import geopandas as gpd
            filename =self.filename#"./Output/DataTrain.txt"#
            outname =filename[:-3]+'shp'#"DataTrain.shp"#
            crs = {'init': 'epsg:32705'}
            datainterpolated=np.concatenate((self.xIntc,self.yIntc,self.zIntc),axis=1)
            df=pd.DataFrame(datainterpolated, columns=['X', 'Y', 'Z'])
            df['geometry'] = df.apply(lambda row: Point(row.X,row.Y,row.Z),axis=1)
            #df = df.drop(['X', 'Y', 'Z'], axis=1)
            geometry = [Point(xyz) for xyz in zip(self.xIntc, self.yIntc,self.zIntc)]
            gdf = gpd.GeoDataFrame(df, geometry = df.geometry)
            gdf.to_file(outname)
            message='{:.<40}{:.>20}'.format('Export shp for GIS', 'Ok')
            print (message)

#################################################################################################################################         
        def concavehullk(self):
            # IN DEV: NOT FINISHED AT ALL    
            """
            Calculates a valid concave hull polygon containing all given points. The algorithm searches for that
            point in the neighborhood of k nearest neighbors which maximizes the rotation angle in clockwise direction
            without intersecting any previous line segments.
            This is an implementation of the algorithm described by Adriano Moreira and Maribel Yasmina Santos:
            CONCAVE HULL: A K-NEAREST NEIGHBOURS APPROACH FOR THE COMPUTATION OF THE REGION OCCUPIED BY A SET OF POINTS.
            GRAPP 2007 - International Conference on Computer Graphics Theory and Applications; pp 61-68.
            :param points_list: list of tuples (x, y)
            :param k: integer
            :return: list of tuples (x, y)
            """
            points_list = np.concatenate((self.x, self.y), axis=1)
            k=3
            hull=[]
            
            # return an empty list if not enough points are given
            if k > len(points_list):
                return None

            # the number of nearest neighbors k must be greater than or equal to 3
            # kk = max(k, 3)
            kk = max(k, 2)

            # start with the point having the smallest y-coordinate (most southern point)
            ia,ib=np.where(points_list==np.min(points_list))
            first_point = points_list[ia]

            # add this points as the first vertex of the hull
            hull = [first_point]

            # make the first vertex of the hull to the current point
            current_point = first_point

            # remove the point from the point_set, to prevent him being among the nearest points
            
            
            point_set = np.delete(points_list, (ia), axis=0)
            previous_angle = np.pi

            # step counts the number of segments
            step = 2
            # as long as point_set is not empty or search is returning to the starting point
            while (current_point != first_point) or (step == 2) and (len(point_set) > 0):

                # after 3 iterations add the first point to point_set again, otherwise a hull cannot be closed
                if step == 5:
                    point_set = add_point(point_set, first_point)

                # search the k nearest neighbors of the current point
                k_nearest_points = nearest_points(point_set, current_point, kk)

                # sort the candidates (neighbors) in descending order of right-hand turn. This way the algorithm progresses
                # in clockwise direction through as many points as possible
                c_points = sort_by_angle(k_nearest_points, current_point, previous_angle)

                its = True
                i = -1

                # search for the nearest point to which the connecting line does not intersect any existing segment
                while its is True and (i < len(c_points)-1):
                    i += 1
                    if c_points[i] == first_point:
                        last_point = 1
                    else:
                        last_point = 0
                    j = 2
                    its = False

                    while its is False and (j < len(hull) - last_point):
                        its = intersect((hull[step-2], c_points[i]), (hull[step-2-j], hull[step-1-j]))
                        j += 1

                # there is no candidate to which the connecting line does not intersect any existing segment, so the
                # for the next candidate fails. The algorithm starts again with an increased number of neighbors
                if its is True:
                    return concave_hull(points_list, kk + 1)

                # the first point which complies with the requirements is added to the hull and gets the current point
                current_point = c_points[i]
                hull = add_point(hull, current_point)

                # calculate the angle between the last vertex and his precursor, that is the last segment of the hull
                # in reversed direction
                previous_angle = angle(hull[step - 1], hull[step - 2])

                # remove current_point from point_set
                point_set = remove_point(point_set, current_point)

                # increment counter
                step += 1

            all_inside = True
            i = len(point_set)-1

            # check if all points are within the created polygon
            while (all_inside is True) and (i >= 0):
                all_inside = point_in_polygon_q(point_set[i], hull)
                i -= 1

            # since at least one point is out of the computed polygon, try again with a higher number of neighbors
            if all_inside is False:
                return concave_hull(points_list, kk + 1)

            # a valid hull has been constructed



               


                
