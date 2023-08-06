import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from utils import *

def childlist(url,method='get',post_data=None,json_data=None):
    """Find URLs embeded in the reponse of request.

    :param url: URL
    :type url: str
    :param method: Method of Request
    :type method: str
    :param post_data: Post data (if any)
    :type post_data: dict
    :param json_data: Request header as json
    :returns: List of embeded URLs
    :rtype: list
    """

    l = []
    url = strip_url(url)
    soup = soupify(url,method=method,post_data=post_data,json_data=json_data)

    for link in soup.find_all("a"):
        try:
            href = link.get('href')
            l.append(href_to_url(url,href))
        except Exception as e:
            print("Hop error: "+str(e))
    return l