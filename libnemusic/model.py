PRIMITIVE = 0
DICTIONARY = 1
LIST = 2
class Model:
	__trait__ = DICTIONARY

class Integer(Model): 
	__trait__ = PRIMITIVE

class String(Model): 
	__trait__ = PRIMITIVE

class Boolean(Model):
	__trait__ = PRIMITIVE

class List(Model):
	Element = Model
	__trait__ = LIST

class Dictionary(Model):
	def __init__(self, obj):
		basemembers = dir(Dictionary)
		members     = dir(self)
		for member in members:
			if member not in basemembers:
				model = getattr(self, member)
				if '__trait__' not in dir(model): continue
				if model.__trait__ == PRIMITIVE: setattr(self, member, obj.get(member, None))
				elif model.__trait__ == DICTIONARY: setattr(self, member, model(obj[member]) if member in obj else None)
				else: setattr(self, member, map(lambda x: model.Element(x), obj.get(member, [])))

class NamedObject(Dictionary):
	id   = Integer
	name = String
	def __str__(self): 
		return self.name

class RequireModel:
	""" This class is used to resolve the circular dependency in the data models"""
	def __init__(self, model_name):
		self._model_name = model_name
	def model_name(self):
		return self._model_name
	def __str__(self):
		return "<Undefined model %s>"% self._model_name

def link_model(scope):
	done = set()
	def _do_link(name, var):
		members = dir(var)
		if "__trait__" not in members: return
		if var in done: return
		done.add(var)
		for member in members:
			model = getattr(var, member)
			if isinstance(model, RequireModel):
				if model.model_name() not in scope:
					raise Exception("Unable to resolve model dependency %s" % model)
				setattr(var, member, scope[model.model_name()])
			else: 
				_do_link( name + "." + member, model)	
	for name,var in scope.items(): _do_link(name, var)
