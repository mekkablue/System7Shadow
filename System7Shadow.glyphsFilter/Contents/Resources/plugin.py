# encoding: utf-8

###########################################################################################################
#
#
#	Filter with dialog Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20with%20Dialog
#
#	For help on the use of Interface Builder:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc, math

from GlyphsApp import *
from GlyphsApp.plugins import *
from AppKit import NSAffineTransform, NSAffineTransformStruct
from Foundation import NSClassFromString

def offsetLayer( thisLayer, offsetX, offsetY, makeStroke=False, position=0.5, autoStroke=False ):
	offsetFilter = NSClassFromString("GlyphsFilterOffsetCurve")
	offsetFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_error_shadow_(
		thisLayer,
		offsetX, offsetY, # horizontal and vertical offset
		makeStroke,       # if True, creates a stroke
		autoStroke,       # if True, distorts resulting shape to vertical metrics
		position,         # stroke distribution to the left and right, 0.5 = middle
		None, None )



def transform(shiftX=0.0, shiftY=0.0, rotate=0.0, skew=0.0, scale=1.0):
	"""
	Returns an NSAffineTransform object for transforming layers.
	Apply an NSAffineTransform t object like this:
		Layer.transform_checkForSelection_doComponents_(t,False,True)
	Access its transformation matrix like this:
		tMatrix = t.transformStruct() # returns the 6-float tuple
	Apply the matrix tuple like this:
		Layer.applyTransform(tMatrix)
		Component.applyTransform(tMatrix)
		Path.applyTransform(tMatrix)
	Chain multiple NSAffineTransform objects t1, t2 like this:
		t1.appendTransform_(t2)
	"""
	myTransform = NSAffineTransform.transform()
	if rotate:
		myTransform.rotateByDegrees_(rotate)
	if scale != 1.0:
		myTransform.scaleBy_(scale)
	if not (shiftX == 0.0 and shiftY == 0.0):
		myTransform.translateXBy_yBy_(shiftX,shiftY)
	if skew:
		skewStruct = NSAffineTransformStruct()
		skewStruct.m11 = 1.0
		skewStruct.m22 = 1.0
		skewStruct.m21 = math.tan(math.radians(skew))
		skewTransform = NSAffineTransform.transform()
		skewTransform.setTransformStruct_(skewStruct)
		myTransform.appendTransform_(skewTransform)
	return myTransform


class System7Shadow(FilterWithDialog):
	
	# Definitions of IBOutlets
	
	# The NSView object from the User Interface. Keep this here!
	dialog = objc.IBOutlet()
	
	# Text field in dialog
	outlineXField = objc.IBOutlet()
	outlineYField = objc.IBOutlet()
	depthXField = objc.IBOutlet()
	depthYField = objc.IBOutlet()
	keepSidebearingsField = objc.IBOutlet()
	
	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'System 7 Shadow',
			'de': u'System-7-Schatten',
		})
		
		# Word on Run Button (default: Apply)
		self.actionButtonLabel = Glyphs.localize({
			'en': u'Shadow',
			'de': u'Schatten',
		})
		
		# Load dialog from .nib (without .extension)
		self.loadNib('IBdialog', __file__)
	
	# On dialog show
	@objc.python_method
	def start(self):
		
		# Set default value
		Glyphs.registerDefault('com.mekkablue.system7shadow.outlineX', 80)
		Glyphs.registerDefault('com.mekkablue.system7shadow.outlineY', 74)
		Glyphs.registerDefault('com.mekkablue.system7shadow.depthX', 160)
		Glyphs.registerDefault('com.mekkablue.system7shadow.depthY', 135)
		Glyphs.registerDefault('com.mekkablue.system7shadow.keepSidebearings', 1)
		
		# Set value of text field
		self.outlineXField.setStringValue_(Glyphs.defaults['com.mekkablue.system7shadow.outlineX'])
		self.outlineYField.setStringValue_(Glyphs.defaults['com.mekkablue.system7shadow.outlineY'])
		self.depthXField.setStringValue_(Glyphs.defaults['com.mekkablue.system7shadow.depthX'])
		self.depthYField.setStringValue_(Glyphs.defaults['com.mekkablue.system7shadow.depthY'])
		self.keepSidebearingsField.setState_(Glyphs.defaults['com.mekkablue.system7shadow.keepSidebearings'])
		
		# Set focus to text field
		self.outlineXField.becomeFirstResponder()
		
	# Actions triggered by UI
	@objc.IBAction
	def setOutlineX_( self, sender ):
		Glyphs.defaults['com.mekkablue.system7shadow.outlineX'] = sender.floatValue()
		self.update()
	
	@objc.IBAction
	def setOutlineY_( self, sender ):
		Glyphs.defaults['com.mekkablue.system7shadow.outlineY'] = sender.floatValue()
		self.update()
	
	@objc.IBAction
	def setDepthX_( self, sender ):
		Glyphs.defaults['com.mekkablue.system7shadow.depthX'] = sender.floatValue()
		self.update()
	
	@objc.IBAction
	def setDepthY_( self, sender ):
		Glyphs.defaults['com.mekkablue.system7shadow.depthY'] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setKeepSidebearings_( self, sender ):
		Glyphs.defaults['com.mekkablue.system7shadow.keepSidebearings'] = sender.state()
		self.update()
	
	# Actual filter
	@objc.python_method
	def filter(self, layer, inEditView, customParameters):
		# fallback values:
		outlineX, outlineY, depthX, depthY = 80, 74, 160, 135
		keepSidebearings = 1
		
		# Called on font export, get value from customParameters
		if customParameters.has_key('outlineX'):
			outlineX = customParameters['outlineX']
		if customParameters.has_key('outlineY'):
			outlineY = customParameters['outlineY']
		if customParameters.has_key('depthX'):
			depthX = customParameters['depthX']
		if customParameters.has_key('depthY'):
			depthY = customParameters['depthY']
		if customParameters.has_key('keepSidebearings'):
			keepSidebearings = customParameters['keepSidebearings']
		
		# Called through UI, use stored value
		else:
			outlineX = float(Glyphs.defaults['com.mekkablue.system7shadow.outlineX'])
			outlineY = float(Glyphs.defaults['com.mekkablue.system7shadow.outlineY'])
			depthX = float(Glyphs.defaults['com.mekkablue.system7shadow.depthX'])
			depthY = float(Glyphs.defaults['com.mekkablue.system7shadow.depthY'])
			keepSidebearings = float(Glyphs.defaults['com.mekkablue.system7shadow.keepSidebearings'])
		
		fatLayer = layer.copyDecomposedLayer()
		fatLayer.removeOverlap()
		fatLayer.cleanUpPaths()
		offsetLayer( fatLayer, outlineX, outlineY )
		
		for h,v in ((depthX,0), (0,depthY)):
			mergeLayer = fatLayer.copy()
			shift = transform(h,-v)
			shiftMatrix = shift.transformStruct()
			mergeLayer.applyTransform(shiftMatrix)
			for path in mergeLayer.paths:
				mergePath = path.copy()
				fatLayer.paths.append(mergePath)
			fatLayer.removeOverlap()
			fatLayer.cleanUpPaths()
		
		originalLSB = layer.LSB
		originalRSB = layer.RSB
		
		layer.removeOverlap()
		
		for fatPath in fatLayer.paths:
			layer.paths.append(fatPath.copy())
		
		if keepSidebearings:
			layer.LSB = originalLSB
			layer.RSB = originalRSB
		
		layer.correctPathDirection()
		
	
	@objc.python_method
	def generateCustomParameter( self ):
		return "%s; outlineX:%s; outlineY:%s; depthX:%s; depthY:%s; keepSidebearings:%s" % (
			self.__class__.__name__,
			Glyphs.defaults['com.mekkablue.system7shadow.outlineX'],
			Glyphs.defaults['com.mekkablue.system7shadow.outlineY'],
			Glyphs.defaults['com.mekkablue.system7shadow.depthX'],
			Glyphs.defaults['com.mekkablue.system7shadow.depthY'],
			Glyphs.defaults['com.mekkablue.system7shadow.keepSidebearings'],
			)
	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
