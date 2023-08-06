import sys
from os import path
from multiprocessing import Pool
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from utils import *

def images(url,method='get',post_data=None,json_data=None):
    """Find URL of images embeded in the reponse of request.

    :param url: URL
    :type url: str
    :param method: Method of Request
    :type method: str
    :param post_data: Post data (if any)
    :type post_data: dict
    :param json_data: Request header as json
    :returns: List of URL of images
    :rtype: list
    """

    l = []
    url = strip_url(url)
    if not (check(url,method='get',post_data=None,json_data=None)):
        return None
    soup = soupify(url,method=method,post_data=post_data,json_data=json_data)
    for link in soup.find_all("img"):
        try:
            imgurl = link['src']
            l.append(href_to_url(url,imgurl))
        except:
            pass
    return l

def imageslist(urllist,p=5):
    with Pool(processes=p) as pool:
        result = pool.map(images, urllist)
        return result