#!/bin/sh
echo "This script will fetch the contents of the xHamster bundle"
echo "into the  plex Plug-ins folder/directory and copy the"
echo "current xHamster bundle into xHamster.bundle.zz.bak if it"
echo "already exists"
echo "In order to function properly you must pass the directory within"
echo "which you installed plex."
echo "That plex directory will reside directly above the"
echo "\"Library/Application Support/Plex Media Server\" directory"
echo "Hit return to continue"
read garbage

myplexserverbase=$1
if [ -z "${myplexserverbase}" ]
then
echo "You must pass the plex install dir as an argument, eg:"
echo "./install.sh /some/path/to/plex "
echo "and wrap it in double quotes if it has spaces"
echo "./install.sh \"/some path/with spaces/to plex\" "
exit
fi
if [ ! -d "${myplexserverbase}/Library/Application Support/Plex Media Server/Plug-ins/" ]
then
echo  the plex server directory you passed in does not contain Plug-ins
exit
fi
cd "${myplexserverbase}/Library/Application Support/Plex Media Server/Plug-ins/"
wget -O xHamster.bundle-master.zip --no-check-certificate \
https://github.com/johnny8ch/xHamster.bundle/archive/master.zip
unzip  xHamster.bundle-master.zip
ext=""
cnt=0
if [ -d xHamster.bundle ]
then
cnt=`expr $cnt + 1`
ext=".bak.${cnt}"
while [ -d xHamster.bundle${ext} ]
do
cnt=`expr $cnt + 1`
ext=".bak.${cnt}"
done
mv  -f xHamster.bundle xHamster.bundle${ext}
fi
mv -f xHamster.bundle-master xHamster.bundle
rm xHamster.bundle-master.zip
