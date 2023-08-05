import functools, abc, collections, copy

__all__ = [ "AbstractCollateral", "ArgumentSpec" ]

ArgumentSpecBase = collections.namedtuple("ArgumentSpecBase", ("args", "kwargs"), defaults=((), ()))
class ArgumentSpec(ArgumentSpecBase):
	"""
	A namedtuple with pretreatment of its instantiation arguments.
	The namedtuple has to fields: `args` and `kwargs`. The former
	stores a tuple, the second stores a dictionary whose keys are
	strings.
	"""
	def __new__(self, args=(), kwargs=(), **kwargs2):
		kwargs = dict(kwargs2, **kwargs)
		super().__new__(args=args, kwargs=kwargs)

class CollateralTuple(tuple):
	def all_equal(self):
		return all(c == self[0] for c in self[1:])

class AbstractCollateral(abc.ABC):
	#list of attribute name to protect, in addition to __class__.__dict__.keys()
	_notcollaterables = frozenset((
		'__bool__',
		'__class__',
		'__dict__',
		'__doc__',
		'__format__',
		'__getattribute__',
		'__int__',
		'__len__',
		'__qualname__',
		'__str__'
	))
	_collaterize_prefix = "_collateral_"

	@property
	@abc.abstractmethod
	def collaterals(self):
		"""
		The tuple of collateral objects, to manipulate in parallel.
		"""
		pass

	@staticmethod
	def _collaterize(methname):
		"""
		Internal helper for defining collateral method on collateral
		instance from method name. The static method is not a
		function decorator, since its argument is not a function,
		but a method name.

		+	methname: a method name (`str`).
		"""
		def overloaded(self, *args, **kwargs):
			resSuccess = []
			resAll = []
			exception = None
			for c in self.collaterals:
				try:
					res = (getattr(c, methname)(*args, **kwargs))
					resSuccess.append(res)
				except Exception as e:
					res = e
					exception = exception or e
				finally:
					resAll.append(res)
			res =  __class__.collateral_build(*resSuccess)
			if exception:
				resFail = __class__.collateral_build(*resAll)
				e = copy.deepcopy(exception)
				e.args = exception.args + (res, resFail)
				raise e
			return res
		overloaded.__name__ = methname
		overloaded.__doc__ = f"Overload of {methname} in Collateral."
		return overloaded
	@staticmethod
	def collateral_build(*collaterals):
		"""
		The constructor for the class. Its name is not the usual
		`__new__` or `__init__` for two reasons:
		1.	the object built is not an instance of the class
			`AbstractCollateral` (which is abstract whence not
			instanciable) but of a subclass `Collateral` that
			implements the abstract property `collaterals` by
			returning the fixed tuple `collaterals` of collateral
			objects.
		2.	the method `__new__` and `__init__` may be overloaded
			in the resulting object class. In that case, `__new__`
			should apply the `__new__` static method of each
			collateral objects in parallel, and returns the result
			gathered in a new `Collateral` subclass. Notice that
			a call to the static method `__new__` would result in an
			object of different type. On the other hand, `__init__`
			we be applied on each collateral objects. In other words,
			`__new__` and `__init__` method names are protected for
			being possibly used as collateral methods.

		+	collaterals: a tuple of objects to manipulate in parallel.
			If all given objects are `None`, then the constructor
			directly returns `None`, namely, does not build any
			collateral objects. This captures the case of an empty
			tuple.
		"""
		if all(c is None for c in collaterals):
			return
		lls = CollateralTuple(collaterals)

		@property
		def collaterals(self):
			return lls
		mdict = dict(collaterals=collaterals)

		classes = map(type, lls)
		clsdirs = map(set, map(dir, classes))
		ndir = functools.reduce(set.union, clsdirs)
		for methname in ndir:
			name = methname
			while name in __class__._notcollaterables or name in __class__.__dict__:
				name = f"{__class__._collaterize_prefix}{methname}"
			if all(map(callable, map(lambda c: getattr(c, methname, None), lls))):
				mdict[name] = __class__._collaterize(methname)
			else:
				mdict[name] = property(__class__._collaterize(methname))

		cls = type("Collateral", (__class__,), mdict)
		self = object.__new__(cls)
		return self

	def collateral_map(self, f):
		resSuccess, resAll = [], []
		exception = None
		for c in self.collaterals:
			try:
				res = f(c)
				resSuccess.append(res)
			except Exception as e:
				res = e
				exception = exception or e
			finally:
				resAll.append(res)
		res = self.collateral_build(*resSuccess)
		if exception:
			e = copy.deepcopy(exception)
			resFail = self.collateral_build(*resAll)
			e.args = exception.args + (res, resFail)
			raise e
		return res
	def collateral_filter(self, f):
		resSuccess, resAll = [], []
		exception = None
		for c in self.collaterals:
			try:
				res = f(c)
				if res:
					resSuccess.append(c)
			except Exception as e:
				res = e
				exception = exception or e
			finally:
				resAll.append(res)
		res = self.collateral_build(*res)
		if exception:
			e = copy.deepcopy(exception)
			resFail = self.collateral_build(*resAll)
			e.args = exception.args + (res, resFail)
			raise e
		return res
	def collateral_call(self, *arguments, default_args=(), default_kwargs=(), common_pre_args=(), common_post_args=(), **common_kwargs):
		"""
		+	arguments: a tuple that defines a partial mapping from
			indices of collaterals in `self` to `ArgumentSpec`s. The
			partial mapping is defined as a dict as follows: If
			`dict(arguments)` successes, then it is the mapping
			dictionary. Otherwise, the mapping dictionary is defined
			by `dict(enumerate(arguments))` which should success.
		+	default_args:	a tuple of arguments to be used for
			collateral indices that do not have associated argument
			specification image in the above-defined mapping.
		+	default_kwargs: a dictionary specification, whose keys
			are expected to be all strings (`str`), to be used as
			default list of keyworded arguments for collateral indices
			that do not have associated argument specification image
			in the above-mapping.
		+	common_args: a tuple of arguments to be appended to the
			argument tuple of each argument specification defined by
			`arguments`.
		+	common_kwargs: a list of keyworded parameter to be added
			to the list of keyworded arguments of each specification
			defined by `arguments`, with least priority (namely, a
			keyworded parameter given in an argument specification
			will be preferred to a same-keyword parameted given in
			`common_kwargs`).

		When the mapping dictionary is defined, it is used as
		follows. We associate the collateral of index `i` (i.e.,
		`self.collaterals[i]`) with the value associated with the
		integer key `i` in the mapping dictionary, if any. This
		value is expected to be an argument specification
		(`ArgumentSpec`). If it does not exist, the default argument
		specification `ArgumentSpec(`default_args, default_kwargs)`
		is taken instead.
		"""
		try:
			arguments = dict(arguments)
		except TypeError:
			arguments = dict(enumerate(arguments))
		EmptyArgumentSpec = ArgumentSpec(default_args, default_kwargs)
		res = map(lambda i, c: (arguments.get(i, EmptyArgumentSpec), c), enumerate(self.collaterals))
		res = map(lambda a, c: (a if hasattr(a, 'args') and hasattr(a, 'kwargs') else ArgumentSpec(*a), c), res)
		resSuccess, resAll = [], []
		exception = None
		for a, c in res:
			try:
				r = c(*common_pre_args, *a.args, *common_post_args, **dict(common_kwargs, **a.kwargs))
				resSuccess.append(r)
			except Exception as e:
				r = e
				exception = exception or e
			finally:
				resAll.append(r)
		res = self.collateral_build(*resSuccess)
		if exception:
			e = coppy.deepcopy(exception)
			resFail = self.collateral_build(*resAll)
			e.args = exception.args + (res, resFail)
			raise e
		return res

	#MAGICS
	def __getattr__(self, attr):
		resSuccess, resAll = [], []
		exception = None
		for c in self.collaterals:
			try:
				res = getattr(c, attr)
				resSuccess.append(res)
			except Exception as e:
				res = e
				exception = exception or e
			finally:
				resAll.append(res)
		res = self.collateral_build(*resSuccess)
		if exception:
			e = copy.deepcopy(exception)
			resFail = self.collateral_build(*resAll)
			e.args = exception.args + (res, resFail)
			raise e
		return res
	def __hash__(self):
		return hash((self.__class__.__name__, self.collaterals))
	def __repr__(self):
		return f"{self.__class__.__name__}< {' // '.join(map(repr, self.collaterals))} >"
	def __dir__(self):
		return sorted(set(__class__.__dict__.keys()).union(self.__class__.__dict__.keys()).union(sum(map(dir, self.collaterals), [])))
	def _ipython_key_completions_(self):
		"""
		Autocompletion of keys on getting item.
		"""
		nokeys = lambda: ()
		allkeys = lambda c: getattr(c, 'keys', nokeys)()
		keys = map(allkeys, self.collaterals)
		keys = functools.reduce(set.union, keys, set())
		return keys

