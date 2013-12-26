xHamster.bundle
===============

Video/Adult 18+ Plex-Plugin - Browse, search and watch videos from xHamster.com

==============================================================================================

ok, so this is attempt to get xHamster running with plex channels

i forked flownex xHamster bundle and uploaded __init__.py to get channel working.

the ServiceCode.pys file in Contents/Code directory must be copied on the plex server into the
directory:

YourPlexBase/Library/Application Support/Plex Media Server/Plug-ins/Services.bundle/Contents/Service
Sets/com.plexapp.plugins.xhamster/URL/xHamster

( nightmare path i know ! )

please backup the existing ServiceCode.pys to a new name before copying the one from this repository
--

the URL that is served will correspond to mp4 video file with h264/aac encoding.

direct plays on roku - but my linux plex web client wont direct play so it is a bit sketch on that --
but, most sweet on roku !!!

Interface is minimal - but functional

Njoy and dont blame me if you dont backup files and your s*^t breaks ;)


==============================================================================

if anyone from xhamster.com objects to use of this plugin, please advise me of your objection, and i
will remove immediately
