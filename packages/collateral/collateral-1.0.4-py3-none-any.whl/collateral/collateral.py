import functools, itertools
from collateral.exception import collateralErrorFactory
from collateral.tools import ArgumentSpec, TuplePlus
from collateral.decorators import keep_errors

__all__ = ['BaseCollateral', 'pointwise_method', 'Collateral']


chain = itertools.chain
reduce = functools.reduce

class BaseCollateral:
	"""
	The base abstract class for `Collateral` all objects. The
	constructor `__new__` builds a subclass implementing it, and
	instantiate this subclass.

	>>> C = Collateral( (9, 0, 9), [0, 9, 0] )
	>>> repr(C)
	'Collateral< (9, 0, 9) // [0, 9, 0] >'
	>>> C.collaterals.all_equal()
	False
	>>> C.count(0)
	Collateral< 1 // 2 >
	>>> C._collateral___len__()
	Collateral< 3 // 3 >
	>>> C.collateral_map(len)
	Collateral< 3 // 3 >
	>>> C._collateral___len__() == C.collateral_map(len)
	True
	>>> C[0]
	Collateral< 9 // 0 >
	>>> C[:1]
	Collateral< (9,) // [0] >
	>>> C.collateral_map(set).collaterals.all_equal()
	True
	>>> D = C.collateral_map(list)
	>>> repr(D)
	'Collateral< [9, 0, 9] // [0, 9, 0] >'
	>>> D.append(8)
	>>> repr(D)
	'Collateral< [9, 0, 9, 8] // [0, 9, 0, 8] >'
	>>> D.collateral_map(sorted).collaterals.all_equal()
	False
	>>> E = D.collateral_map(lambda c: getattr(c, 'append'))
	>>> E.collateral_call((0, 9))
	>>> D.collateral_map(sorted).collaterals.all_equal()
	True
	>>> repr(D)
	'Collateral< [9, 0, 9, 8, 0] // [0, 9, 0, 8, 9] >'
	>>> D.pop()
	Collateral< 0 // 9 >
	>>> repr(D)
	'Collateral< [9, 0, 9, 8] // [0, 9, 0, 8] >'
	"""
	#list of attribute name to protect, in addition to __class__.__dict__.keys()
	_notcollaterables = frozenset((
		'__bool__',
		'__class__',
		'__format__',
		'__getattribute__',
		'__int__',
		'__len__',
		'__qualname__',
		'__slots__',
		'__str__'
	))
	_notprocedures = frozenset((
		'pop',
		'__getitem__',
		'get',
		'__getattribute__',
		'__getattr__'
	))
	_collaterize_prefix = "_collateral_"
	_collateral_tuple = TuplePlus

	@property
	def collaterals(self):
		"""
		The tuple of collateral objects, to manipulate in parallel.
		>>> C = Collateral(True, False)
		>>> C.collaterals.all_equal()
		False
		>>> D = C.__and__(False)
		>>> D.collaterals.all_equal()
		True
		"""
		return TuplePlus()

	def collateral_map(self, f, notallnone=False):
		"""
		>>> C = Collateral(range(2, 3), range(7, 9))
		>>> C.collateral_map(len)
		Collateral< 1 // 2 >
		>>> C.collateral_map(bool)
		Collateral< True // True >
		>>> D = C.collateral_map(tuple)
		>>> D
		Collateral< (2,) // (7, 8) >
		>>> H = D.collateral_map(hash)
		>>> isinstance(H, BaseCollateral)
		True
		>>> all(isinstance(c, int) for c in H.collaterals)
		True
		>>> D.collateral_map(hash) == D._collateral___hash__()
		True
		"""
		try:
			#return Collateral(*map(f, self.collaterals), notallnone=notallnone)
			#cannot use builtin map, because of catched StopIteration exception
			r = []
			for c in self.collaterals:
				r.append(f(c))
			return Collateral(*r, notallnone=notallnone)
		except Exception as e:
			f = keep_errors(f)
			raise collateralErrorFactory(Collateral(*map(f, self.collaterals), notallnone=notallnone), on_exception=e)
	def collateral_filter(self, f, notallnone=False):
		"""
		>>> C = Collateral(range(2, 3), range(7, 9))
		>>> C.collateral_filter(bool) == C
		True
		>>> C.collateral_filter(lambda r: len(tuple(r[:-1])))
		Collateral< range(7, 9) >
		>>> C.collateral_filter(lambda r: False)
		"""
		try:
			#return Collateral(*filter(f, self.collaterals), notallnone=notallnone)
			#cannot use builtin filter, because of catched StopIteration exception
			r = []
			for c in self.collaterals:
				if f(c):
					r.append(c)
			return Collateral(*r, notallnone=notallnone)
		except Exception as e:
			f = keep_errors(f)
			raise collateralErrorFactory(Collateral(*map(f, self.collaterals), notallnone=notallnone), on_exception=e)
	def collateral_enumerate(self, start=0, notallnone=False):
		"""
		Enumerate the collaterals and gather them in a `Collateral`
		object. This is different from `collateral_map(enumerate)`.
		Indeed, the latter applies `enumerate` on each collateral.
		With `collateral_enumerate`, the user has a direct access to
		the object index among collaterals of `self`. In the
		resulting `Collateral` object, each of the collaterals is a
		pair `(i, c)`, where `c` is one of the collaterals of `self`
		and `i` is its index in `self.collaterals`. In other words,
		`self.collaterals[i] == c`. Moreover, the order is preserved
		whence `i` is also the index of `(i,c)` is the tuple of
		collaterals of the resulting `Collateral` object.

		+	start: the starting index (as for enumerate builtin).
			Default is `0`.

		>>> C = Collateral([0, 2], True)
		>>> D = C.collateral_enumerate()
		>>> D
		Collateral< (0, [0, 2]) // (1, True) >
		>>> D.collateral_enumerate()
		Collateral< (0, (0, [0, 2])) // (1, (1, True)) >
		>>> E = Collateral([0, 2], (3, 8, 5))
		>>> E.collateral_enumerate()
		Collateral< (0, [0, 2]) // (1, (3, 8, 5)) >
		>>> F = E.collateral_map(enumerate)
		>>> F
		Collateral< <enumerate at 0x...> // <enumerate at 0x...> >
		>>> F.collateral_map(list)
		Collateral< [(0, 0), (1, 2)] // [(0, 3), (1, 8), (2, 5)]
		>>> E.collateral_enumerate(start=2)
		Collateral< (2, [0, 2]) // (3, (3, 8, 5)) >
		"""
		return Collateral(*enumerate(self.collaterals, start=start), notallnone=notallnone)
	def collateral_call(
			self, argspecs, method=None,
			default_args=(), default_kwargs=(),
			common_pre_args=(), common_post_args=(), common_kwargs=(),
			notallnone=False,
			**other_common_kwargs):
		"""
		+	argspecs: an iterable that defines a partial mapping from
			indices of collaterals in `self` to `ArgumentSpec`s. The
			partial mapping is defined as a dict as follows: If
			`dict(argspecs)` successes, then it is the mapping
			dictionary. Otherwise, the mapping dictionary is defined
			by `dict(enumerate(argspecs))` which should success.
		+	method: the name of a method to call (`str`) or `None`.
			If `None`, the collaterals themselves are called (whence
			`method=None` should hopefully produce the same result as
			`method=__call__`).
		+	default_args:	a tuple of arguments to be used for
			collateral indices that do not have associated argument
			specification image in the above-defined mapping.
		+	default_kwargs: a dictionary specification, whose keys
			are expected to be all strings (`str`), to be used as
			default list of keyworded arguments for collateral indices
			that do not have associated argument specification image
			in the above-mapping.
		+	common_pre_args: a tuple of arguments to be prepended to
			the argument tuple of each argument specification defined
			by `argspecs`.
		+	common_post_args: a tuple of arguments to be appended to
			the argument tuple of each argument specification defined
			by `argspecs`.
		+	common_kwargs: a list of keyworded parameter to be added
			to the list of keyworded arguments of each specification
			defined by `argspecs`, with least priority (namely, a
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

		>>> l, r = [3, 2], [2, 3]
		>>> C = Collateral(l.append, r.append)
		>>> C.collateral_call((8, 7))
		>>> l, r
		([3, 2, 8], [2, 3, 7])
		>>> C = Collateral(l, r)
		>>> C.collateral_call((9, 0), method='append')
		>>> C
		Collateral< [3, 2, 8, 9] // [2, 3, 7, 0] >
		>>> l, r
		([3, 2, 8, 9], [2, 3, 7, 0])
		"""
		try:
			argspecs = dict(argspecs)
		except TypeError:
			argspecs = dict(enumerate(argspecs))
		EmptyArgumentSpec = ArgumentSpec(default_args, default_kwargs)
		def pointwise_call(ic):
			#ic=(i,c) from collaterals of self.collateral_enumerate()
			i, c = ic
			a = argspecs.get(i, EmptyArgumentSpec)
			if not hasattr(a, 'args') or not hasattr(a, 'kwargs'):
				a = ArgumentSpec((a,))
			if method:
				f = getattr(c, method)
			else:
				f = c
			return f(*common_pre_args, *a.args, *common_post_args, **dict(dict(common_kwargs, **other_common_kwargs), **a.kwargs))
		return self.collateral_enumerate(notallnone=notallnone).collateral_map(pointwise_call, notallnone=notallnone)

	#MAGICS
	def __getattr__(self, attr):
		"""
		>>> class A:
		...		pass
		>>> l, r = A(), A()
		>>> C = Collateral(l, r)
		>>> l.foo = "bar"
		>>> r.foo = "rab"
		>>> C.foo
		Collateral< 'bar' // 'rab' >
		>>> "foo" in dir(C)
		True
		>>> class B:
		...		def __dir__(self):
		...			return []
		>>> l, r = B(), B()
		>>> C = Collateral(l, r)
		>>> l.foo = "babar"
		>>> r.foo = "rabab"
		>>> C.foo
		Collateral< 'babar' // 'rabab' >
		>>> "foo" in dir(C)
		False
		"""
		f = lambda c: getattr(c, attr)
		return self.collateral_map(f, notallnone=False)
	def __eq__(self, other):
		"""
		>>> l, r = [2, 3], [2, 3]
		>>> C = Collateral((3, 4, 5), l)
		>>> D = Collateral((3, 4, 5), l)
		>>> C == D
		True
		>>> E = Collateral((3, 4, 5), r)
		>>> C == E
		True
		>>> r.append(2)
		>>> C == E
		False
		"""
		if not isinstance(other, __class__):
			return False
		return self.collaterals == other.collaterals
	def __hash__(self):
		"""
		>>> C = Collateral((2, 3), "foobar", True, False, None, "9")
		>>> hash(C) == C.__hash__()
		True
		>>> isinstance(hash(C), int)
		True
		>>> D = Collateral([])
		>>> hash(D)
		Traceback (most recent call last):
			...
		TypeError: unhashable type: 'list'
		"""
		return hash((self.__class__.__name__, self.collaterals))
	def __repr__(self):
		"""
		>>> C = Collateral((3, 4), [3, 4])
		>>> repr(C) == C.__repr__()
		True
		>>> isinstance(repr(C), str)
		True
		>>> repr(C)
		'Collateral< (3, 4) // [3, 4] >'
		>>> D = Collateral(object(), dict(), set(), tuple(), list(), None)
		>>> len(repr(D).replace(' // ', '|').split('|')) == len(D.collaterals)
		True
		"""
		return f"{self.__class__.__name__}< {' // '.join(map(repr, self.collaterals))} >"
	def __dir__(self):
		"""
		>>> class A:
		...		class_attribute = frozenset((3, 4))
		...		def _hidden_attribute(self):
		...			return False
		...		def a_method_name_that_we_never_saw42(self):
		...			return True
		...		@property
		...		def a_property(self):
		...			return None
		...		@classmethod
		...		def a_class_method(cls):
		...			return cls.__name__
		...		@staticmethod
		...		def a_static_method():
		...			return "Good job!"
		...		def __repr__(self):
		...			return repr(self.foo) if hasattr(self, 'foo') else 'no foo found'
		>>> l, r = A(), A()
		>>> C = Collateral(l, r)
		>>> dir(C) == C.__dir__()
		True
		>>> for k in ['a_class_attribute', '_hidden_attribute', 'a_method', 'a_property', 'a_class_method', 'a_static_method', '__repr__' ]:
		...		assert k in dir(C)
		>>> for k in dir(C):
		...		assert isinstance(k, str)
		...		getattr(C, k)
		>>> C
		Collateral< no foo found // no foo found >
		>>> C.foo = "bar"
		>>> "foo" in dir(C)
		True
		>>> C
		Collateral< 'bar' // 'bar' >
		"""
		res = set(__class__.__dict__.keys())
		res = res.union(self.__class__.__dict__.keys())
		if self.collaterals:
			res = res.union(reduce(set.intersection, map(set, map(dir, self.collaterals))))
		res = sorted(res)
		return res

class BaseKeyableCollateral(BaseCollateral):
	def transversal_keys(self):
		"""
		Returns the set of keys shared by all collaterals. Unlike
		the `keys` method, this method returns a `set` rather than
		a `Collateral` iterable on keys. This could be useful in
		order to iterate over shared keys, with same order on each
		of the collaterals.
		>>> C = Collateral({ 0: True, 1: False, 'other': "bar", 'shared': "foo" }, { 1: False, 0: True, 'shared': "foo" })
		>>> for k in C:
		...		print(k)
		...		print(C[k])
		...		print("---")
		Collateral< 0 // 1 >
		Collateral< True // False >
		---
		Collateral< 1 // 0 >
		Collateral< False // True >
		---
		Collateral< 'other' // 'shared' >
		Collateral< "bar" // "foo" >
		---
		>>> for k in C.transversal_keys():
		...		print(k)
		...		print(C[k])
		...		print("---")
		Collateral< 0 // 0 >
		Collateral< True // True >
		---
		Collateral< 1 // 1 >
		Collateral< False // False >
		---
		Collateral< 'shared' // 'shared' >
		Collateral< "foo" // "foo" >
		---
		"""
		if not self.collaterals or not hasattr(self, '__getitem__') or not hasattr(self, 'keys'):
			return ()
		keys = self.keys().collateral_map(set).collaterals
		keys = reduce(set.intersection, keys)
		return keys
	def transversal_keys_all(self):
		if not self.collaterals or not hasattr(self, '__getitem__') or not hasattr(self, 'keys'):
			return ()
		keys = reduce(set.union, self.keys().collaterals, set())
		return keys
	_ipython_key_completions_ = transversal_keys
	_ipython_key_completions_.__doc__ = "Autocompletion of keys"

def pointwise_method(methname, callable=True):
	"""
	Defines a method that applies pointwise on each of the
	collaterals. It is not a function decorator, as the `methname`
	argument is expected to be a string rather than a function.
	Nevertheless, it could be thought as an attribute decorator,
	applied on the `methname`-named attribute of each collaterals
	of the `self`, the first argument of the returned method.

	+	methname: a method name (`str`).
	+	callable: a Boolean indicating whether `methname` correspond
		to a callable attribute of all collaterals. If `False`, then
		the resulting method is returned as a property.
	"""
	notallnone = methname not in BaseCollateral._notprocedures
	if callable:
		def overloaded(self, *args, **kwargs):
			if any(isinstance(c, BaseCollateral) for c in chain(args, kwargs.values())):
				g = lambda i: (lambda arg: arg.collaterals[i] if isinstance(arg, BaseCollateral) else arg)
				h = lambda i: (lambda kwarg: (kwarg[0], kwarg[1].collaterals[i] if isinstance(kwarg[1], BaseCollateral) else kwarg))
				f = lambda ic: getattr(ic[1], methname)(*map(g(ic[0]), args), **dict(map(h(ic[0]), kwargs.items())))
				return self.collateral_enumerate().collateral_map(f, notallnone=notallnone)
			else:
				f = lambda c: getattr(c, methname)(*args, **kwargs)
				return self.collateral_map(f, notallnone=notallnone)
	else:
		def overloaded(self):
			f = lambda c: getattr(c, methname)
			return self.collateral_map(f, notallnone=notallnone)
	overloaded.__name__ = methname
	overloaded.__doc__ = f"Pointwise overload of {methname} in Collateral."
	if not callable:
		overloaded = property(overloaded)
	return overloaded

def Collateral(*collaterals, notallnone=False):
	"""
	A constructor of `Collateral` objects. The function builds a
	subclass implementing `BaseCollateral` and returns an
	instantiation of the subclass. This has one exception: when
	all given collaterals are `None` and the `notallnone` argument
	is `True`, then the function returns the value `None`. This
	includes the case of an empty tuple of collaterals.

	+	collaterals: a tuple of objects to manipulate in parallel.
	+	notallnone: a Boolean indicating whether to return `None`
		when all given collaterals are `None` (if `True`) or not
		(if `False`). Default is `False`. This keyword is mostly
		used when calling a method on a `Collateral` object, in
		order to avoid procedure (method with no return) to pollute
		the output.

	>>> Collateral(True, False)
	Collateral< True // False >
	>>> Collateral(None, None, None, notallnone=True)
	>>> Collateral(notallnone=True)
	>>> Collateral(None, None, None, True, None, None, notallnone=True)
	Collateral< None // None // None // True // None // None >
	"""
	if notallnone and all(c is None for c in collaterals):
		return
	lls = BaseCollateral._collateral_tuple(collaterals)

	@property
	def collaterals(self):
		return lls
	mdict = dict(collaterals=collaterals)

	classes = map(type, lls)
	clsdirs = map(set, map(dir, classes))
	ndir = reduce(set.intersection, clsdirs) if lls else set()
	bases = (BaseCollateral,)
	protected_names = BaseCollateral._notcollaterables.union(BaseCollateral.__dict__)
	if '__getitem__' in ndir and 'keys' in ndir:
		bases = (BaseKeyableCollateral,)
		protected_names = protected_names.union(BaseKeyableCollateral.__dict__)
	for methname in ndir:
		name = methname
		while name in protected_names:
			name = f"{BaseCollateral._collaterize_prefix}{methname}"
		iscallable = all(map(callable, map(lambda c: getattr(c, methname, None), lls)))
		mdict[name] = pointwise_method(methname, callable=iscallable)
	cls = type("Collateral", bases, mdict)
	self = object.__new__(cls)
	return self

