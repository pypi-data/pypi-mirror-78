# https://github.com/salismazaya

from .. import decorators
from .. import objects
from .. import sorting
from .. import parsing
import re

class Friend:
	@decorators.check_login
	def friend_request(self, next = None):
		html = self.session.get("https://mbasic.facebook.com/friends/center/requests/" if not next else next).text
		confirm = parsing.parsing_href(html, "?confirm=")

		reject = parsing.parsing_href(html, "?delete=")
		data = list(zip(confirm, reject))
		next = parsing.parsing_href(html, "?ppk=", one = True)

		return objects.Output(self.friend_request, items = data, next = next, html = html)

	@decorators.check_login
	def friend_requested(self, next = None):
		html = self.session.get("https://mbasic.facebook.com/friends/center/requests/outgoing/" if not next else next).text
		data = parsing.parsing_href(html, "/cancel/?")
		next = parsing.parsing_href(html, "?ppk=", one = True)
		return objects.Output(self.friend_requested, items = data, next = next, html = html)

	@decorators.check_login
	def list_friend(self, id, next = None):
		if str(id).isdigit():
			url = "https://mbasic.facebook.com/profile.php?id={}&v=friends".format(id)
		else:
			url = "https://mbasic.facebook.com/{}/friends".format(id)
		html = self.session.get(url if not next else next).text

		data = parsing.parsing_href(html, "fref=fr_tab", bs4_class = True)
		data = [x.parent.parent for x in data]

		def sorted(x):
			name = x.find("a").text
			id = re.search(r"\w[\w.]+", x.find("a")["href"].replace("/", "").replace("profile.php?id=", "")).group()
			img = x.find("img")["src"]
			return objects.People(self, name = name, id = id, pp = img)

		data = list(map(sorted, data))
		next = parsing.parsing_href_regex(html, r"\/friend.*?lst=", one = True)

		return objects.Output(self.list_friend, items = data, next = next, html = html)
		
	def myFriend(self, next = None):
		return self.list_friend(id = self.id, next = next)

	@decorators.check_login
	def onlineFriend(self, next = None):
		out = []
		html = self.session.get("https://mbasic.facebook.com/buddylist.php").text
		data = parsing.to_bs4(html).find_all("img", {"src":lambda x: "https://static.xx.fbcdn.net/rsrc.php/v3/ym/r/bzGumJjigJ0.png" in x})
		data = [x.parent.parent for x in data]
		if data:
			del data[0]
		
		def sorted(arg):
			a_class = arg.find("a")
			name = a_class.text
			id = a_class["href"].split("fbid=")[1].split("&")[0]
			return name, id

		data = list(map(sorted, data))
		return objects.Output(self.onlineFriend, items = data, html = html)
