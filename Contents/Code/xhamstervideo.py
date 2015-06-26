# -*- coding: utf-8 -*-
from xhamsterutil import L

################################################################################
@route(PREFIX+'/videos')
def xhamster_videos():
  from xhamstervideostraight import xhamster_videos_straight
  from xhamstervideogays import xhamster_videos_gays
  from xhamstervideotranssexuals import xhamster_videos_transsexuals

  oc = ObjectContainer( title2 = L("Videos") )

  oc.add(DirectoryObject(
    key = Callback( xhamster_videos_straight ),
    title = L("Straight"),
    summary = L("straight videos"),
    thumb = R(STRAIGHT_ICON)
  ))

  oc.add(DirectoryObject(
    key = Callback( xhamster_videos_gays ),
    title = L("Gays"),
    summary = L("gay videos"),
    thumb = R(GAYS_ICON)
  ))

  oc.add(DirectoryObject(
    key = Callback( xhamster_videos_transsexuals ),
    title = L("Transsexuals"),
    summary = L("transsexual videos"),
    thumb = R(TRANSSEXUALS_ICON)
  ))

  return oc

################################################################################
@route(PREFIX+'/videos/list', page = int)
def xhamster_videos_list(title, url, page = 1):
  if XHAMSTER_DEBUG: Log.Info("[XHAMSTER] xhamster_videos_list *** url " + url + " ***")

  oc = ObjectContainer( title2 = unicode( title ) + " | " + L("Page") + " " + str(page) )

  data = HTML.ElementFromURL( url )

  # TODO: exclude promoted videos
  videos = data.xpath('//div[contains(@class, "video")]')

  for video in videos:
    if XHAMSTER_DEBUG: Log.Info(HTML.StringFromElement(video))
    video_url = video.xpath('.//a/@href')[0]
    video_thumb = video.xpath('.//img/@src')[0]
    video_title = video.xpath('.//img/@alt')[0].strip()
    oc.add(VideoClipObject(
      url = video_url,
      title = video_title,
      thumb = Resource.ContentsOfURLWithFallback(url = video_thumb),
      art = Resource.ContentsOfURLWithFallback(url = video_thumb)
    ))

  next_a = data.xpath('//div[@class="pager"]//a[contains(@class,"last")]')
  if len(next_a) > 0:
    if XHAMSTER_DEBUG: Log.Info(HTML.StringFromElement(next_a[0]))
    oc.add(NextPageObject(
      key = Callback(
        xhamster_videos_list,
        title = title,
        url = next_a[0].xpath('./@href')[0],
        page = page + 1
      ),
      title = L('Next') + ' >>'
    ))

  return oc
