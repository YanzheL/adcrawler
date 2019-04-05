from urllib.parse import *


# def fix_url(url):
#     type, path = splittype(url)
#     host, _ = splithost(path)
#     if not type:
#         type = 'http'
#         url = '{}://{}'.format(type, url)
#
#     if type not in ('http', 'https') or not host:
#         return None
#     # return '%s://%s' % (type, host)
#     return url

def fix_url(url):
    if not url:
        return
    if not isinstance(url, str):
        print(' Fuck type = {} '.format(type(url)).center(80, '-'))
    res = urlsplit(url, 'http', False)
    if res.scheme not in ('http', 'https'):
        return None
    if not res.netloc:
        return None
    return urlunsplit(res)


def process_links(links):
    for link in links:
        link.url = fix_url(link.url)
    return links
