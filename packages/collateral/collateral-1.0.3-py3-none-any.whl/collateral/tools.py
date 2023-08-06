import collections

ArgumentSpecBase = collections.namedtuple("ArgumentSpecBase", ("args", "kwargs"), defaults=((), ()))
class ArgumentSpec(ArgumentSpecBase):
	"""
	A namedtuple with pretreatment of its instantiation arguments.
	The namedtuple has to fields: `args` and `kwargs`. The former
	stores a tuple, the second stores a dictionary whose keys are
	strings.
	"""
	def __new__(cls, args=(), kwargs=(), **kwargs2):
		kwargs = dict(kwargs2, **dict(kwargs))
		self = super().__new__(cls, args=args, kwargs=kwargs)
		return self

class TuplePlus(tuple):
	def all_equal(self):
		return all(c == self[0] for c in self[1:])

