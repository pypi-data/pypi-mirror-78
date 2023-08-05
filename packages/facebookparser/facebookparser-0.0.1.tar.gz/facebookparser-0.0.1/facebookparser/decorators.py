# coded by: salism3
# 23 - 05 - 2020 23:18 (Malam Takbir)

from .exception import CookiesInvalid
from .exception import ArgumentError
from .parsing import refsrc

def check_login(func):
	def inner(*args, **kwargs):
		data = func(*args, **kwargs)
		if refsrc(data.html):
			raise CookiesInvalid
		return data
	inner._original = func
	return inner

# def check(required = []):
# 	def decorator(func):
# 		def wrapper(*args, **kwargs):
# 			for x in required:
# 				if not kwargs.get("next") and not locals()["kwargs"].get(x):
# 					raise ArgumentError("check argument in function '{}'".format(func.__name__))
# 			else:
# 				data = func(*args, **kwargs)
# 				if refsrc(data.html):
# 					raise CookiesInvalid(data.session_number)
# 				return data
# 		return wrapper
# 	return decorator