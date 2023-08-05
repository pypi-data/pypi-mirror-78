# https://github.com/salismazaya

from .. import decorators
from .. import objects
from .. import sorting
from .. import parsing

class Post:
	def _get_post_core(self, func, url, next, string_next):
		html = self.session.get(url if not next else next).text
		parse = parsing.to_bs4(html)

		data = parse.find_all("div", {"data-ft":lambda x: x and "mf_story_key" in x})
		data = [objects.Post(self, **sorting.post_object(html)) for html in data]

		next = parsing.parsing_href(html, string_next, one = True)

		return objects.Output(func, items = data, next = next, html = html)

	@decorators.check_login
	def get_post_home(self, next = None):
		return self._get_post_core(self.get_post_home, "https://mbasic.facebook.com/home.php", next, "?aftercursorr=")

	@decorators.check_login
	def get_post_people(self, id, next = None):		
		return self._get_post_core(self.get_post_people, "https://mbasic.facebook.com/{}?v=timeline".format(id), next, "?cursor")

	@decorators.check_login
	def get_post_fanspage(self, username, next = None):	
		return self._get_post_core(self.get_post_fanspage, "https://mbasic.facebook.com/{}".format(username), next, "?sectionLoadingID=")

	@decorators.check_login
	def get_post_group(self, id, next = None):
		return self._get_post_core(self.get_post_group, "https://mbasic.facebook.com/groups/{}".format(id), next, "?bacr=")