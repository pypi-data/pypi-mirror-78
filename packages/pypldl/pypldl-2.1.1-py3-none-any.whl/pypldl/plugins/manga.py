import re
import os
import logging
from ..core import Task

logger = logging.getLogger('manga')


def title_to_path(title):
    """Normalize a manga title to be suitable as a path"""
    s = title.lower()
    s = re.sub('["*:<>?|]', '', s)
    s = re.sub('[ -]', '_', s)
    return s


class _MangaTask(Task):
    """
    Download manga chapters

    Attributes:
      title -- manga title
      manga -- manga identifier (path)
      chapters -- list of chapter paths
      base_url -- base URL, override class value
      progress_chapters -- number of processed chapters
      progress_pages -- number of downloaded pages
      progress_queued_pages -- number of queued pages (not downloaded yet)

    title and chapters will be updated when the task is run.

    Priority format is: (chapter, [page])

    """

    img_extensions = ('jpg', 'png')
    download_referer = None

    def __init__(self, manga, chapters=None, title=None):
        """Create a manga task

        Parameters:
          manga -- manga identifier
          chapters -- chapters to download (see below)
          title -- manga title
          
        Chapters can be provided as:
          None -- download all chapters
          strings -- chapter paths (as seen in URLs) or names (not titles)
          integers -- chapter numbers

        """
        Task.__init__(self)
        self.manga = manga
        self.chapters = chapters
        self.title = title
        self.progress_chapters = None
        self.progress_pages = None
        self.progress_queued_pages = None

    def __str__(self):
        return f"<manga{self.handler_name}: {self.manga!r}>"


    def progress(self):
        if self.progress_pages is None:
            return (0, "initializing")
        with self.lock:
            chapters = self.progress_chapters
            pages = self.progress_pages
            queue = self.progress_queued_pages
            nchapters = len(self.chapters)
        npages = pages + queue

        if chapters == 0:
            # no chapter downloaded yet, cannot estimate
            max_pages = "???"
            progress = 0.
        elif chapters == nchapters:
            # all chapter processed, page count is known
            max_pages = npages
            progress = pages / npages
        else:
            # page count not known yet, make an estimation
            est_pages = npages + (nchapters - chapters) * (npages / chapters)
            max_pages = f"{est_pages:.0f} (est.)"
            progress = pages /est_pages
        status = f"chapters: {chapters}/{nchapters}  pages: {pages}/{max_pages}"
        return (progress, status)


    def run(self):
        # get manga information, update attributes
        info = self.get_manga_info(self.dm, self.manga)
        if info is False:
            raise ValueError(f"manga not found: '{self.manga}'")

        self.manga = info['path']
        if self.title is None:
            self.title = info['title']
        if self.outdir is None:
            if self.title is not None:
                self.outdir = title_to_path(self.title)
            else:
                self.outdir = self.manga

        self.base_url = self.build_manga_url(self.manga).rstrip('/')
        logger.debug('get info for manga %s', self.manga)

        # resolve chapters
        if self.chapters is None:
            chapters = info['chapters'].values()
        else:
            all_paths = set(info['chapters'].values())
            chapters = []
            for ch in self.chapters:
                if ch in all_paths:
                    chapters.append(ch)
                else:
                    if not isinstance(ch, str):
                        ch = str(ch)
                    if ch not in info['chapters']:
                        raise ValueError(f"chapter '{self.manga}' not found for manga '{ch}'")
                    chapters.append(ch)
        self.chapters = chapters

        # initialize values for progress
        self.progress_chapters = 0
        self.progress_pages = 0
        self.progress_queued_pages = 0

        # download chapters
        logger.info("manga '%s': %d chapter(s) to download", self.manga, len(chapters))
        for i, ch in enumerate(chapters):
            prio = (i,)
            self.dm.add_job(prio, self.fetch_chapter, (prio, ch))


    def fetch_chapter(self, prio, chapter):
        """Job routine to fetch a chapter"""

        pages = self.get_chapter_pages_paths(chapter)
        assert pages, f"chapter without pages: {chapter}"
        logger.info("downloading chapter '%s/%s' (%d pages)", self.manga, chapter, len(pages))

        outprefix = self.outpath(chapter.replace('/', ','))
        outpath_fmt = '{0},{1:0%d}.' % max(3, len(str(len(pages))))

        for i, page in enumerate(pages):
            # build output path for the page
            outpath = outpath_fmt.format(outprefix, i+1)
            for ext in self.img_extensions:
                if os.path.exists(outpath+ext):
                    skip = True
                    break
            else:
                skip = False
            if skip:
                logger.info("skip page '%s/%s' (already downloaded)", self.manga, page)
                with self.lock:
                    self.progress_pages += 1
                continue  # page already downloaded, skip
            logger.info("download page '%s/%s'", self.manga, page)
            with self.lock:
                self.progress_queued_pages += 1
            self.dm.add_job(prio + (i,), self.fetch_page, (page, outpath))
        with self.lock:
            self.progress_chapters += 1


    def fetch_page(self, page, outpath):
        """Job routine to fetch a page"""

        img = self.get_image_url(page)
        if img is None:
            logger.warning("no URL for page '%s/%s'", self.manga, page)
            return
        ext = img.split('?')[0].rsplit('.', 1)[-1].lower()
        if ext not in self.img_extensions:
            ext = self.img_extensions[0]
        headers = None
        if self.download_referer:
            headers = {'Referer': self.download_referer}
        try:
            self.download(img, outpath+ext, headers=headers)
        finally:
            with self.lock:
                self.progress_pages += 1
                self.progress_queued_pages -= 1


    @classmethod
    def build_manga_url(cls, manga):
        """Build a manga URL from its manga path"""
        raise NotImplementedError()


    @classmethod
    def get_manga_info(cls, dm, manga):
        """Get manga information, including chapter list

        Parameters:
          dm -- DownloadManager
          manga -- manga path

        Return a map with the following fields:
          title -- manga pretty title (if available)
          path -- manga path
          chapters -- OrderedDict of chapter paths indexed by number (not title)
        If manga is not found, return False.

        """
        raise NotImplementedError()

    def get_chapter_pages_paths(self, chapter):
        """Get pages paths of a chapter
        Return a list of pages paths.
        """
        raise NotImplementedError()

    def get_image_url(self, page):
        """Get an image URL from a page path
        Return None if image URL is not found.
        """
        raise NotImplementedError()

