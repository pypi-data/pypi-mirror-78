import re
import logging
from collections import OrderedDict
from .manga import _MangaTask, title_to_path

logger = logging.getLogger('mangaframework')


class _MangaFrameworkTask(_MangaTask):
    """
    Download manga chapters on several websites based on the same framework.

    Subclasses must define the following class attributes:
      hostname
      handler_name

    """

    hostname = None


    @classmethod
    def match_uri(cls, uri): 
        return re.match(r"^(?:https?:)?//%s/(?P<type>manga|chapter)/(?P<title>[^/]+)(?:/(?P<chapter>[^/]+))?$" % cls.hostname, uri)

    @classmethod
    def from_uri(cls, uri):
        m = cls.match_uri(uri)
        if m is None:
            return None
        if m.group('chapter'):
            chapters = [m.group('chapter')]
        else:
            chapters = None
        return cls(m.group('title'), chapters=chapters)

    @classmethod
    def build_manga_url(cls, manga):
        return f"http://{cls.hostname}/manga/{manga}"

    @classmethod
    def build_chapter_url(cls, manga, chapter):
        return f"http://{cls.hostname}/chapter/{manga}/{chapter}"

    @classmethod
    def get_manga_info(cls, dm, manga):
        soup = dm.request_soup(cls.build_manga_url(title_to_path(manga)))
        if soup.find(text=re.compile("Sorry, the page you have requested cannot be found.")):
            return False

        # get pretty title
        s = soup.find('meta', property='og:title')['content']
        pretty_title = s.split(' Manga Online')[0]
        # get path title
        s = soup.find('meta', property='og:url')['content']
        path_title = cls.match_uri(s).group('title')

        chapters = OrderedDict()
        for c in ('chapter-list', 'panel-story-chapter-list'):
            chapter_list = soup.find('div', class_=c)
            if chapter_list is not None:
                break
        else:
            raise ValueError("failed to retrieve chapter list")

        for e in chapter_list.find_all('a')[::-1]:
            chapter_name = e.text.strip()
            path = cls.match_uri(e['href']).group('chapter')
            chapters[chapter_name] = path

        return {'title': pretty_title, 'path': path_title, 'chapters': chapters}


    def get_chapter_pages_paths(self, chapter):
        soup = self.request_soup(self.build_chapter_url(self.manga, chapter))
        pages = []

        for c in ('vungdoc', 'container-chapter-reader'):
            page_list = soup.find('div', class_=c)
            if page_list is not None:
                break
        else:
            raise ValueError("failed to retrieve page list")

        for e in page_list.find_all('img'):
            pages.append(e['src'])
        return pages

    def get_image_url(self, page):
        return page


class MangakakalotTask(_MangaFrameworkTask):
    handler_name = 'mangakakalot'
    hostname = "mangakakalot.com"
    download_referer = "http://mangakakalot.com/"

class ManganeloTask(_MangaFrameworkTask):
    handler_name = 'manganelo'
    hostname = "manganelo.com"
    download_referer = "http://manganelo.com/"

