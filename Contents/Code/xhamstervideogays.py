# -*- coding: utf-8 -*-
from xhamsterutil import L
from xhamstervideo import xhamster_videos_list

XHAMSTER_VIDEOS_LATEST_GAYS = '{0}/?content=gay'.format(XHAMSTER_BASE_URL)
XHAMSTER_VIDEOS_HD_GAYS = '{0}/channels/new-hd_gays-1.html'.format(XHAMSTER_BASE_URL)

################################################################################
@route(PREFIX+'/videos/gays')
def xhamster_videos_gays():

  ObjectContainer.art = R(GAYS_ART)
  DirectoryObject.art = R(GAYS_ART)

  oc = ObjectContainer( title2 = L("Gays Videos") )

  oc.add(DirectoryObject(
    key = Callback(
      xhamster_videos_list,
      title = L("Last Added") + " - " + L("Gays"),
      url = XHAMSTER_VIDEOS_LATEST_GAYS
    ),
	  title = L("Last Added"),
    summary = L("new gay porn videos")
  ))

  oc.add(DirectoryObject(
    key = Callback( xhamster_videos_gays_categories ),
	  title = L("Categories"),
    summary = L("choose a category")
  ))

  oc.add(DirectoryObject(
    key = Callback( xhamster_videos_gays_top ),
	  title = L("Top Rated"),
    summary = L("top rated gay porn videos")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      xhamster_videos_list,
      title = L("HD Porn") + " - " + L("Gays"),
      url = XHAMSTER_VIDEOS_HD_GAYS
    ),
	  title = L("HD Porn"),
    summary = L("HD gay porn videos")
  ))

  return oc

################################################################################
@route(PREFIX+'/videos/gays/top')
def xhamster_videos_gays_top():
  if XHAMSTER_DEBUG: Log.Info("[XHAMSTER] xhamster_videos_gays_top")

  oc = ObjectContainer(
    title2 = unicode ( L("Top Rated") + " - " + L("Gays") ),
  )

  # We have to force fetching the headers or CookiesForURL won't work
  request = HTTP.Request(XHAMSTER_VIDEOS_LATEST_GAYS)
  headers = request.headers
  cookies = HTTP.CookiesForURL(XHAMSTER_VIDEOS_LATEST_GAYS)
  HTTP.Headers['Cookie'] = cookies
  if XHAMSTER_DEBUG: Log.Info("#### COOKIES #### " + cookies)

  oc.add(DirectoryObject(
    key = Callback(
      xhamster_videos_list,
      title = L("Daily Top") + " - " + L("Gays"),
      url = XHAMSTER_VIDEOS_TOP_1DAY
    ),
    title = L("Daily"),
    summary = L("last day top rated gays videos")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      xhamster_videos_list,
      title = L("Weekly Top") + " - " + L("Gays"),
      url = XHAMSTER_VIDEOS_TOP_7DAYS
    ),
    title = L("Weekly"),
    summary = L("last week top rated gays videos")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      xhamster_videos_list,
      title = L("Monthly Top") + " - " + L("Gays"),
      url = XHAMSTER_VIDEOS_TOP_30DAYS
    ),
    title = L("Monthly"),
    summary = L("last month top rated gays videos")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      xhamster_videos_list,
      title = L("All Time Top") + " - " + L("Gays"),
      url = XHAMSTER_VIDEOS_TOP
    ),
    title = L("All Time"),
    summary = L("all time top rated gays videos")
  ))

  return oc

################################################################################
@route(PREFIX+'/videos/gays/categories')
def xhamster_videos_gays_categories():
  if XHAMSTER_DEBUG: Log.Info("[XHAMSTER] xhamster_videos_gays_categories")

  oc = ObjectContainer(
    title2 = L("Categories") + " - " + L("Gays"),
    no_cache = True
  )

  data = HTML.ElementFromURL(
    XHAMSTER_VIDEOS_CATEGORIES,
    cacheTime = 0
  )

  xpath_string = '//div[text()="' + L("Gays") + '"]/parent::div/following-sibling::div/a'
  categories = data.xpath(xpath_string)

  # categories is a 5 column list. Order categories
  ordered_categories = []
  for i in list(range(0,5)):
    ordered_categories += categories[i::5]

  for category in ordered_categories:
    if XHAMSTER_DEBUG: Log.Info(HTML.StringFromElement(category))
    try:
      url = category.xpath('./@href')[0]
    except:
      continue
    name = category.xpath('./text()')[-1].strip()
    oc.add(DirectoryObject(
      key = Callback(
        xhamster_videos_list,
        title = name,
        url = url
      ),
      title = unicode(name)
    ))

  return oc
