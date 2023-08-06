import requests
def strip_url(url):
    """Remove trailing / from url.

    :param url: URL
    :type url: str
    :returns: URL
    :rtype: str
    """

    return url.strip('/')

def url_to_domain(url):
    """Get domain name from url.

    :param url: URL
    :type url: str
    :returns: Domain of the URL
    :rtype: str
    """
    try:
        domain = strip_url(url).split("://")
        return domain[1]
    except:
        print("Invalid URL"+str(url))
        return None

def href_to_url(url,href):
    """Get Absolute URL from scraped href.

    :param url: URL
    :type url: str
    :param href: href from scraping
    :type href: str
    :returns: Absolute URL of href
    :rtype: str
    """

    url = strip_url(url)
    if href.startswith("//"):
        return href[2:]
    elif href.startswith("favicon/"):
        return url.rsplit('/',1)[0]+'/'+href
    elif href.startswith("data"):
        return href
    elif href.startswith('/'):
        return url+href
    elif href.startswith('.'):
        return url.rsplit('/',1)[0]+'/'+href
    elif "www" not in href:
        return url.rsplit('/',1)[0]+'/'+href
    else:
        return href

def check(url,method='get',post_data=None,json_data=None,timeout=3):
    """Check validity of request.

    :param url: URL
    :type url: str
    :param method: Method of Request
    :type method: str
    :param post_data: Post data (if any)
    :type post_data: dict, optional
    :param json_data: Request header as json
    :param timeout: timeout for request
    :type timeout: int
    :returns: Validity of request
    :rtype: bool
    """
    try:
        if method=='get':
            try:
                return requests.get(url,params=json_data,timeout=timeout).status_code == 200
            except:
                return False
        elif method=='post':
            try:
                return requests.post(url,data=post_data,json=json_data,timeout=timeout).status_code == 200
            except:
                return False
        else:
            return False
    except Exception as e:
        print(e)
        return False

def checklist(urllist):
    """Check validity of headerless get request to a list of URLs.

    :param urllist: list of URLs
    :type url: list
    :returns: list of valid URLs
    :rtype: list
    """

    l = []
    for url in urllist:
        if check(url):
            l.append(url)
    return l

