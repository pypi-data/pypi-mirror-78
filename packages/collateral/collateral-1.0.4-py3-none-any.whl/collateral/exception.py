
class CollateralError(Exception):
	pass

def collateralErrorFactory(*args, on_exception=Exception):
	"""
	A function that builds an instance of a subclass of the above
	`CollateralError`. The subclass extends both `CollateralError`
	and a given exception `on_exception`.

	+	on_exception:
		either an `Exception` subclass (default is `Exception`) or
		an `Exception` subclass instance. In the latter case, the
		`args` attribute of the instance is prepended to the `args`
		attribute of the built exception instance. The type of the
		built exception extends both `CollateralError` and either
		`on_exception` (if it is a type), or `type(on_exception)`
		if it is an `Exception` instance.
	"""
	if isinstance(on_exception, Exception):
		args = (*on_exception.args, *args)
		on_exception = type(on_exception)
	cls = type(f"Collateral{on_exception.__name__}", (CollateralError, on_exception), {})
	self = cls(*args)
	return self

