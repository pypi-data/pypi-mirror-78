# https://github.com/salismazaya

from .. import decorators
from .. import objects
from .. import sorting
from .. import parsing
import re

class Other:
    @decorators.check_login
    def msgUrl(self, next = None):
        html = self.session.get("https://mbasic.facebook.com/messages" if not next else next).text
        data = parsing.parsing_href(html, "/read/")
        next = parsing.parsing_href_regex(html, r"[?]pageNum.*selectable", one = True)
        return objects.Output(self.msgUrl, items = data, next = next, html = html)

    @decorators.check_login
    def list_album(self, id):
        # id: str, id album
        if id.isdigit():
            url = f"https://mbasic.facebook.com/profile.php?v=photos&id={id}"
        else:
            url = f"https://mbasic.facebook.com/{id}/photos"

        html = self.session.get(url).text
        data = parsing.parsing_href(html, "/albums/", bs4_class = True)

        data = [objects.Album(self, name = x.text, id_people = id, id_album = str(x).split("/")[3]) for x in data]
        return objects.Output(self.list_album, items = data, html = html)

    @decorators.check_login
    def list_photo_inAlbum(self, url, next = None, html = None):
        # url: str, url album
        if not html:
            html = self.session.get(url if not next else next).text

        data = parsing.parsing_href_regex(html, r"photo.php|/photos/")

        def get_photo(url):
            html_ = self.session.get(url).text
            data = parsing.to_bs4(html_).find("div",  {"style":"text-align:center;"}).find("img").get("src")
            return data

        data = list(map(lambda url: get_photo(url), data))
        next = parsing.parsing_href(html, "?start_index=", one = True)
        return objects.Output(self.list_photo_inAlbum, items = data, html = html, next = next)

    @decorators.check_login
    def get_photo_from_inbox(self, url, next = None, html = None):
        # url: str, url chat
        if not html:
            html = self.session.get(url if not next else next).text

        data = parsing.to_bs4(html).find_all("img", {"src":lambda x: "oh=" in x and "oe=" in x, "alt":False})
        data = [x.get("src") for x in data]
        next = parsing.parsing_href_regex(html, r"(last_message_timestamp)(pagination_direction=)", one = True)
        return objects.Output(self.get_photo_from_inbox, items = data, html = html, next = next)

    # @decorators.check_login
    # def option_post_people(self, id, next = None, html = None):
    #     # id: str, id people
    #     html = self.session.get(("https://mbasic.facebook.com/" + id) if not next else next).text
    #     data = parsing.parsing_href(html, "direct_actions/?context_str=")
    #     next = parsing.parsing_href(html, "?cursor", one = True)
    #     return objects.Output(self.option_post_people, items = data, html = html, next = next)

