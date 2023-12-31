import os
import urllib
import requests
import magic
from tqdm.auto import tqdm
from urllib.parse import quote
import random
from requests.exceptions import ReadTimeout
import functools
import time


################
# ---> CONSTANTS
################

BASE_URL = 'https://www.google.com/search?q='
GOOGLE_PICTURE_ID = '''&biw=1536&bih=674&tbm=isch&sxsrf=ACYBGNSXXpS6YmAKUiLKKBs6xWb4uUY5gA:1581168823770&source=lnms&sa=X&ved=0ahUKEwioj8jwiMLnAhW9AhAIHbXTBMMQ_AUI3QUoAQ'''
HEADERS = {
    'User-Agent':
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
}
SCANNER_COUNTER = None


def generate_search_url(keywords):
    keywords_to_search = [str(item).strip() for item in keywords.split(',')]
    keywords_count = len(keywords_to_search)
    return keywords_to_search, keywords_count


def generate_urls(search):
    """Generates a URLS in the correct format that brings to Google Image seearch page"""
    return [(BASE_URL+quote(word)+GOOGLE_PICTURE_ID) for word in search]


def check_webpage(url):
    checked_url = None
    try:
        request = requests.get(url, allow_redirects=True, timeout=10)
        if 'html' not in str(request.content):
            checked_url = request
    except ReadTimeout as err:
        print(err)
        pass
    return checked_url


def scan_webpage(webpage, extensions, timer):
    """Scans for pictures to download based on the keywords"""
    global SCANNER_COUNTER
    scanner = webpage.find
    found = False
    counter = 0
    while counter < timer:
        new_line = scanner('"https://', SCANNER_COUNTER + 1)  # How Many New lines
        SCANNER_COUNTER = scanner('"', new_line + 1)  # Ends of line
        buffor = scanner('\\', new_line + 1, SCANNER_COUNTER)
        if buffor != -1:
            object_raw = webpage[new_line + 1:buffor]
        else:
            object_raw = webpage[new_line + 1:SCANNER_COUNTER]
        if any(extension in object_raw for extension in extensions):
            found = True
            break
        counter += 1
    if found:
        object_ready = check_webpage(object_raw)
        return object_ready


class Downloader:
    """
        Main Downloader
        ::param extension:iterable of Files extensions
    """
    def __init__(self, extensions=None, dir_name=None):
        if extensions:
            self._extensions = set(*[extensions])
        else:
            self._extensions = {'.jpg', '.png', '.jpeg'}
        self._directory = dir_name if dir_name else "simple_images/"
        self.get_dirs = set()
        self._cached_urls = {}
        self.img_hashes = set()

    @property
    def directory(self):
        return self._directory

    @directory.setter
    def directory(self, value):
        self._directory = value

    @property
    def cached_urls(self):
        return self._cached_urls

    @property
    def extensions(self):
        return self._extensions

    @extensions.setter
    def extensions(self, value):
        self._extensions = set([value])


    def get_urls(self):
        return [self._cached_urls[url][1].url for url in self._cached_urls]

    def _download_page(self, url):
        req = urllib.request.Request(url, headers=HEADERS)
        resp = urllib.request.urlopen(req)
        resp_data = str(resp.read())
        return resp_data

    def search_urls(self, keywords, limit=1, verbose=False, cache=True, timer=None):
        cache_out = {}
        search, count = generate_search_url(keywords)
        urls_ = generate_urls(search)
        timer = timer if timer else 1000
        max_progressbar = count * (list(range(limit+1))[-1]+1)
    
        i = 0
        while i < count:
            global SCANNER_COUNTER
            SCANNER_COUNTER = -1
            url = urls_[i]
            path = self.generate_dir(search[i])
            raw_html = self._download_page(url) # Download the entire page from the google Picture search

            imgs_found = 0
            total_searched = 0
            pbar = tqdm(range(limit), desc=f"Term = {search[i]}, Images searched={total_searched}")
            while imgs_found < limit:
                webpage_url = scan_webpage(raw_html, self._extensions, timer)
                pbar.set_description(f"Term = {search[i]}, Images searched={total_searched}")
                total_searched += 1
                if webpage_url and (webpage_url.content.hex() not in self.img_hashes):
                    file_name = Downloader.gen_fn(webpage_url, search[i])
                    cache_out[file_name] = [path, webpage_url]
                    self.img_hashes.add(webpage_url.content.hex())
                    pbar.update(1)
                    imgs_found += 1
                else:
                    pass
                
            i += 1
        if verbose:
            for url in cache_out:
                print(url)
        if cache:
            self._cached_urls = cache_out
        if not cache_out:
            print('==='*15 + ' < ' + 'NO PICTURES FOUND' + ' > ' + '==='*15)
        return cache_out

    def download(self, keywords=None, limit=1, verbose=False, cache=True, download_cache=False, timer=None):
        if not download_cache:
            content = self.search_urls(keywords, limit, verbose, cache, timer)
        else:
            content = self._cached_urls
            if not content:
                print('Downloader has not URLs saved in Memory yet, run Downloader.search_urls to find pics first')
        for name, (path, url) in content.items():
            with open(os.path.join(path, name), 'wb') as file:
                file.write(url.content)
            if verbose:
                print(f'File Name={name}, Downloaded from {url.url}')
            else:
                pass

    def _create_directories(self, name):
        dir_path = os.path.join(self._directory, name)
        try:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        except OSError:
            raise
        self.get_dirs.update([name])
        return

    def generate_dir(self, dir_name):
        """Generate Path and Directory, also check if Directory exists or not """
        dir_name = dir_name.replace(" ", "_")
        if dir_name in self.get_dirs:
            pass
        else:
            self._create_directories(dir_name)
        return os.path.join(self._directory, dir_name)

    @staticmethod
    def gen_fn(check, name):
        """Create a file name string and generate a random identifiers otherwise won't import same pic twice"""
        id = str(hex(random.randrange(1000)))
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(check.content)
        file_extension = f'.{file_type.split("/")[1]}'
        file_name = str(name) + "_" + id[2:] + file_extension
        return file_name

    def flush_cache(self):
        """Clear the Downloader instance cache"""
        self._cached_urls = set()