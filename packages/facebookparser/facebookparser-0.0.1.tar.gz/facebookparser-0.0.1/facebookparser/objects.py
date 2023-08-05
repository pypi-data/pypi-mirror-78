# https://github.com/salismazaya

from . import parsing
from . import sorting
from . import action
from inspect import signature

class Pewaris:
	def __init__(self, html):
		self._html = html

	@property
	def html(self):
		return self._html

class Output(Pewaris):
	def __init__(self, func, items = None, next = None, html = None):
		super(Output, self).__init__(html)
		self._func = func
		self.items = items
		self._next = next
		self.isNext = bool(self.next_url)
	
	def __repr__(self):
		return "<total_items: {}, next: {}>".format(len(self.items), self.next_url)

	def next(self):
		if not self._next:
			return
		
		args = [None] * (len(signature(self._func._original).parameters) - 2)
		return self._func(*args, next = self._next)

	@property
	def next_url(self):
		rv = self._next
		return rv

class People:
	def __init__(self, ses, name = 0, id = 0, pp = 0, _html = 0, _confirm_url = 0, _reject_url = 0, _unadd_url = 0):
		self.ses = ses
		self.name = name
		self._profile_picture = pp
		self._cover_picture = 0
		self._id = id
		self._html = _html
		self._confirm_url = _confirm_url
		self._reject_url = _reject_url
		self._unfriend_url = 0
		self._add_url = 0
		self._follow_url = 0
		self._unfollow_url = 0
		self._message_url = 0
		self._unadd_url = 0
		self._isFriend = 0

	def __repr__(self):
		return "<{}>".format(self.name[:25])

	def _active(self):
		html = self._html if self._html else self.ses.session.get("https://mbasic.facebook.com/{}?v=timeline".format(self._id)).text
		self._profile_picture, self._cover_picture, self._confirm_url, \
		self._reject_url, self._unfriend_url, self._add_url, \
		self._follow_url, self._unfollow_url, \
		self._message_url, self._unadd_url, self._isFriend = sorting.people_object(html)
		del self._html

	def _check(self, var):
		if var == 0:
			self._active()

	@property
	def id(self):
		return self._id

	@property
	def profile_picture(self):
		self._check(self._profile_picture)
		return self._profile_picture

	@property
	def cover_picture(self):
		self._check(self._cover_picture)
		return self._cover_picture

	@property
	def confirm_url(self):
		self._check(self._confirm_url)
		return self._confirm_url

	@property
	def reject_url(self):
		self._check(self._reject_url)
		return self._reject_url

	@property
	def unfriend_url(self):
		self._check(self._unfriend_url)
		return self._unfriend_url

	@property
	def add_url(self):
		self._check(self._add_url)
		return self._add_url

	@property
	def follow_url(self):
		self._check(self._follow_url)
		return self._follow_url

	@property
	def unfollow_url(self):
		self._check(self._unfollow_url)
		return self._unfollow_url

	@property
	def message_url(self):
		self._check(self._message_url)
		return self._message_url

	@property
	def unadd_url(self):
		self._check(self._unadd_url)
		return self._unadd_url

	@property
	def isFriend(self):
		self._check(self._isFriend)
		return self._isFriend	

	def send_msg(self, msg):
		# msg: str, message
		# return: bool
		return action.people.send_msg(self.ses, self.id, msg, _url = self.message_url).status

	def list_friend(self):
		# return: objects.Output
		return self.ses.list_friend(self.id)

	def get_post(self):
		# return: objects.Output
		return self.ses.get_post_people(self.id)

	def get_album(self):
		# return: objects.Output
		return self.ses.list_album(self.id)

	def unfriend(self):
		# return: bool
		return action.people.unfriend(self.ses, self.id, _url = self.unfriend_url).status

	def follow(self):
		# return: bool
		return action.people.follow(self.ses, self.id, _url = self.follow_url).status

	def unfollow(self):
		# return: bool
		return action.people.unfollow(self.ses, self.id, _url = self.unfollow_url).status

	def create_post(self, *args, **kwargs):
		# return: bool
		return action.people.create_post(self.ses, self.id, *args, **kwargs).status

class Group:
	def __init__(self, ses, name = 0, id = 0):
		self.ses = ses
		self.name = name
		self.id = id

	def __repr__(self):
		return "<{} group>".format(self.name)

	def join_group(self):
		# return: bool
		return action.group.join_group(self.id).status

	def leave_group(self):
		# return: bool
		return action.group.leave_group(self.id).status

	def member_group(self):
		# return: bool
		return self.ses.member_group(self.id)

	def create_post(self, text):
		# return: bool
		return action.group.create_post(self.id, text).status

class Fanspage:
	def __init__(self, ses, name = 0, username = 0):
		self.ses = ses
		self.name = name
		self.username = username

	def __repr__(self):
		return "<{} fanspage>".format(self.name)

	def get_post(self):
		# return: objects.Output
		return self.ses.get_post_fanspage(self.username)

	def like(self):
		# return: bool
		return action.fanspage.like(self.ses, self.username).status

	def unlike(self):
		# return: bool
		return action.fanspage.unlike(self.ses, self.username).status

	def follow(self):
		# return: bool
		return action.fanspage.follow(self.ses, self.username).status

	def unfollow(self):
		# return: bool
		return action.fanspage.unfollow(self.ses, self.username).status

	def send_msg(self, msg):
		# return: bool
		return action.fanspage.send_msg(self.ses, self.username, msg).status

class Post:
	def __init__(self, ses, name = None, caption = None, like_url = None, react_url = None,
				comment_url = None, image_url = [], option_url = None, data = {}):
		self.ses = ses
		self.name = name
		self.caption = caption
		self.like_url = like_url
		self.react_url = react_url
		self.comment_url = comment_url
		self.image_url = image_url
		self.option_url = option_url
		self.data = data

	def __repr__(self):
		return "<{} post's>".format(self.name)

	def get_image(self):
		# return: list
		rv = []
		for image in self.image_url:
			soup = parsing.to_bs4(self.ses.session.get(image).text)
			data = soup.find("div", {"style":"text-align:center;"}).find("img")["src"]
			rv.append(data)
		return rv

	def like(self):
		# return: bool
		if self.like_url:
			action.open_url(self.ses, self.like_url)
			return True
		else:
			return False

	def react(self, type = "2"):
		# return: bool
		if self.react_url:
			return action.post.react(self.ses, self.react_url, type = type).status
		else:
			return False

	def unreact(self):
		# return: bool
		if self.react_url:
			return action.post.react(self.ses, self.react_url, 0).status
		else:
			return False

	def comment(self, text):
		# return: bool
		if self.comment_url:
			return action.post.comment(self.ses, self.comment_url, text).status
		else:
			return False

	def delete_post(self):
		# return: bool
		if self.option_url:
			return action.post.delete_post(self.ses, self.option_url).status
		else:
			return False

	def untag_post(self):
		# return: bool
		if self.option_url:
			return action.post.untag_post(self.ses, self.option_url).status
		else:
			return False

class Album:
	def __init__(self, ses, name = 0, id_people = 0, id_album = 0):
		self.ses = ses
		self.name = name
		self.id_people = id_people
		self.id_album = id_album

	def __repr__(self):
		return "<{} album>".format(self.name)

	def get_people(self):
		# return: objects.People
		return self.ses.people(self.id_people)

	def get_image(self):
		# return: objects.Output
		return self.ses.list_photo_inAlbum("https://mbasic.facebook.com/{}/albums/{}/".format(self.id_people, self.id_album))
	
