PRIMITIVE = 0
DICTIONARY = 1
LIST = 2
class Model:
	__trait__ = DICTIONARY

class Integer(Model): 
	__trait__ = PRIMITIVE

class String(Model): 
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
	def __str__(self): return self.name

