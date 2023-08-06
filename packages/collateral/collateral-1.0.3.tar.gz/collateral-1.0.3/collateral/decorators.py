import functools

def keep_errors(f):
	@functools.wraps(f)
	def decored(*args, **kwargs):
		try:
			return f(*args, **kwargs)
		except Exception as e:
			return e
	return decored

