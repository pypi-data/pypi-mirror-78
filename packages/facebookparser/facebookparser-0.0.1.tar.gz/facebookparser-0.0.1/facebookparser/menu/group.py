# https://github.com/salismazaya

from .. import decorators
from .. import objects
from .. import sorting
from .. import parsing

class Group:
	@decorators.check_login
	def member_group(self, id, next = None):
		# id: str, id group
		url = "https://mbasic.facebook.com/browse/group/members/?id={}".format(id)
		html = self.session.get(url if not next else next).text
		data = parsing.to_bs4(html).find_all("table", {"id":lambda x: x and "member_" in x})

		def sorted(arg):
			name = arg.find("a", href = True).text
			id_ = arg["id"].replace("member_", "")
			img = arg.find("img").get("src")
			return objects.People(self, name = name, id = id_, pp = img)

		next_ = parsing.parsing_href(html, "&cursor=", one = True)
		data = list(map(sorted, data))
		return objects.Output(self.member_group, items = data, next = next_, html = html)

	@decorators.check_login
	def myGroup(self):
		html = self.session.get("https://mbasic.facebook.com/groups/?seemore&refid=27").text
		data = parsing.parsing_href_regex(html, r"/groups/\d+\W", bs4_class = True)
		data = [objects.Group(name = x.text, id = re.search(r"/(\d+)\W", x["href"]).group(1)) for x in data]
		return objects.Output(self.myGroup, items = data, html = html)
