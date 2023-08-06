# This file is part of pymadcad,  distributed under license LGPL v3

'''	Display module of pymadcad
	
	This module provides a render pipeline system centered around class 'Scene' and a Qt widget 'View' for window integration and user interaction. 'Scene' is only to manage the objects to render (almost every madcad object). Most of the time you won't need to deal with it directly. The widget is what actually displays it on the screen.
	The objects displayed can be of any type but must implement the display protocol
	
	display protocol
	----------------
		a displayable is an object that implements the signatue of Display:
		
			class display:
				box (Box)       delimiting the display, can be an empty or invalid box
				pose (mat4)     local transformation
				
				stack(scene)                   rendering routines (can be methods, or any callable)
				duplicate(src,dst)             copy the display object for an other scene if possible
				upgrade(scene,displayable)     upgrade the current display to represent the given displayable
				control(...)                   handle events
				
				__getitem__       access to subdisplays if there is
		
		For more details, see class Display below
	
	NOTE
	----
		There is some restrictions using the widget. This is due to some Qt limitations (and design choices), that Qt is using separated opengl contexts for each independent widgets or window.
		
		- a View should not be reparented once displayed
		- a View can't share a scene with Views from an other window
		- to share a Scene between Views, you must activate 
				QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
'''

# minimum opengl required version
opengl_version = (3,3)




class Display:
	''' Blanket implementation for displays.
		This class is exactly the display protocol specification
	'''
	box = Box(width=-inf)
	pose = fmat4(1)
	selected = False
	
	def stack(self, scene) -> '[(place, key, callable)]':
		''' rendering functions to insert in the renderpipeline '''
		return ()
	def duplicate(self, src, dst) -> 'display/None':
		''' duplicate the display for an other scene (other context) but keeping the same memory buffers when possible '''
		return None
	def __getitem__(self, key) -> 'display':
		''' get a subdisplay by its index/key in this display (like in a scene) '''
		raise IndexError('{} has no sub displays'.format(type(self).__name__))
	def upgrade(self, scene, displayable) -> 'bool':
		''' update the current displays internal datas with the given displayable '''
		return False
	
	def control(self, scene, key, sub, evt: 'QEvent'):
		''' handle input events occuring on the area of this display (or of one of its subdisplay).
			for subdisplay events, the parents control functions are called first, and the sub display controls are called only if the event is not accepted by parents
			
			:key:    the key path for the current display
			:sub:    the key path for the subdisplay
		'''
		pass
	
	def display(self, scene):
		''' displays are obviously displayable as themselves '''
		return self


class Turntable:
	def __init__(self, center: vec3, camera: vec3):
		self.center = fvec3(center)
		self.camera = fvec3(camera)
	def rotate(self, dx, dy):
		self.camera = (
						  fmat3(1.,       0.,        0.,
								0.,  cos(dy),   sin(dy),
								0., -sin(dy),   cos(dy))
						* fmat3( cos(dx),   sin(dx),  0.,
								-sin(dx),   cos(dx),  0.,
								 0.,        0.,       1.)
					) * self.camera
	def pan(self, dx, dy):
		rot = fmat3(dirbase(self.camera))
		self.center += fvec3(rot[0]) * dx + fvec3(rot[1]) * dy
	def zoom(self, f):
		self.camera *= f
	@property
	def distance(self):
		return length(self.camera)
	
	def tomatrix(self) -> mat4:
		rot = fmat3(dirbase(self.camera))
		mat = translate(fmat4(rot), -self.center)
		mat[3][3] -= length(self.camera)
		return mat
	#@staticmethod
	#def frommatrix(view):
		#self.center = fvec3(view[3]) * inverse(fmat3(view))
		#self.camera = -view[3][3] * fvec3(view[2])
class Orbit:
	def __init__(self, center: vec3, distance, orient: vec3):
		self.center = fvec3(center)
		self.distance = distance
		self.orient = fquat(orient)
	def rotate(self, dx, dy):
		self.orient = quat(vec3(-dy, 0, dx)) * self.orient
	def pan(self, dx, dy):
		mat = mat3_cast(self.orient)
		self.center += fvec3(rot[0]) * dx + fvec3(rot[1]) * dy
	def zoom(self, f):
		self.distance *= f
	def tomatrix(self) -> mat4:
		mat = translate(mat4_cast(self.orient), -self.center)
		mat[3][3] -= self.distance
	#@staticmethod
	#def frommatrix(view):
		#self.orient = quat_cast(fmat3(view))
		#self.center = 

class Perspective:
	def __init__(self, fov):
		self.fov = fov
	def tomatrix(self, ratio, distance) -> mat4:
		indev
class Orthographic:
	def __init__(self, size):
		self.size = size
	def tomatrix(self, ratio, distance) -> mat4:
		indev


class Scene:
	''' rendeing pipeline for madcad displayable objects 
		
		This class is gui-agnostic, it only relys on opengl, and the context has to be created by te user.
	'''
	STEP_IDENT = 0
	STEP_DISPLAY = 10

	def __init__(self, ctx, objs=(), options=None):
		# context variables
		self.ctx = ctx
		self.ressources = {}	# context-related ressources, shared across displays, but not across contexts (shaders, vertexarrays, ...)
		
		# rendering options
		self.options = deepcopy(settings.scene)
		if options:	self.options.update(options)
		
		# render pipeline
		self.displays = {} # displays created from the inserted objects, associated to their insertion key
		self.queue = []	# list of objects to display, not yet loaded on the GPU
		self.stack = []	# list of callables, that constitute the render pipeline:  (place, key, callable)
		self.steps = [] # list of last rendered ids for each stack step
		
	
	# methods to manage the rendering pipeline
	
	def add(displayable, key=None) -> 'key':
		''' add a displayable object to the scene, if key is not specified, an unused integer key is used 
			the object is not added to the the renderpipeline yet, but queued for next rendering.
		'''
		if key is None:
			for i in range(len(self.displays)):
				if i not in self.displays:	key = i
		self.queue.append((key, displayable))
		return key

	def __setitem__(self, key, value):
		''' equivalent with self.add with a key '''
		self.queue.append((key, value))
	def __getitem__(self, key) -> 'display':
		''' get the displayable for the given key, raise when there is no object or when the object is still in queue. '''
		return self.displays[key]
		
	
	def dequeue(self):
		''' load all queued objects to the render pipeline (and in the GPU) '''
		if self.queue:
			with self.ctx as ctx:
				for key, obj in self.queue:
					if key in self.displays:
						self.stack = [rdr for rdr in self.stack if rdr[1][:len(key)] == key]
					self.displays[key] = disp = displayable.display(self)
					for rdr in disp.stack(self):
						place = bisect(self.stack, rdr[0], key=lambda rdr: rdr[0])
						self.stack.insert(place, rdr)
			self.steps = [0] * len(self.stack)

	def render(self, view):
		self.dequeue()
		ident = 1
		i = 0
		
		# identify objects
		self.ctx.enable_only(mgl.DEPTH_TEST)
		self.ctx.blend_func = mgl.ONE, mgl.ZERO
		self.ctx.blend_equation = mgl.FUNC_ADD
		
		while i < len(self.stack) and self.stack[i][0] < STEP_DISPLAY:
			ident += self.stack[i][2](view, ident) or 0
			self.steps[i] = ident
			i += 1
		
		# render objects
		self.ctx.multisample = True
		self.ctx.enable_only(mgl.BLEND | mgl.DEPTH_TEST)
		self.ctx.blend_func = mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA
		self.ctx.blend_equation = mgl.FUNC_ADD
		view.fb_screen.use()
		view.fb_screen.clear()
		
		while i < len(self.stack):
			ident += self.stack[i][2](self, ident) or 0
			self.steps[i] = ident
			i += 1
		
		self.fresh.clear()
	
	def ressource(self, name, func=None):
		''' get a ressource loaded or load it using the function func.
			If func is not provided, an error is raised
		'''
		if name in self.ressources:	
			return self.ressources[name]
		elif callable(func):
			with self.ctx as ctx:  # set the scene context as current opengl context
				res = func(self)
				self.ressources[name] = res
				return res
		else:
			raise KeyError(f"ressource {repr(name)} doesn't exist or is not loaded")
	
	def preload(self):
		''' internal method to load common ressources '''
		self.ressources['shader_ident'] = self.ctx.program(
					vertex_shader=open(ressourcedir+'/shaders/object-ident.vert').read(),
					fragment_shader=open(ressourcedir+'/shaders/ident.frag').read(),
					)

		self.ressources['shader_subident'] = self.ctx.program(
					vertex_shader=open(ressourcedir+'/shaders/object-item-ident.vert').read(),
					fragment_shader=open(ressourcedir+'/shaders/ident.frag').read(),
					)
					

# dictionnary to store procedures to override default object displays
dispoverrides = {}

def list_override(l,scene):
	for obj in l:
		if type(obj) in dispoverrides:	yield from dispoverrides[type(obj)](obj,scene)
		elif hasattr(obj, 'display'):	yield from obj.display(scene)
dispoverrides[list] = list_override

	

class View(QOpenGLWidget):
	''' Qt widget to render and interact with displayable objects 
		it holds a scene as renderpipeline
	'''
	def __init__(self, objs=(), projection=None, navigation=None, parent=None):
		# super init
		super().__init__(parent)
		fmt = QSurfaceFormat()
		fmt.setVersion(*opengl_version)
		fmt.setProfile(QSurfaceFormat.CoreProfile)
		fmt.setSamples(4)
		self.setFormat(fmt)
		self.setFocusPolicy(Qt.StrongFocus)
        				
		# interaction methods
		self.projection = projection or Perspective()
		self.navigation = navigation or Turntable()
		self.tool = [self.navigation_tool().send] # tool stack, the last tool is used for input events, until it is removed 
		self.scene = Scene(None, objs)
		
		# render parameters
		self.uniforms = {'proj':fmat4(1), 'view':fmat4(1), 'projview':fmat4(1)}	# last frame rendering constants
		# render targets
		self.fb_screen = None	# UI framebuffer
		self.fb_idents = None	# framebuffer for id rendering
		# dump targets
		self.map_depth = None
		self.map_idents = None
		
		# internal variables
		self.fresh = set()	# set of refreshed internal variables since the last render
	
	# -- internal frame system --
	
	def init(self, size):
		w,h = size
		assert self.scene.ctx, 'context is not initialized'

		# self.fb_frame is already created and sized by Qt
		self.fb_screen = self.ctx.detect_framebuffer(self.defaultFramebufferObject())
		self.fb_ident = self.ctx.simple_framebuffer(size, components=3, dtype='f1')
		self.ident_map = np.empty((h,w), dtype='u2')
		self.depth_map = np.empty((h,w), dtype='f4')
		
	def refreshmaps(self):
		''' load the rendered frames from the GPU to the CPU 
			
			- When a picture is used to GPU rendering it's called 'frame'
			- When it is dumped to the RAM we call it 'map' in this library
		'''
		if 'fb_idents' not in self.fresh:
			with self.scene.ctx as ctx:
				ctx.finish()
				self.makeCurrent()	# set the scene context as current opengl context
				self.fb_idents.read_into(self.map_idents, viewport=self.fb_idents.viewport, components=2)
				self.fb_idents.read_into(self.map_depth, viewport=self.fb_idents.viewport, components=1, attachment=-1, dtype='f4')
			self.fresh.add('fb_idents')
	
	def render(self):
		s = self.size()
		w, h = s.width(), s.height()
		self.scene.uniforms['view'] = view = self.navigation.tomatrix()
		self.scene.uniforms['proj'] = proj = self.projection.tomatrix(w/h, self.navigation.distance)
		self.scene.uniforms['projview'] = proj * view
		self.scene.render()
		
	# -- methods to deal with the view --
	
	def itemnear(self, point: QPoint, radius=10) -> QPoint:
		''' return the closest coordinate to coords, (within the given radius) for which there is an object at
			So if objnear is returing something, objat and ptat will return something at the returned point
		'''
		self.refreshmaps()
		for x,y in snailaround((point.x(), point.y()), (self.map_ident.shape[1], self.map_ident.shape[0]), radius):
			ident = int(self.map_ident[-y, x])
			if ident > 0:
				return QPoint(x,y)
	
	def ptat(self, point: QPoint) -> vec3:
		''' return the point of the rendered surfaces that match the given window coordinates '''
		self.refreshmaps()
		viewport = self.fb_ident.viewport
		depthred = float(self.map_depth[-coords[1],coords[0]])
		x =  (point.x()/viewport[2] *2 -1)
		y = -(point.y()/viewport[3] *2 -1)
		
		if depthred == 1.0:
			return None
		else:
			view = self.uniforms['view']
			proj = self.uniforms['proj']
			a,b = proj[2][2], proj[3][2]
			depth = b/(depthred + a) * 0.53	# get the true depth  (can't get why there is a strange factor ... opengl trick)
			#near, far = self.projection.limits  or settings.display['view_limits']
			#depth = 2 * near / (far + near - depthred * (far - near))
			#print('depth', depth, depthred)
			return vec3(fvec3(affineInverse(view) * fvec4(
						depth * x /proj[0][0],
						depth * y /proj[1][1],
						-depth,
						1)))
	
	def ptfrom(self, point: QPoint, center: vec3) -> vec3:
		''' 3D point below the cursor in the plane orthogonal to the sight, with center as origin '''
		view = self.uniforms['view']
		proj = self.uniforms['proj']
		viewport = self.scene.fb_ident.viewport
		x =  (point.x()/viewport[2] *2 -1)
		y = -(point.y()/viewport[3] *2 -1)
		depth = (view * fvec4(fvec3(center),1))[2]
		return vec3(fvec3(affineInverse(view) * fvec4(
					-depth * x /proj[0][0],
					-depth * y /proj[1][1],
					depth,
					1)))
	
	def itemat(self, point: QPoint) -> 'key':
		''' return the key path of the object at the given screen position (widget relative). 
			If no object is at this exact location, None is returned  
		'''
		self.refreshmaps()
		ident = int(self.fb_ident[-point.y(), point.x()])
		if ident > 0:
			rdri = bisect(self.scene.steps, ident)
			if rdri == len(self.scene.steps):
				print('internal error: object ident points out of idents list')
			while rdri > 0 and self.scene.steps[rdri-1] == ident:	rdri -= 1
			if rdri > 0:	subi = ident - self.scene.steps[rdri-1] - 1
			else:			subi = ident - 1
			return (*self.scene.stack[rdri][1], subi)
	
	def look(self, box: 'Box/key'):
		''' Make the scene manipulator look at the box.
			This is adjusting both the manipulator center and the zoom level.
		'''
		# TODO rendre compatible avec une projection quelconque (ou au moins orthographique)
		if isinstance(box, (vec3,fvec3)):	box = Box(center=box, width=vec3(0))
		if box.isvalid():
			if box.isempty():
				self.manipulator.center = fvec3(box.center)
			else:
				fov = self.projection.fov or settings.display['field_of_view']
				self.manipulator.center = fvec3(box.center)
				self.manipulator.distance = length(box.width) / (2*tan(fov/2))
			self.manipulator.update()
	
	def adjust(self, box: 'Box/key'):
		indev
	def center(self, center: vec3):
		indev
	
	# -- event system --
	
	def event(self, evt):
		''' Qt event handler
			In addition to the usual subhandlers, inputEvent is called first to handle every InputEvent.
			
			The usual subhandlers are used to implement the navigation through the scene (that is considered to be intrinsic to the scene widget).
		'''
		if isinstance(evt, QInputEvent):
			evt.ignore()
			self.inputEvent(evt)
			if evt.isAccepted():	return True
		return super().event(evt)
	
	def inputEvent(self, evt):
		''' Default handler for every input event (mouse move, press, release, keyboard, ...) 
			When the event is not accepted, the usual matching Qt handlers are used (mousePressEvent, KeyPressEvent, etc).
			
			This function can be overwritten to change the view widget behavior.
		'''
		if self.tool:	
			for tool in reversed(self.tool):
				tool(self, evt)
				if evt.isAccepted():	return
		
		elif isinstance(evt, QMouseEvent) and evt.type() in (QEvent.MouseButtonPress, QEvent.MouseButtonRelease, QEvent.MouseButtonDblClick):
			pos = self.itemnear(evt.pos())
			if pos:
				key = self.itemat(pos)
				self.control(key, evt)
				if evt.isAccepted():	return
				
	def control(self, key, evt):
		''' transmit a control event successively to all the displays matching the key path stages.
			At each level, if the event is not accepted, it transmits to sub items
			
			This function can be overwritten to change the interaction with the scene objects.
		'''
		disp = self.scene.displays[key[0]]
		for i in range(1,len(key)):
			disp.control(self, key[:i], key[i:], evt)
			if evt.isAccepted(): return
			disp = disp[key[i]]
	
	def navigation_tool(self):
		''' internal navigation tool '''
		ctrl = alt = slow = False
		nav = None
		while True:
			evt = yield
			if isinstance(evt, QKeyboardEvent):
				k = evt.key()
				press = evt.type() == QEvent.KeyPressed
				if	 k == Qt.Key_Control:	ctrl = press
				elif k == Qt.Key_Alt:		alt = press
				elif k == Qt.Key_Shift:		slow = press
				if ctrl and alt:		nav = self.navigation.zoom
				elif ctrl:				nav = self.navigation.pan
				elif alt:				nav = self.navigation.orbit
				else:					nav = None
				evt.accept()
			elif evt.type() == QEvent.MouseButtonPress:
				last = evt.pos()
			elif evt.type() == QEvent.MouseMoveEvent:
				if evt.button() == Qt.MiddleButton:
					move = self.navigation.orbit
				elif nav:
					move = nav
				if move:
					gap = evt.pos() - last
					size = self.size()
					move(gap.x()/size.width(), gap.y()/size.height())
					self.update()
					evt.accept()
	
	# -- Qt things --
	
	def initializeGL(self):	pass

	def paintGL(self):
		self.scene.ctx = mgl.create_context()
		self.init()
		self.scene.preload()
		self.render()
		self.paintGL = self.render
		
	def resizeEvent(self, evt):
		super().resizeEvent(evt)
		self.init()
		self.update()


def snail(radius):
	''' generator of coordinates snailing around 0,0 '''
	x = 0
	y = 0
	for r in range(radius):
		for x in range(-r,r):		yield (x,-r)
		for y in range(-r,r):		yield (r, y)
		for x in reversed(range(-r,r)):	yield (x, r)
		for y in reversed(range(-r,r)):	yield (-r,y)

def snailaround(pt, box, radius):
	''' generator of coordinates snailing around pt, coordinates that goes out of the box are skipped '''
	cx,cy = pt
	mx,my = box
	for rx,ry in snail(radius):
		x,y = cx+rx, cy+ry
		if 0 <= x and x < mx and 0 <= y and y < my:
			yield x,y

def show(objs, options=None):
	''' shortcut to create a QApplication showing only one view with the given objects inside.
		the functions returns when the window has been closed and all GUI destroyed
	'''
	import sys
	from PyQt5.QtCore import Qt, QCoreApplication
	from PyQt5.QtWidgets import QApplication
	
	QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
	app = QApplication(sys.argv)
	scn = View(Scene(objs, options))
	scn.show()
	err = app.exec()
	if err != 0:	print('error: Qt exited with code', err)


'''
		-- generators helpers --
'''

class Generated(object):
	__slots__ = 'generator', 'value'
	def __init__(self, generator):	self.generator = generator
	def __iter__(self):				self.value = yield from self.generator

class Dispatcher(object):
	''' iterable object that holds a generator built by passing self as first argument
		it allows the generator code to dispatch references to self.
		NOTE:  at contrary to current generators, the code before the first yield is called at initialization
	'''
	__slots__ = 'generator', 'value'
	def __init__(self, func=None, *args, **kwargs):
		self.generator = self._run(func, *args, **kwargs)
		next(self.generator)
	def _run(self, func, *args, **kwargs):
		self.value = yield from func(self, *args, **kwargs)
		
	def send(self, value):	return self.generator.send(value)
	def __iter__(self):		return self.generator
	def __next__(self):		return next(self.generator)

class Tool(Dispatcher):
	def _run(self, func, view, *args, **kwargs):
		try:	
			self.value = yield from func(self, *args, **kwargs)
		except StopTool:	
			pass
		view.tool.remove(self)
	
	def __call__(self, evt):
		return self.send(evt)
		
	def stop(self):
		if self.generator:
			self.generator.throw(StopTool())
			self.generator = None
	def __del__(self):
		self.stop()
	
class StopTool(Exception):
	''' used to stop a tool execution '''
	pass


# temporary examples
if False:

	def tutu(self, main):
		evt = yield
		gnagna
		scene.tool = self.send
		budu.iterator = self

	Tool(tutu, main)
	
	
	class MeshDisplay:
		def control(self, scene, key, sub, evt):
			if evt.type() == QEvent.MOUSE_RELEASE_EVENT:
				self.flags[sub] ^= self.FLAG_SELECT	# invert selection state
				self.vb_flags.write(self.flags)
				self.selected = np.any(self.flags)
				evt.accept()

ç
