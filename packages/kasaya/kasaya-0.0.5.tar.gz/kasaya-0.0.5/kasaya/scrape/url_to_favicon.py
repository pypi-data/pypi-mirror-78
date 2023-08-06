import sys
from os import path
import requests
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from utils import *
from multiprocessing import Pool


def find_favicon(soup):
    """Find href of favicon from soup.

    :param soup: URL
    :type soup: BeautifulSoup (parsed HTML)
    :returns: href of favicon
    :rtype: string
    """

    if soup.find('link', rel='shortcut icon'):
        return soup.find('link', rel='shortcut icon')
    elif soup.find('link', rel='apple-touch-icon'):
        return soup.find('link', rel='apple-touch-icon')
    elif soup.find('link', rel='icon'):
        return soup.find('link', rel='icon')
    elif soup.find('link', rel='mask-icon'):
        return soup.find('link', rel='mask-icon')
    else:
        return
    
def guess_favicon(url):
    """Guess possible favicon location.

    :param url: URL
    :type url: str
    :returns: Absolute URL favicon
    :rtype: str
    """
    if check(url+'/favicon.ico'):
        return url+'/favicon.ico'
    else:
        pass

def favicon(url,method='get',post_data=None,json_data=None):
    """find URL of favicon from a request.

    :param url: URL
    :type url: str
    :param method: Method of Request
    :type method: str
    :param post_data: Post data (if any)
    :type post_data: dict
    :param json_data: Request header as json
    :returns: Absolute URL of favicon
    :rtype: str
    """

    url = strip_url(url)
    if not (check(url,method='get',post_data=None,json_data=None)):
        return None
    soup = soupify(url,method=method,post_data=post_data,json_data=json_data)
    if soup:
        if find_favicon(soup) !=None:
            try:
                _favurl = find_favicon(soup)['href']
                return href_to_url(url,_favurl)
            except:
                return guess_favicon(url)

        else:
            return guess_favicon(url)
    else:
        print("No Soup for the URL")
        return None

def favlist(urllist,p=5):
    """Get list of favicons from a urllist.

    :param urllist: list of urls
    :type urllist: list
    :param p: Number of thread Pool
    :type p: int
    :returns: List of favicons
    :rtype: list
    """

    with Pool(processes=p) as pool:
        result = pool.map(favicon, urllist)
        return result