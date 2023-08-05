from .requests_session import HttpRequest
from bs4.element import Tag
from . import sorting
from . import parsing
from . import objects

class Account:
    def __init__(self, cookies):
        self._name = None
        self._id = None
        self._cookies = None
        self._session = None
        self._session_active = False
        self.info = None
        self._html = ""
        self.login(cookies)
    
    def __repr__(self):
        return "<logged: {}, name: {}, id: {}, info: {}>".format(self.logged(), self._name, self._id, self.info)

    
    def logged(self):
        if not self._html:
            return False

        return not parsing.refsrc(self._html) and not "?refsrc=" in self.session._url

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id
    
    @property
    def cookies(self):
        return self._cookies
    
    @property
    def session(self):
        return self._session
    
    def login(self, cookies):
        self._cookies = cookies
        self._session = HttpRequest()
        self.session.set_cookies(cookies)
        data = self.session.get("https://mbasic.facebook.com/me")
        self._html = data.text
        if not "?refsrc" in data.url and "mbasic_logout_button" in self._html:
            self.__success_login(self._html)
        else:
            self.info = "failed login! when taking cookies make sure not in free mode"
    
    def __success_login(self, html):        
        self.info = "You successfully login"
        self._session_active = True
        self._name = parsing.getMyName(html)
        self._id = parsing.getMyId(html)

        profile_picture = parsing.to_bs4(html).find("img", alt = lambda x: x and "profile picture" in x)
        self.profile_picture = profile_picture.get("src") if type(profile_picture) == Tag else None

