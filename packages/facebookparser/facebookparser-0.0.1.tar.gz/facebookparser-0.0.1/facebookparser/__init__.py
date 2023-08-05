# https://github.com/salismazaya

from . import sorting
from . import parsing
from .menu.post import Post
from .menu.friend import Friend
from .menu.group import Group
from .menu.other import Other
from . import objects
from . import account
import re

class Mbasic(account.Account, Friend, Post, Group, Other):
    def __init__(self, cookies):
        account.Account.__init__(self, cookies)
        
    def people(self, id):
        try:
            soup = parsing.to_bs4(self.session.get("https://mbasic.facebook.com/{}".format(id)).text)
            name = soup.find("title").text
            id = re.search(r"id=(\d+)", parsing.parsing_href(soup, "block/confirm", one = True)).group(1)
            return objects.People(self, name = name, id = id)
        except:
            return

    def group(self, id):
        try:
            soup = parsing.to_bs4(self.session.get("https://mbasic.facebook.com/groups/{}?view=info".format(id)).text)
            name = soup.find("title").text
            id = re.search(r"groups/(\d+)", str(soup)).group(1)
            return objects.Group(self, name = name, id = id)
        except:
            return

    def fanspage(self, username):
        try:
            soup = parsing.to_bs4(self.session.get("https://mbasic.facebook.com/{}".format(username)).text)
            name = soup.find("title").text
            username = soup.find("span", string = lambda x: x and "@" in x).text.replace("@", "")
            return objects.Fanspage(self, name = name, username = username)
        except:
            return
