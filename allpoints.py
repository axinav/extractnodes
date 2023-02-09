from qgis.gui import *
from qgis.core import *
from qgis.PyQt.QtCore import *
from .vectortools import *
import os.path
class allPoints:
	def __init__(self, layername):
		self.layername=layername
		
		
	def processAlgorithm(self, isNew):
		#layer = find_layer(self.layername)
		layer = self.layername
		inputlayerName=layer.name()
		pr=layer.dataProvider()
		pathe=pr.dataSourceUri(True)
		dUrl=os.path.dirname(pathe.split("|")[0])+"/allpoints.shp"
		
		
				
		outFeat = QgsFeature()
		inGeom = QgsGeometry()
		outGeom = QgsGeometry()
		outFields=QgsFields()
		outFields.append(QgsField("layername",QVariant.String))
		outFields.append(QgsField("pointname",QVariant.String))
		outFeat.setFields(outFields)
		outFeat.setAttribute("layername", layer.name())
		transform_context =QgsProject.instance().transformContext()
		save_options = QgsVectorFileWriter.SaveVectorOptions()
		save_options.driverName = "ESRI Shapefile"
		save_options.fileEncoding = "UTF-8"
		
		writer=QgsVectorFileWriter.create(dUrl, outFields, QgsWkbTypes.Point, layer.crs(), transform_context, save_options)


		
		Features =features(layer)
		uniquelist=[]
		for f in Features:
			inGeom = f.geometry()
			points =extractPoints(inGeom)
			lcoord = map(lambda p: (p.x(), p.y()), points)

			for p in lcoord:
				if p not in uniquelist:
					uniquelist.append(p)

            #luniquecoords.update(lcoord)

		for i in uniquelist:
			outFeat.setGeometry(outGeom.fromPointXY(QgsPointXY(i[0],i[1])))
                #print outFeat.attribute("layername")
			writer.addFeature(outFeat)

				
		del writer
		

	def processAlgorithm2(self, pntlayer):
		layer = self.layername
		inputlayerName=layer.name()
		
		outFeat = QgsFeature()
		inGeom = QgsGeometry()
		outGeom = QgsGeometry()
		pntL = pntlayer
        #pntL.startEditing()
		dp = pntL.dataProvider()

		outFields=QgsFields()
		listFields = map(lambda field: field.name(), dp.fields().toList())
		if "layername" not in listFields:
			outFields.append(QgsField("layername", QVariant.String))
		if "pointname" not in listFields:
			outFields.append(QgsField("pointname", QVariant.String))
		dp.addAttributes(outFields)
		pntL.commitChanges()
		existFields = dp.fields()
		pntL.startEditing()



		outFeat.setFields(existFields)
		outFeat.setAttribute("layername", layer.name())


		existPnts=features(pntL)
		existcoords=set(map(lambda f: (f.geometry().asPoint().x(),f.geometry().asPoint().y()),existPnts))
		allcoords=existcoords.copy()



		Features =features(layer)
		uniquelist = []
		for f in Features:
			inGeom = f.geometry()


			points =extractPoints(inGeom)
			lcoord=map(lambda p:(p.x(),p.y()),points)
            #allcoords.update(lcoord)
			for p in lcoord:
				if p not in allcoords:
					allcoords.add(p)
					uniquelist.append(p)
            #allcoords.update(lcoord)

        #noExist=allcoords.difference(existcoords)


		for i in uniquelist:
			outFeat.setGeometry(outGeom.fromPointXY(QgsPointXY(i[0],i[1])))
			pntL.addFeature(outFeat)
		pntL.commitChanges()
				
if __name__=="__main__":
	import sys
	import os.path
	from qgis.gui import *
	from qgis.core import *
	from qgis.PyQt.QtCore import *
	aps=QgsApplication([],False)
	#(sys.argv,False,'desktop')
	aps.initQgis()

	vlayer = QgsVectorLayer("/home/alex/coding/1-1.shp", "layer_name_you_like", "ogr")
	vlayername=vlayer.name()
	#points=[]
	#for f in features(vlayer):
	#	points=extractPoints(f.geometry())

	#print(f.geometry().asWkt())
	#print(points)
	aPoints=allPoints(vlayer)

	newlayer=True
	aPoints.processAlgorithm(newlayer)

            
            
				

