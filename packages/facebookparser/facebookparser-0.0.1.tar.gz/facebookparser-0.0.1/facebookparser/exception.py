# coded by: salism3
# 23 - 05 - 2020 23:18 (Malam Takbir)

class CookiesInvalid(Exception):
	def __init__(self):
		super().__init__("cookies invalid :(")

class ArgumentError(Exception):
	pass