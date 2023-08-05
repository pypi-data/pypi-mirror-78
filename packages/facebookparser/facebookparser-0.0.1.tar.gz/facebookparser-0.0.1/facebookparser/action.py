# https://github.com/salismazaya

from . import decorators
from . import objects
from . import sorting
from . import parsing
import time, re, base64

def open_url(ses, url):
	return ses.session.get(url).text

def dump(func, args = [], kwargs = {}, limit = 100):
	rv = []

	if type(func) == output.Output and func.isNext:
		data = func.next()
	else:
		data = func(*args, **kwargs)

	rv += data.items[:limit]
	if len(rv) >= limit:
		return rv[:limit]
	while data.isNext:
		data = data.next()
		rv += data.items
		if len(rv) >= limit:
			return rv[:limit]
	return rv

class Output:
	def __init__(self, status, html):
		self.status = status
		self._html = html

	@property
	def html(self):
		return self._html

	def bs4(self):
		return parsing.to_bs4(self.html)

	def __repr__(self):
		return "<status: {}>".format(self.status)


class me:
	def create_post(ses, text = None, privacy = None, image = None, feel = None):
		# text: str, value your post
		# privacy: str, see in data.py
		# image: str, path to image file
		# feel: str, see in data.py
		# return: action.Output
		return post._create_post(ses, text, privacy, image, feel, _url = "https://mbasic.facebook.com/me")

class post:
	@decorators.check_login
	def _create_post(ses, text, privacy, image, feel, _url):
		status = True
		html = ses.session.get(_url).text

		try:
			if image:
				url_post = sorting.to_mbasic(parsing.to_bs4(html).find("form", {"action":lambda x: x and "composer" in x})["action"])
				data = ses.session.current_hidden_input()[1]
				data["view_photo"] = "submit"
				html = ses.session.post(url_post, data = data).text

				url_post = sorting.to_mbasic(parsing.to_bs4(html).find("form", {"action":lambda x: x and "composer" in x})["action"])
				data = ses.session.current_hidden_input()[0]
				data["add_photo_done"] = "submit"
				files = {"file1":open(image, "rb")}
				html = ses.session.post(url_post, files = files, data = data).text

			url_post = sorting.to_mbasic(parsing.to_bs4(html).find("form", {"action":lambda x: x and "composer" in x})["action"])
			data = ses.session.current_hidden_input()[0 if image else 1]
			data["privacyx"] = privacy
			data["xc_message"] = text

			if feel:
				data["ogaction"], data["ogobj"] = feel

			data["view_post"] = "submit"

			html = ses.session.post(url_post, data = data).text
			if not "mbasic_logout_button" in html:
				status = False
		except FileNotFoundError as e:
			raise e
		except IOError:
			status = False

		return Output(status, html)
		
	@decorators.check_login
	def like(ses, url, _html = None):
		# ses: Mbasic
		# url: str, post url
		# _html: ignore it

		html = ses.session.get(url).text if not _html else _html
		status = True
		try:
			url = parsing.parsing_href(html, "/like.php", one = True)
			html = ses.session.get(url).text
		except:
			status = False
		return Output(status, html)

	@decorators.check_login
	def comment(ses, url, text = "", image = None,  _html = None):
		# ses: Mbasic
		# url: str, post url
		# text: str, value your comment
		# image: text, path to image file
		# _html: ignore it

		status = True
		try:
			id = re.search(r"id=(\d+)\W?", url).group(1)
			url = "https://mbasic.facebook.com/mbasic/comment/advanced/?target_id={}&pap=1&at=compose&photo_comment=1".format(id)
			html = ses.session.get(url).text if not _html else _html

			url_post = parsing.to_bs4(html).find("form", {"action":lambda x: x and "advanced_composer" in x})["action"]
			data = ses.session.current_hidden_input()[0]
			files = {}

			if image:
				files["photo"] = open(image, "rb")

			data["comment_text"] = text
			data["post"] = "submit"

			html = ses.session.post(url_post, files = files, data = data).text

		except FileNotFoundError as e:
			raise e
		except:
			status = False

		if not text.rstrip() and not image:
			status = False

		return Output(status, html)

	@decorators.check_login
	def react(ses, url, type = "2", in_reactions_picker = True, _html = None):
		# ses: Mbasic
		# url: str, reactions picker url
		# _html: ignore it

		status = True

		if not in_reactions_picker:
			html = ses.session.get(url).text if not _html else _html
			url = parsing.parsing_href(html, "reactions/picker", one = True)

		html = ses.session.get(url).text if not _html else _html
		data = parsing.to_bs4(html)
		try:
			url = sorting.to_mbasic(data.find("a", href = lambda x: "&reaction_type={}&".format(type) in x)["href"])
			html = ses.session.get(url).text
		except:
			status = False

		return Output(status, html)

	@decorators.check_login
	def delete_post(ses, option_url):
		status = True
		html = ses.session.get(option_url).text
		try:
			url_post = parsing.to_bs4(html).find("form", {"method":"post", "action":lambda x: x and "/nfx/basic/handle_action" in x})["action"]
			url_post = "https://mbasic.facebook.com" + url_post
			param = ses.session.current_hidden_input(index = 0)
			param["action_key"] = "DELETE"
			# print(url_post)
			# print(param)
			html_ = ses.session.post(url_post, data = param).text
			# print(html_)
			if "mbasic_logout_button" in html_:
				html = html_
			else:
				status = False
		except:
			status = False
		return Output(status, html)

	@decorators.check_login
	def untag_post(ses, option_url):
		status = True
		html = ses.session.get(option_url).text
		try:
			url_post = parsing.to_bs4(html).find("form", {"method":"post", "action":lambda x: x and "/nfx/basic/handle_action" in x})["action"]
			url_post = "https://mbasic.facebook.com" + url_post
			param = ses.session.current_hidden_input(index = 0)
			param["action_key"] = "UNTAG"
			# print(url_post)
			# print(param)
			html_ = ses.session.post(url_post, data = param).text
			# print(html_)
			if "mbasic_logout_button" in html_:
				html = html_
			else:
				status = False
		except:
			status = False
		return Output(status, html)

class people:
	def create_post(ses, id, text = None, image = None, feel = None):
		return post._create_post(ses, text, None, image, feel, _url = "https://mbasic.facebook.com/{}".format(id))

	@decorators.check_login
	def follow(ses, id, _url = None):
		status = True

		if not _url:
			html = ses.session.get("https://mbasic.facebook.com/{}".format(id)).text
			_url = parsing.parsing_href(html, "subscribe.php", one = True)

		if not _url:
			status = False
		else:
			html = ses.session.get(_url).text

		return Output(status, html)

	@decorators.check_login
	def unfollow(ses, id, _url = None):
		status = True

		if not _url:
			html = ses.session.get("https://mbasic.facebook.com/{}".format(id)).text
			_url = parsing.parsing_href(html, "subscriptions/remove", one = True)
		if not _url:
			status = False
		else:
			html = ses.session.get(_url).text
		return Output(status, html)

	@decorators.check_login
	def addfriend(ses, id, _url = None):
		status = True

		if not _url:
			html = ses.session.get("https://mbasic.facebook.com/{}".format(id)).text
			_url = parsing.parsing_href(html, "profile_add_friend.php", one = True)

		try:
			req = ses.session.get(_url)
			html = req.text
			if not "/friends" in req.url:
				status = False
		except:
			status = False
		return Output(status, html)

	@decorators.check_login
	def unadd(ses, id, _url = None):
		status = True

		if not _url:
			html = ses.session.get("https://mbasic.facebook.com/{}".format(id)).text
			_url = parsing.parsing_href(html, "/friendrequest/cancel/?", one = True)
		try:
			req = ses.session.get(_url)
			html = req.text
			if not "/privacy/touch/block/confirm/" in html:
				status = False
		except:
			status = False
		return Output(status, html)

	@decorators.check_login
	def unfriend(ses, id, _url = None):
		status = True

		if not _url:
			html = ses.session.get("https://mbasic.facebook.com/{}".format(id)).text
			url = parsing.parsing_href(html, "removefriend", one = True)

		if not _url:
			status = False
		else:
			post_data = parsing.getHiddenInput(ses.session.get(_url).text, "removefriend")
			post_data["confirm"] = "Confirm"
			html = ses.session.post("https://mbasic.facebook.com/a/removefriend.php", data = post_data).text
		return Output(status, html)

	@decorators.check_login
	def send_msg(ses, id, msg, _url = None):
		status = True

		if not _url:
			html = ses.session.get("https://mbasic.facebook.com/{}".format(id)).text
			_url = parsing.parsing_href(html, "messages/thread", one = True)
		if not _url:
			status = False
		else:
			post_data = parsing.getHiddenInput(ses.session.get(_url).text, "messages/send")
			post_data["body"] = msg
			post_data["Send"] = "Send"
			html = ses.session.post("https://mbasic.facebook.com/messages/send/?icm=1", data = post_data).text
		return Output(status, html)

	@decorators.check_login
	def deleteMsg(ses, url):
		status = True
		html = ses.session.get(url).text
		try:
			url = parsing.to_bs4(html).find("form", action = lambda x: "/messages/action_redirect" in x)["action"]
			url = sorting.to_mbasic(url)
			param = parsing.getHiddenInput(html, "/messages/action_redirect")
			param["delete"] = "Delete"
			html = ses.session.post(url, data = param).text
			url = parsing.parsing_href(html, "mm_action=delete", one = True)
			html = ses.session.get(url).text
		except:
			status = False
		return Output(status, html)

class group:
	def create_post(ses, id, text = None, image = None, feel = None):
		return post._create_post(ses, text, None, image, feel, _url = "https://mbasic.facebook.com/groups/{}".format(id))

	@decorators.check_login
	def leave_group(ses, id):
		status = True
		html = ses.session.get("https://mbasic.facebook.com/group/leave/?group_id={}".format(id)).text
		try:
			data = ses.session.current_hidden_input(index = 1)
			html_ = ses.session.post("https://mbasic.facebook.com/a/group/leave/?qp=0", data = data).text
			if "?source=ErrorPage" in html_:
				raise Exception
			html = html_
		except:
			status = False
		return Output(status, html)

	@decorators.check_login
	def join_group(ses, id):
		status = True
		html = ses.session.get("https://mbasic.facebook.com/groups/{}".format(id)).text
		try:
			url = ses.session.bs4().find("form", {"action":lambda x: x and "/join/" in x})
			url = sorting.to_mbasic(url["action"])
			data = ses.session.current_hidden_input(index = 1)
			html_ = ses.session.post(url, data = data).text
			if "?source=ErrorPage" in html_:
				raise Exception
			html = html_
		except:
			status = False
		return Output(status, html)

class fanspage:
	@decorators.check_login
	def like(ses, username):
		status = True
		html = ses.session.mbasic(username).text
		try:
			url = parsing.parsing_href(html, "?fan&id=", one = True)
			ses.session.get(url).text
		except:
			status = False
		return Output(status, html)

	@decorators.check_login
	def unlike(ses, username):
		status = True
		html = ses.session.mbasic(username).text
		try:
			url = parsing.parsing_href(html, "?unfan&id=", one = True)
			ses.session.get(url).text
		except:
			status = False
		return Output(status, html)

	@decorators.check_login
	def follow(ses, username):
		status = True
		html = ses.session.mbasic(username).text
		try:
			url = parsing.parsing_href(html, "subscriptions/add?subject_id=", one = True)
			ses.session.get(url).text
		except:
			status = False
		return Output(status, html)

	@decorators.check_login
	def unfollow(ses, username):
		status = True
		html = ses.session.mbasic(username).text
		try:
			url = parsing.parsing_href(html, "/follow_mutator/?page_id=", one = True)
			ses.session.get(url).text
		except:
			status = False
		return Output(status, html)

	@decorators.check_login
	def send_msg(ses, username, msg):
		status = True
		html = ses.session.mbasic(username).text
		try:
			url = parsing.parsing_href(html, "messages/thread", one = True)
			html_ = ses.session.get(url).text
			param = ses.session.current_hidden_input(index = 1)
			param["body"] = msg
			ses.session.post("https://mbasic.facebook.com/messages/send/?icm=1&ref=dbl", data = param)
		except:
			status = False
		return Output(status, html)