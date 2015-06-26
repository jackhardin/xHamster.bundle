# -*- coding: utf-8 -*-
TITLE  = u'xHamster'
PREFIX = '/video/xhamster'

XHAMSTER_BASE_URL = 'http://xhamster.com'

XHAMSTER_VIDEOS_CATEGORIES = '{0}/channels.php'.format(XHAMSTER_BASE_URL)
XHAMSTER_VIDEOS_TOP_1DAY = '{0}/rankings/daily-top-videos.html'.format(XHAMSTER_BASE_URL)
XHAMSTER_VIDEOS_TOP_7DAYS = '{0}/rankings/weekly-top-videos.html'.format(XHAMSTER_BASE_URL)
XHAMSTER_VIDEOS_TOP_30DAYS = '{0}/rankings/monthly-top-videos.html'.format(XHAMSTER_BASE_URL)
XHAMSTER_VIDEOS_TOP = '{0}/rankings/alltime-top-videos.html'.format(XHAMSTER_BASE_URL)

XHAMSTER_ICON     = 'xHamster.png'
ICON              = 'default.png'
SEARCH_ICON       = 'search.png'
SETTINGS_ICON     = 'preferences.png'

STRAIGHT_ICON     = 'straight.png'
GAYS_ICON         = 'gays.png'
TRANSSEXUALS_ICON = 'transsexuals.png'

STRAIGHT_ART     = 'straightArt.jpg'
GAYS_ART         = 'gaysArt.jpg'
TRANSSEXUALS_ART = 'transsexualsArt.jpg'

from xhamsterutil import L
from xhamstervideo import xhamster_videos
from xhamsterphoto import xhamster_photos
from xhamstersearch import xhamster_search

################################################################################
def Start():

  Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
  Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
  Plugin.AddViewGroup('PanelStream', viewMode='PanelStream', mediaType='items')

  HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0'
  HTTP.Headers['Connection'] = 'keep-alive'
  try:
    language = Prefs["language"].split("/")[1] + '.'
  except:
    language = 'en'
  HTTP.Headers['Accept-Language'] = language

  ObjectContainer.title1 = TITLE
  #ObjectContainer.view_group = 'List'
  ObjectContainer.art = R(STRAIGHT_ART)
  DirectoryObject.thumb = R(ICON)
  DirectoryObject.art = R(STRAIGHT_ART)
  PhotoAlbumObject.thumb = R(ICON)

  HTTP.CacheTime = CACHE_1HOUR

################################################################################
@handler(PREFIX, TITLE, art=STRAIGHT_ART, thumb=XHAMSTER_ICON)
def xhamster_main_menu():

  oc = ObjectContainer()

  oc.add(DirectoryObject(
    key = Callback(xhamster_videos),
	  title = L("Videos"),
    summary = L("xHamster videos")
  ))

  oc.add(DirectoryObject(
    key = Callback(xhamster_photos),
	  title = L("Photos"),
    summary = L("xHamster photos")
  ))

  if Client.Product != 'PlexConnect':
    oc.add(InputDirectoryObject(
      key     = Callback(xhamster_search),
      title   = L('Search xHamster Videos'),
      prompt  = L('Search for xHamster Videos'),
      summary = L('Search for xHamster Videos'),
      thumb   = R(SEARCH_ICON)
    ))

  return oc
