from qgis.gui import *
from qgis.core import *
def find_layer(layer_name):
	# print "find_layer(" + str(layer_name) + ")"

	for name, search_layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
		# print unicode(search_layer.name()) + " ?= " + unicode(layer_name)
		if search_layer.name() == layer_name:
			return search_layer

	return None
	
def extractPoints(geom):
	points = []
	if geom.wkbType() == QgsWkbTypes.Point:
	#	if geom.isMultipart():
		points = geom.asPoint()
	elif geom.wkbType()== QgsWkbTypes.MultiPoint:
		points.append(geom.asMultiPoint())
	elif geom.wkbType() == QgsWkbTypes.MultiLineString:
		#if geom.isMultipart():
		lines = geom.asMultiPolyline()
		for line in lines:
			points.extend(line)
	elif geom.wkbType()==QgsWkbTypes.LineString:
			points = geom.asPolyline()
	elif geom.wkbType() == QgsWkbTypes.MultiPolygon:
		#if geom.isMultipart():
		polygons = geom.asMultiPolygon()
		#points=geom.asMultiPolygon()
		for poly in polygons:
			for line in poly:
				points.extend(line)
	elif geom.wkbType()==QgsWkbTypes.Polygon:
		polygon = geom.asPolygon()
		for line in polygon:
			points.extend(line)
	return points
		
def features(layer):

	class Features:

		def __init__(self, layer):
			self.layer = layer
			self.selection = False
			self.iter = layer.getFeatures()
			selected = layer.selectedFeatures()
			if len(selected) > 0:
				self.selection = True
				self.iter = iter(selected)

		def __iter__(self):
			return self.iter

		def __len__(self):
			if self.selection:
				return int(self.layer.selectedFeatureCount())
			else:
				return int(self.layer.featureCount())

	return Features(layer)
