import types, re, random, datetime
import urllib2
from lxml.html import soupparser

NAME = 'xHamster'## setup html element for clips page
XH_BASE = 'http://xhamster.com'
XH_CHANNELS = 'http://xhamster.com/'
XH_CHANNEL = 'http://xhamster.com/channels/%s-%s-%s.html'

#######################################################################################################
def getrandartidx():
    rand = datetime.datetime.now().microsecond%3
    return rand


XHART = [ 'artwork-1.jpg',
          'artwork-2.jpg',
          'artwork-3.jpg'
        ]

HAMSTERHEADS = [   'hamsterhead-1.h0.jpg',
                   'hamsterhead-1.h30.jpg',
                   'hamsterhead-1.h60.jpg',
                   'hamsterhead-1.h90.jpg',
                   'hamsterhead-1.h120.jpg',
                   'hamsterhead-1.h150.jpg',
                   'hamsterhead-1.h180.jpg',
                   'hamsterhead-1.h210.jpg',
                   'hamsterhead-1.h240.jpg',
                   'hamsterhead-1.h270.jpg',
                   'hamsterhead-1.h300.jpg',
                   'hamsterhead-1.h330.jpg'
            ]

                
                
ART = XHART[ getrandartidx() ]
ICON = 'icon-default.png'
ICON_PREFS  = 'icon-prefs.png'
NXT = 'dudehamsterwheel.png'
PRV = 'hamsterback.jpg'
XH_MYDEBUG = 0
PLUGIN_PREFIX='/video/xhamster'
## globals
xh_maxpg = 0
xh_initpg = False
xh_pg1str=''
xh_clipsstr=''
xh_clipsperpage=12


def xhloginfo( infostr):
    if XH_MYDEBUG == 1:
        Log.Info( infostr)


####################################################################################################
def Start():
    global XHART
    
    arturl = XHART[ getrandartidx() ]
    HTTP.CacheTime = CACHE_1HOUR
    #HTTP.CacheTime = 0
    ObjectContainer.art = arturl
    HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:23.0) Gecko/20100101 Firefox/23.0'
        

###################################################################################################
@handler('/video/xhamster', NAME, ICON, ART )
def Main():
    global XHART
    
    arturl = XHART[ getrandartidx() ]
    oc = ObjectContainer( no_cache=True, no_history=False, title1=NAME, replace_parent=False,
                          art=R(arturl))
    
    oc.add( DirectoryObject(
                    key = Callback(ShowChannels),
                    title = 'Channels',
                    thumb=R(NXT)
            ))

    return oc

##############################################################################################################
@route('/video/xhamster/showchannels')
def ShowChannels( ):
    global XHART
    
    arturl = XHART[ getrandartidx() ]
    oc = ObjectContainer( replace_parent=False,  title1='Channels', no_history=False,
                           art=R(arturl))
                          
    pageContent = HTML.ElementFromURL(XH_CHANNELS)
    q = pageContent.xpath( "//a/@href[re:test( ., '^\/channels.*\.html', 'i' )]",
         namespaces={"re": "http://exslt.org/regular-expressions"})
    xhloginfo( "testing 234")
    getchan = re.compile( r'(.*)-(.*?)\.html')
    

    chancnt=int(1)
    ## add page for basic latest vids
    titxt = 'New'
    oc.add(DirectoryObject(
                    key = Callback(PageRange, title1=titxt, chanurl='/new', page=1, initpgstr='true'),
                    title = titxt,
                    ## had to put this png image here or android doesnt use thumbnails
                    thumb=R( 'hamsterhead-1.h30.png' )
            ))
            
    for chan in q:
        chancnt = chancnt + 1
        match = getchan.search( chan)
        if match:
            basechan = match.group( 1)
        xhloginfo( "in loop")
        tit = chan.getparent()
        xhloginfo( "jhok1")
        if( tit is types.NoneType ):
            xhloginfo( 'jhnonetit')
            continue
        titxt = tit.text
        if( titxt is None ):
            continue
        xhloginfo( 'jh tit url: ' + titxt + chan )
        wintitle = titxt
        itmtitle = titxt[:10]
        oc.add(DirectoryObject(
                #key = Callback(ClipsPage, pgcin='', title=titxt, chanurl=basechan, page=1, initpgstr='false'),
                #key = Callback(Picker, title1=titxt, chanurl=basechan, page=1, initpgstr='true'),
                key = Callback(PageRange, title1=wintitle, chanurl=basechan, page=1, initpgstr='true'),
                title = itmtitle,
                thumb=R( HAMSTERHEADS[ chancnt%12] )
        ))


    return oc
        
#################################################################################################################
@route( '/video/xhamster/showchannels/pagerange')
def PageRange( title1, chanurl, page=0, initpgstr='true'):
    global xh_initpg
    global xh_pg1str
    global XHART
    
    arturl = XHART[ getrandartidx() ]
    
    xh_initpg = True

    oc = ObjectContainer(title1=title1,replace_parent=False,no_history=False,
                          art=R(arturl))


    ### setup paging ahead of time
    xh_pg1str=''
    if xh_initpg:
        xhloginfo( 'getting page info for chanurl: ' + chanurl)
        if ( chanurl == '/new' ) :
            pg1f = urllib2.urlopen( XH_BASE + chanurl + '/' + page + '.html') 
            #pageContent = HTML.ElementFromURL( XH_BASE + chanurl + '/' + page + '.html')
        else:
            pg1f = urllib2.urlopen( XH_BASE + chanurl + '-' + page + '.html')
            #pageContent = HTML.ElementFromURL( XH_BASE + chanurl + '-' + page + '.html')
        xh_pg1str = pg1f.read()
        maxpglcl = int(setmaxpg( xh_pg1str))
    
    fullgroups = maxpglcl/100
    
    
    for i in range( 1, fullgroups+1):
        pgst = (i-1)*100 + 1
        pgend = i*100
        wintitle = 'Pages: ' + str(pgst) + '-' + str(pgend)
        itmtitle = wintitle
        oc.add(DirectoryObject(
                    key =  Callback(Picker, title1=wintitle, chanurl=chanurl, pgsts=pgst, pgends=pgend, subpgstr=1),
                    title = itmtitle
            )) 
    
    #lastgroup
    tst=maxpglcl%100
    if ( tst > 0 ):
        pgst = fullgroups*100 + 1
        pgend = fullgroups*100 + maxpglcl%100
        wintitle = 'Pages: ' + str(pgst) + '-' + str(pgend)
        itmtitle = wintitle
        oc.add(DirectoryObject(
                        key = Callback(Picker, title1=wintitle, chanurl=chanurl, pgsts=pgst, pgends=pgend, subpgstr=1),
                        title = itmtitle
                ))
    
            
    return oc
##############################################################################################################      
      
      
      

#################################################################################################
@route('/video/xhamster/showchannels/pagerange/picker')
def Picker( title1, chanurl, pgsts, pgends, subpgstr ):
    global XHART
    
    arturl = XHART[ getrandartidx() ]
    
    pgst = int( pgsts)
    pgend = int( pgends)
    
    oc = ObjectContainer(title1=title1, replace_parent=False, no_history=False,
                          art=R(arturl))
   
    rngend = pgend+1
    for i in range(pgst, rngend):
        wintitle = 'Page ' + str(i)
        itmtitle = wintitle
        oc.add(DirectoryObject(
                    #key = Callback(ClipsPage, title=wintitle, chanurl=chanurl, page=i, subpgstr='1', pgsts=pgsts, pgends=pgends),
                    key = Callback(SubPicker, title1=wintitle, chanurl=chanurl, pagestr=i, subpgstr=subpgstr, pgsts=pgsts, pgends=pgends),
                    #title = title1 + ' > Page ' + str(i) +' > Part 1'
                    title = itmtitle
            ))
            
    xh_initpg=False
    return oc
    
##################################################################################################
def getnclips( ):
    global xh_vidpg
    
    initialXpath = "//div[@class='video']"
    itemcnt = 0
    for videoItem in xh_vidpg.xpath(initialXpath):
        itemcnt += 1
    return itemcnt
    
#################################################################################################
@route('/video/xhamster/showchannels/picker/subpicker')
def SubPicker( title1, chanurl, pagestr, subpgstr, pgsts, pgends):
    global xh_clipsstr
    global xh_vidpg
    global xh_pg1str
    global XHART
    
    arturl = XHART[ getrandartidx() ]

    pgst = int( pgsts)
    pgend = int( pgends)
    subpage = int( subpgstr)
    page = int( pagestr)
    
    ####### count clips on page
    if( subpage == 1):
        if ( page == 1 ):
            ## already hit page once to get count of pages for channel
            xhloginfo( 'jhzfirstelemnt')
            #pageContent = soupparser.fromstring( xh_pg1str)
            xh_clipsstr = xh_pg1str
        else:
            xhloginfo( 'getting page info for chanurl: ' + chanurl)
            if ( chanurl == '/new' ) :
                clipsf = urllib2.urlopen( XH_BASE + chanurl + '/' + pagestr + '.html') 
                #pageContent = HTML.ElementFromURL( XH_BASE + chanurl + '/' + page + '.html')
            else:
                clipsf = urllib2.urlopen( XH_BASE + chanurl + '-' + pagestr + '.html')
                #pageContent = HTML.ElementFromURL( XH_BASE + chanurl + '-' + page + '.html')
            xh_clipsstr = clipsf.read()
        xh_vidpg = soupparser.fromstring( xh_clipsstr)
        nclips = int(getnclips( ) )
        xhloginfo( "jhznclips: " + str(nclips))
        ## setup html element for clips page
        xhloginfo( 'jhzz setting xh_vidpg global')
        
    oc = ObjectContainer(title1=title1, replace_parent=False, no_history=False,
                          art=R(arturl))

    subpgcnt = (nclips-1)/xh_clipsperpage + 1
    for i in range(1, subpgcnt):
        clipidx1 = (i-1) * xh_clipsperpage +1
        clipidx2 = xh_clipsperpage * i
        wintitle = 'CLIPS ' + str( clipidx1) + '-' + str( clipidx2)
        itmtitle = wintitle
        oc.add(DirectoryObject(
                    key = Callback(ClipsPage, title=wintitle, chanurl=chanurl, page=page, subpgstr=i, pgsts=pgsts, pgends=pgends),
                    #title = title1 + ' > Page ' +pagestr+' > Part '+str(i)
                    title = itmtitle
            ))
    i=subpgcnt
    clipidx1 = (i-1) * xh_clipsperpage +1
    clipidx2 = nclips
    wintitle = 'CLIPS ' + str( clipidx1) + '-' + str( clipidx2)
    itmtitle = wintitle
    oc.add(DirectoryObject(
                key = Callback(ClipsPage, title=wintitle, chanurl=chanurl, page=page, subpgstr=i, pgsts=pgsts, pgends=pgends),
                #title = title1 + ' > Page ' +pagestr+' > Part '+str(i)
                title = itmtitle
        ))
            
    xh_initpg=False
    return oc

        
########################################################################################################
def setmaxpg( rootstr):
    root = soupparser.fromstring( rootstr)
    pg = root.xpath( "//div[@class='pager']" )
    print len(pg)
    maxpg=0
    anchs = pg[0].xpath( '*//a')
    for ank in anchs:
        if ( ank.text is not None ):
            print 'txt: ' + ank.text
            try:
                maxpg = int(ank.text)
            except:
                poo = 1
        else:
            dv = ank.xpath( 'div')
            if len(dv) > 0:
                print 'tail:' +  dv[0].tail
        hr = ank.xpath( '@href')
        if ( hr is not None ):
            print hr
    xhloginfo( "maxpg: " + str(maxpg) )
    xh_maxpg = int(maxpg)         
    return maxpg

####################################################################################################
### recursive calls cause slowdown for unknown reason
@route('/video/xhamster/showchannels/pagerange/picker/subpicker/clipspage', method='GET')
def ClipsPage( title, chanurl, page, subpgstr, pgsts, pgends):
    global xh_pg1str
    global xh_clipsstr
    global xh_vidpg
    global XHART
    
    arturl = XHART[ getrandartidx() ]
    
    
    subpage = int(subpgstr)
    
    xhloginfo( 'jhzzClipsPage page='+page+' subpage='+subpgstr)
    if( subpage > 1):
        reparent = True
    else:
        reparent = False
    oc = ObjectContainer( title1=title, replace_parent=reparent, no_history=True,
                         no_cache=True,art=R(arturl))
                         
    xhloginfo( 'chanurl: ' + chanurl)
    
    
    initialXpath = "//div[@class='video']"
    itemcnt = 0
    nxtpage = 0
    minitm = (subpage-1)*xh_clipsperpage+1
    maxitm = subpage*xh_clipsperpage
    for videoItem in xh_vidpg.xpath(initialXpath):
        itemcnt += 1
        xhloginfo( 'jhzitemcnt: '+str(itemcnt))
        if( itemcnt < minitm):
		    continue
        if( itemcnt > maxitm ):
            break
        ht = videoItem.xpath( 'a/@href')
        xhloginfo( 'linkage:'+ht[0])
        vtit = videoItem.xpath( 'a/img/@alt' )
        videoItemTitle = vtit[0]
        videoItemLink  = videoItem.xpath('a')[0].get('href')
        videoItemThumb = videoItem.xpath('a/img')[0].get('src')         
        vtm = videoItem.xpath( 'a/b')
        duration = vtm[0].text
        #videoItemDuration = GetDurationFromString(duration)
        videoItemRating = (len(videoItem.xpath('img[contains(@src,"/star.gif")]'))+(float(len(videoItem.xpath('img[contains(@src,"/starhalf.gif")]')))/2))*2
        videoItemSummary = 'Duration: ' + duration
        #videoItemSummary += '\r\nRating: ' + str(videoItemRating)
        xhloginfo('videoItemTitle: '+videoItemTitle+' | videoItemLink: '+videoItemLink+' | videoItemThumb: '+videoItemThumb+' | videoItemSummary: '+videoItemSummary)
        #thumb = Resource.ContentsOfURLWithFallback( videoItemThumb)
        #timg = Resource.ContentsOfURLWithFallback(url=videoItemThumb)
        oc.add(EpisodeObject(
                url = videoItemLink,
                show=NAME,
                season=int(page),
                index=int(itemcnt),
                title = videoItemTitle[:10],
                thumb = Resource.ContentsOfURLWithFallback(url=videoItemThumb, fallback=PRV)
        ))
    
    if( 6==9 ):
        if( itemcnt > maxitm ):
            ### Next supbage
            nxtpgt = title+'/Pg:'+page+'_'+str(subpage+1)
            oc.add(DirectoryObject(
                        key = Callback( ClipsPage, title=title, chanurl=chanurl, page=page, subpgstr=subpage+1, pgsts=pgsts, pgends=pgends),
                        #key = Callback( Picker, title1=title, chanurl=chanurl, pgsts=pgsts, pgends=pgends, substr=subpage+1),
                        title = nxtpgt,
                        thumb = R(NXT)
            ))
        else:
            ### Next supbage
            nxtpgt = title
            oc.add(DirectoryObject(
                        #key = Callback( ClipsPage, title=title, chanurl=chanurl, page=page, subpgstr=subpage+1, pgsts=pgsts, pgends=pgends),
                        key = Callback( Picker, title1=title, chanurl=chanurl, pgsts=pgsts, pgends=pgends, subpgstr=1),
                        title = nxtpgt,
                        thumb = R(NXT)
            ))
    
    
    if len(oc) < 1:
        return ObjectContainer(header="Empty", message="This channel doesn't contain any videos.")
    else:
        #oc.objects.sort(key = lambda obj: obj.index)
        return oc
    
    
