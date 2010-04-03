rm -rf /tmp/wtwww
svn export . /tmp/wtwww
cd /tmp
tar -zcvf wtwww.tar.gz wtwww
zip -r -9 wtwww.zip wtwww
