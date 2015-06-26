# -*- coding: utf-8 -*-
from xhamsterutil import L
from xhamsterutil import xhamster_get_redirect_url

XHAMSTER_PHOTOS = '{0}/photos'.format(XHAMSTER_BASE_URL)
XHAMSTER_PHOTOS_CATEGORIES = XHAMSTER_PHOTOS
XHAMSTER_PHOTOS_TOP_7DAYS = '{0}/photos/rankings/weekly-rated.html'.format(XHAMSTER_BASE_URL)
XHAMSTER_PHOTOS_TOP_30DAYS = '{0}/photos/rankings/monthly-rated.html'.format(XHAMSTER_BASE_URL)
XHAMSTER_PHOTOS_TOP = '{0}/photos/rankings/alltime-rated.html'.format(XHAMSTER_BASE_URL)
XHAMSTER_PHOTOS_RANDOM = '{0}/random.php?type=gallery'.format(XHAMSTER_BASE_URL)

################################################################################
@route(PREFIX+'/photos')
def xhamster_photos():

  ObjectContainer.art = R(STRAIGHT_ART)
  DirectoryObject.art = R(STRAIGHT_ART)

  oc = ObjectContainer( title2 = L("Photos") )

  oc.add(DirectoryObject(
    key = Callback(
      xhamster_photos_album_list,
      url = XHAMSTER_PHOTOS,
      title = L("Last Added Albums")
    ),
    title = L("Last Added"),
    summary = L("last added porn photo albums")
  ))

  oc.add(DirectoryObject(
    key = Callback( xhamster_photos_album_categories ),
    title = L("Categories"),
    summary = L("choose a category")
  ))

  oc.add(DirectoryObject(
    key = Callback( xhamster_photos_top ),
	  title = L("Top Rated"),
    summary = L("top rated porn photos")
  ))

  oc.add(DirectoryObject(
    key = Callback( xhamster_photos_album_random ),
	  title = L("Random Album"),
    summary = L("show me a random porn photo album")
  ))

  return oc

################################################################################
@route(PREFIX+'/photos/album/categories')
def xhamster_photos_album_categories():
  if XHAMSTER_DEBUG: Log.Info("[XHAMSTER] xhamster_photos_album_categories")

  oc = ObjectContainer( title2 = L("Photo Albums Categories") )

  data = HTML.ElementFromURL( XHAMSTER_PHOTOS_CATEGORIES )

  categories = data.xpath('//div[@id="menuLeft"]/div[@class="list"][1]/a')

  for category in categories:
    if XHAMSTER_DEBUG: Log.Info(HTML.StringFromElement(category))
    try:
      url = category.xpath('./@href')[0]
    except:
      continue
    name = category.xpath('./text()')[-1].strip()
    oc.add(DirectoryObject(
      key = Callback(
        xhamster_photos_album_list,
        title = name,
        url = url
      ),
      title = unicode(name)
    ))

  return oc

################################################################################
@route(PREFIX+'/photos/top')
def xhamster_photos_top():

  oc = ObjectContainer(
    title2 = L("Top Rated Photos"),
  )

  oc.add(PhotoAlbumObject(
    url = XHAMSTER_PHOTOS_TOP_7DAYS,
    title = L("Weekly"),
    summary = L("last week top rated porn photo album")
  ))

  oc.add(PhotoAlbumObject(
    url = XHAMSTER_PHOTOS_TOP_30DAYS,
    title = L("Monthly"),
    summary = L("last month top rated porn photo album")
  ))

  oc.add(PhotoAlbumObject(
    url = XHAMSTER_PHOTOS_TOP,
    title = L("All Time"),
    summary = L("all time top rated porn photo album")
  ))

  return oc

################################################################################
@route(PREFIX+'/photos/album/list', page = int)
def xhamster_photos_album_list(title, url, page = 1):
  if XHAMSTER_DEBUG: Log.Info("[XHAMSTER] xhamster_photos_album_list")

  oc = ObjectContainer( title2 = unicode( title ) + " | " + L("Page") + " " + str(page) )

  data = HTML.ElementFromURL( url )

  albums = data.xpath('//div[contains(@class, "gallery")]')
  
  for album in albums:
    if XHAMSTER_DEBUG: Log.Info(HTML.StringFromElement(album))
    album_url = album.xpath('.//a/@href')[0]
    album_thumb = album.xpath('.//img/@src')[0]
    album_title = album.xpath('.//img/@title')[0]
    oc.add(PhotoAlbumObject(
      url = album_url,
      title = unicode(album_title),
      thumb = Resource.ContentsOfURLWithFallback(url = album_thumb),
      art = Resource.ContentsOfURLWithFallback(url = album_thumb)
    ))

  next_a = data.xpath('//div[@class="pager"]//a[contains(@class,"last")]')
  if len(next_a) > 0:
    if XHAMSTER_DEBUG: Log.Info(HTML.StringFromElement(next_a[0]))
    next_page = page + 1
    oc.add(NextPageObject(
      key = Callback(
        xhamster_photos_album_list,
        title = title,
        url = next_a[0].xpath('./@href')[0],
        page = next_page,
      ),
      title = L('Next') + ' >>'
    ))

  return oc

################################################################################
@route(PREFIX+'/photos/album/random')
def xhamster_photos_album_random():

  oc = ObjectContainer(
    title2 = L("Random Photo Album"),
    no_cache = True
  )

  random_album = xhamster_get_redirect_url(XHAMSTER_PHOTOS_RANDOM)
  oc.add(URLService.MetadataObjectForURL(random_album))

  return oc
