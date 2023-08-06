from . import displays, text, settings
from .mathutils import vec3

def annotations(objs):
	for name,obj in objs.items():
		if isinstance(obj, vec3) and isinstance(name, str):
			yield text.Text(obj, name, 
				size=settings.display['view_font_size'], 
				color=settings.display['annotation_color'], 
				align=(-1,1))
