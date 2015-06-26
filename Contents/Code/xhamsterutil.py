# -*- coding: utf-8 -*-
import urllib2

################################################################################
def L(string):
  Request.Headers['X-Plex-Language'] = Prefs["language"].split("/")[1]
  local_string = Locale.LocalString(string)
  return str(local_string).decode()

################################################################################
def xhamster_get_redirect_url(url):
  opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
  request = opener.open(url)
  return request.url
