import urllib
import urllib.parse
import urllib.request
from http.cookiejar import CookieJar

from yandex_music_agent.common.form import FormParser
from yandex_music_agent.data import YandexCookie


class AuthException(Exception):
    pass


def resolve_cookie(login: str, password: str) -> YandexCookie:
    cookies_jar = CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookies_jar),
        urllib.request.HTTPRedirectHandler(),
    )
    response = opener.open("https://passport.yandex.ru")
    for form_data in (
            {"login": login},
            {"login": login, "passwd": password},
    ):
        doc = response.read()
        parser = FormParser()
        parser.feed(doc.decode("utf-8"))
        parser.close()
        parser.params.update(form_data)
        response = opener.open(parser.url or response.url, urllib.parse.urlencode(parser.params).encode("utf-8"))
    cookie = YandexCookie({item.name: item.value for item in cookies_jar if item.domain == ".yandex.ru"})
    if not cookie:
        raise AuthException(f"Invalid cookie: {cookie}")
    return cookie
