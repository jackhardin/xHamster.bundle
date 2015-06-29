# -*- coding: utf-8 -*-
from xhamsterutil import L
from xhamstervideo import xhamster_videos_list

XHAMSTER_VIDEOS_LATEST_TRANSSEXUALS = '{0}/?content=shemale'.format(XHAMSTER_BASE_URL)
XHAMSTER_VIDEOS_HD_TRANSSEXUALS = '{0}/channels/new-hd_shemales-1.html'.format(XHAMSTER_BASE_URL)

################################################################################
@route(PREFIX+'/videos/transsexuals')
def xhamster_videos_transsexuals():

  ObjectContainer.art = R(TRANSSEXUALS_ART)
  DirectoryObject.art = R(TRANSSEXUALS_ART)

  oc = ObjectContainer( title2 = L("Transsexuals Videos") )

  oc.add(DirectoryObject(
    key = Callback(
      xhamster_videos_list,
      title = L("Last Added") + " - " + L("Transsexuals"),
      url = XHAMSTER_VIDEOS_LATEST_TRANSSEXUALS
    ),
	  title = L("Last Added"),
    summary = L("new transsexuals porn videos")
  ))

  oc.add(DirectoryObject(
    key = Callback( xhamster_videos_transsexuals_categories ),
	  title = L("Categories"),
    summary = L("choose a category")
  ))

  oc.add(DirectoryObject(
    key = Callback( xhamster_videos_transsexuals_top ),
	  title = L("Top Rated"),
    summary = L("top rated transsexuals porn videos")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      xhamster_videos_list,
      title = L("HD Porn") + " - " + L("Transsexuals"),
      url = XHAMSTER_VIDEOS_HD_TRANSSEXUALS
    ),
	  title = L("HD Porn"),
    summary = L("HD transsexuals porn videos")
  ))

  return oc

################################################################################
@route(PREFIX+'/videos/transsexuals/top')
def xhamster_videos_transsexuals_top():
  if XHAMSTER_DEBUG: Log.Info("[XHAMSTER] xhamster_videos_transsexuals_top")

  oc = ObjectContainer(
    title2 = L("Top Rated") + " - " + L("Transsexuals"),
  )

  # We have to force fetching the headers or CookiesForURL won't work
  request = HTTP.Request(XHAMSTER_VIDEOS_LATEST_TRANSSEXUALS)
  headers = request.headers
  cookies = HTTP.CookiesForURL(XHAMSTER_VIDEOS_LATEST_TRANSSEXUALS)
  HTTP.Headers['Cookie'] = cookies
  if XHAMSTER_DEBUG: Log.Info("#### COOKIES #### " + cookies)

  oc.add(DirectoryObject(
    key = Callback(
      xhamster_videos_list,
      title = L("Daily Top") + " - " + L("Transsexuals"),
      url = XHAMSTER_VIDEOS_TOP_1DAY
    ),
    title = L("Daily"),
    summary = L("last day top rated transsexuals videos")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      xhamster_videos_list,
      title = L("Weekly Top") + " - " + L("Transsexuals"),
      url = XHAMSTER_VIDEOS_TOP_7DAYS
    ),
    title = L("Weekly"),
    summary = L("last week top rated transsexuals videos")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      xhamster_videos_list,
      title = L("Monthly Top") + " - " + L("Transsexuals"),
      url = XHAMSTER_VIDEOS_TOP_30DAYS
    ),
    title = L("Monthly"),
    summary = L("last month top rated transsexuals videos")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      xhamster_videos_list,
      title = L("All Time Top") + " - " + L("Transsexuals"),
      url = XHAMSTER_VIDEOS_TOP
    ),
    title = L("All Time"),
    summary = L("all time top rated transsexuals videos")
  ))

  return oc

################################################################################
@route(PREFIX+'/videos/transsexuals/categories')
def xhamster_videos_transsexuals_categories():
  if XHAMSTER_DEBUG: Log.Info("[XHAMSTER] xhamster_videos_transsexuals_categories")

  oc = ObjectContainer(
    title2 = L("Categories") + " - " + L("Transsexuals"),
    no_cache = True
  )

  data = HTML.ElementFromURL(
    XHAMSTER_VIDEOS_CATEGORIES,
    cacheTime = 0
  )

  xpath_string = '//div[text()="' + L("Transsexuals") + '"]/parent::div/following-sibling::div/a'
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
