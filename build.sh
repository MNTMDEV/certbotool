#! /bin/bash
[ -d script/output/rpmbuild/SOURCES ] || mkdir -p script/output/rpmbuild/SOURCES
tar -zcvf script/output/rpmbuild/SOURCES/certbotool.tar.gz ./src ./deploy
PROJECT_ROOT=`pwd`
cd script/output/rpmbuild
pwd
rpmbuild -bb $PROJECT_ROOT/script/certbotool-crond.spec --define="_topdir `pwd`"
rpmbuild -bb $PROJECT_ROOT/script/certbotool-plugins.spec --define="_topdir `pwd`"
rpmbuild -bb $PROJECT_ROOT/script/certbotool.spec --define="_topdir `pwd`"