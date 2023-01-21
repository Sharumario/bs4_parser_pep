from bs4 import BeautifulSoup
from requests import RequestException

from constants import CONNECTION_ERROR_MESSAGE, TAG_ERROR_MESSAGE
from exceptions import ParserFindTagException


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        raise ConnectionError(CONNECTION_ERROR_MESSAGE.format(url=url))


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=({} if attrs is None else attrs))
    if searched_tag is None:
        raise ParserFindTagException(
            TAG_ERROR_MESSAGE.format(tag=tag, attrs=attrs)
        )
    return searched_tag


def get_soup(session, url, features='lxml'):
    return BeautifulSoup(get_response(session, url).text, features)
