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
    scheme, netloc, path, query, fragment = urlsplit(url, 'http', False)
    if scheme not in ('http', 'https'):
        return None
    if not netloc:
        return None
    return urlunsplit(scheme, netloc, path, query, fragment)


def process_links(links):
    for link in links:
        link.url = fix_url(link.url)
    return links
