# -*- coding: utf-8 -*-
from xhamsterutil import L
from xhamsterutil import xhamster_get_redirect_url
from xhamstervideo import xhamster_videos_list

XHAMSTER_VIDEOS_LATEST_STRAIGHT = '{0}/?content=straight'.format(XHAMSTER_BASE_URL)
XHAMSTER_VIDEOS_HD_STRAIGHT = '{0}/channels/new-hd_videos-1.html'.format(XHAMSTER_BASE_URL)

XHAMSTER_VIDEOS_RECOMMENDATIONS = '{0}/recommended_for_me.php'.format(XHAMSTER_BASE_URL)

XHAMSTER_VIDEOS_RANDOM = '{0}/random.php'.format(XHAMSTER_BASE_URL)

################################################################################
@route(PREFIX+'/videos/straight')
def xhamster_videos_straight():

  ObjectContainer.art = R(STRAIGHT_ART)
  DirectoryObject.art = R(STRAIGHT_ART)

  oc = ObjectContainer( title2 = L("Straight Videos") )

  oc.add(DirectoryObject(
    key = Callback(
      xhamster_videos_list,
      title = L("Last Added") + " - " + L("Straight"),
      url = XHAMSTER_VIDEOS_LATEST_STRAIGHT
    ),
	  title = L("Last Added"),
    summary = L("new straight porn videos")
  ))

  oc.add(DirectoryObject(
    key = Callback( xhamster_videos_straight_categories ),
	  title = L("Categories"),
    summary = L("choose a category")
  ))

  oc.add(DirectoryObject(
    key = Callback( xhamster_videos_straight_top ),
	  title = L("Top Rated"),
    summary = L("top rated straight porn videos")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      xhamster_videos_list,
      title = L("HD Porn") + " - " + L("Straight"),
      url = XHAMSTER_VIDEOS_HD_STRAIGHT
    ),
	  title = L("HD Porn"),
    summary = L("HD straight porn videos")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      xhamster_videos_list,
      title = L("Recommendations"),
      url = XHAMSTER_VIDEOS_RECOMMENDATIONS
    ),
	  title = L("Recommendations"),
    summary = L("recommended for me")
  ))

  oc.add(DirectoryObject(
    key = Callback( xhamster_random ),
	  title = L("Random Video"),
    summary = L("show me a random video")
  ))

  return oc

################################################################################
@route(PREFIX+'/videos/straight/top')
def xhamster_videos_straight_top():
  if XHAMSTER_DEBUG: Log.Info("[XHAMSTER] xhamster_videos_straight_top")

  oc = ObjectContainer(
    title2 = L("Top Rated") + " - " + L("Straight"),
  )

  # We have to force fetching the headers or CookiesForURL won't work
  request = HTTP.Request(XHAMSTER_VIDEOS_LATEST_STRAIGHT)
  headers = request.headers
  cookies = HTTP.CookiesForURL(XHAMSTER_VIDEOS_LATEST_STRAIGHT)
  HTTP.Headers['Cookie'] = cookies
  if XHAMSTER_DEBUG: Log.Info("#### COOKIES #### " + cookies)

  oc.add(DirectoryObject(
    key = Callback(
      xhamster_videos_list,
      title = L("Daily Top") + " - " + L("Straight"),
      url = XHAMSTER_VIDEOS_TOP_1DAY
    ),
    title = L("Daily"),
    summary = L("last day top rated straight videos")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      xhamster_videos_list,
      title = L("Weekly Top") + " - " + L("Straight"),
      url = XHAMSTER_VIDEOS_TOP_7DAYS
    ),
    title = L("Weekly"),
    summary = L("last week top rated straight videos")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      xhamster_videos_list,
      title = L("Monthly Top") + " - " + L("Straight"),
      url = XHAMSTER_VIDEOS_TOP_30DAYS
    ),
    title = L("Monthly"),
    summary = L("last month top rated straight videos")
  ))

  oc.add(DirectoryObject(
    key = Callback(
      xhamster_videos_list,
      title = L("All Time Top") + " - " + L("Straight"),
      url = XHAMSTER_VIDEOS_TOP
    ),
    title = L("All Time"),
    summary = L("all time top rated straight videos")
  ))

  return oc

################################################################################
@route(PREFIX+'/videos/straight/categories')
def xhamster_videos_straight_categories():
  if XHAMSTER_DEBUG: Log.Info("[XHAMSTER] xhamster_videos_straight_categories")

  oc = ObjectContainer(
    title2 = L("Categories") + " - " + L("Straight"),
    no_cache = True
  )

  data = HTML.ElementFromURL(
    XHAMSTER_VIDEOS_CATEGORIES,
    cacheTime = 0
  )

  xpath_string = '//div[text()="' + L("Straight") + '"]/parent::div/following-sibling::div[1]/a'
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

################################################################################
@route(PREFIX+'/videos/straight/random')
def xhamster_random():
  if XHAMSTER_DEBUG: Log.Info("[XHAMSTER] xhamster_random")

  oc = ObjectContainer(
    title2 = L("Random Video"),
    no_cache = True
  )

  random_video = xhamster_get_redirect_url(XHAMSTER_VIDEOS_RANDOM)
  if XHAMSTER_DEBUG: Log.Info("*** redirect url " + random_video + " ***")
  oc.add(URLService.MetadataObjectForURL(random_video))

  return oc
