# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor


class AmazonPrimeIE(InfoExtractor):
#    _VALID_URL = r'https?://(?:www\.)?amazon\.com/gp/product/(?P<id>[A-Z0-9]+)'
    _VALID_URL = r'https?://(?:www\.)?amazon\.com/gp/product/(?P<product>[A-Z0-9]+)(\/ref=(?P<id>[a-z0-9_]+))?'
#    _VALID_URL = r'https?://(?:www\.)?amazon\.com/gp/product/(?P<list>[A-Z0-9]+)\/?(?P<id>[]'

    _TEST = {
        'url': 'http://www.amazon.com/gp/product/B00821P4NM',
        'md5': 'TODO: md5 sum of the first 10241 bytes of the video file (use --test)',
        'info_dict': {
            'id': '42',
            'ext': 'mp4',
            'title': 'Video title goes here',
            'thumbnail': 're:^https?://.*\.jpg$',
            # TODO more properties, either as:
            # * A value
            # * MD5 checksum; start the string with md5:
            # * A regular expression; start the string with re:
            # * Any Python type (for example int or float)
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        # TODO more code goes here, for example ...
 #       title = self._html_search_regex(r'<h1>(.*?)</h1>', webpage, 'title')
        title = self._html_search_regex(r'"application/ld\+json">.*,"episode":{"name":"([ a-zA-Z0-9,]+)', webpage, 'title')


        url = self._html_search_regex(r'"playerSwf":"([_:\/\.a-zA-Z0-9,-]+)', webpage, 'url')

#        print '#######  AMAZON initial page', webpage.encode('utf-8'), '#######  END AMAZON initial page'

        print 'Title:', title, "\nURL:", url

        import sys
#        sys.exit("Blah")


###  Deal with login stuff
        (username, password) = self._get_login_info()
         # No authentication to be performed
        if username is None:
            sys.exit('No login info available')
        import cookielib
        import urllib
        import urllib2

        login_data = urllib.urlencode({'action': 'sign-in',
                                       'email': username,
                                       'password': password,
                                       })

        cookie = cookielib.CookieJar()    
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
   #     opener.addheaders = [('User-agent', 'youtube-dl

        response = opener.open('https://www.amazon.com/gp/sign-in.html')
        print(response.getcode())

        response = opener.open('https://www.amazon.com/gp/flex/sign-in/select.html', login_data)
        print(response.getcode())
        

        self._downloader.cookiejar.set_cookie(cookie)

#        import time
#        self._set_cookie(
#            '.amazon.com', cookie,
            # YouTube sets the expire time to about two months
#            expire_time=time.time() + 2 * 30 * 24 * 3600)

        #response = opener.open("https://www.amazon.com/") # it should show that you are logged in
        #print(response.getcode())
        #import pprint
        #print(response)

# #        LOGIN_URL = 'https://www.amazon.com/gp/flex/sign-in/select.html'
#         LOGIN_URL = 'https://www.amazon.com/ap/signin'

#         (username, password) = self._get_login_info()
#         # No authentication to be performed
#         if username is None:
#             sys.exit('No login info available')

#         login_form_strs = {
#             'action': 'sign-in',
#             'email': username,
#             'password': password,
#             }


#         from ..compat import (
#             compat_chr,
#             compat_parse_qs,
#             compat_urllib_parse,
#             compat_urllib_request,
#             compat_urlparse,
#             compat_str,
#             )

#         login_form = dict((k.encode('utf-8'), v.encode('utf-8')) for k, v in login_form_strs.items())
#         login_data = compat_urllib_parse.urlencode(login_form).encode('ascii')

#         req = compat_urllib_request.Request(LOGIN_URL, login_data)
#         login_results = self._download_webpage(
#             req, None,
#             note='Logging in', errnote='unable to log in', fatal=False)
#         if login_results is False:
#             return False

#         print login_results.encode('utf-8')
#        sys.exit("Blah")



        url='http://amazon.com'
        return {
            'url': url,
            'id': video_id,
            'title': title,
            'description': self._og_search_description(webpage),
            # TODO more properties (see youtube_dl/extractor/common.py)
        }
