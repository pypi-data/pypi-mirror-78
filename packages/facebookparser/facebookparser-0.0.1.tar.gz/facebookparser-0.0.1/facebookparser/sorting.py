# https://github.com/salismazaya

import json
from . import parsing

def to_dict_cookies(string_cookies):
    try:
        string_cookies = string_cookies.replace(" ", "")
        dict_cookies = dict(x.split("=") for x in string_cookies.split(";"))
        return dict_cookies
    except:
        return {"datr":""}

def to_mbasic(url):
	if not url:
		return url
	if not "https://mbasic.facebook.com" in url:
		return "https://mbasic.facebook.com" + url
	return url

def post_object(soup):
    name = soup.find("strong").text[:22]
    caption = soup.find("p")
    caption = caption.text if caption else None
    
    data = soup["data-ft"]
    data = json.loads(data)

    def find_a(string):
        rv = soup.find("a", href = lambda x: x and string in x)
        if rv:
            rv = to_mbasic(rv["href"])

        return rv

    like_url = find_a("like.php")
    react_url = find_a("reactions/picker")
    comment_url = find_a("#footer_action_list")
    image_url = parsing.parsing_href(soup, "/photo.php")
    option_url = find_a("direct_actions/?context_str=")

    return {
            "name":name,"caption":caption,
            "like_url":like_url, "react_url":react_url,
            "comment_url":comment_url,
            "image_url":image_url,
            "option_url":option_url,
            "data":data
        }

def people_object(html):
    soup = parsing.to_bs4(html)
    pp = soup.find("img", {"alt": lambda x: x and "profile picture" in x})["src"]

    cover = soup.find("div", {"id":lambda x: x and "profile_cover_photo_container" in x})
    if cover:
        cover = soup.find("img", {"src":lambda x: x and "scontent" in x})["src"]

    confirm_url = parsing.parsing_href(soup, "&confirm", one = True)
    reject_url = parsing.parsing_href(soup, "friends/reject", one = True)
    unfriend_url = parsing.parsing_href(soup, "removefriend.php", one = True)
    add_url = parsing.parsing_href(soup, "profile_add_friend.php", one = True)
    follow_url = parsing.parsing_href(soup, "subscribe.php", one = True)
    unfollow_url = parsing.parsing_href(soup, "subscriptions/remove", one = True)
    message_url = parsing.parsing_href(soup, "messages/thread", one = True)
    unadd_url = parsing.parsing_href(soup, "friendrequest/cancel", one = True)
    isFriend = bool(unfriend_url)

    return [pp, cover, confirm_url, reject_url, unfriend_url,
            add_url, follow_url, unfollow_url, message_url, unadd_url,
            isFriend]

