#!/bin/bash

#####################################################################
#
# This file is part of Old Standard font family
# (http://www.thessalonica.org.ru/en/oldstandard.html) and is
# Copyright (C) 2006-2011 Alexey Kryukov <amkryukov@gmail.com>.
#
# This Font Software is licensed under the SIL Open Font License,
# Version 1.1.
#
# You should have received a copy of the license along with this Font
# Software. If this is not the case, go to (http://scripts.sil.org/OFL)
# for all the details including a FAQ.
#
#####################################################################/

ZIP="zip -DrX"
PACK_NAME=oldstandard
DOCS="OFL.txt OFL-FAQ.txt FONTLOG.txt"
VERSION=$(grep '^Version:' sources/OldStandard-Regular.sfd | sed -e 's/^Version: //')

fontforge -script scripts/ost-generate.py

rm -f *.zip

$ZIP -j $PACK_NAME-$VERSION.ttf.zip fonts/ttf/*.ttf $DOCS
$ZIP -j $PACK_NAME-$VERSION.woff.zip fonts/woff/*.woff $DOCS
$ZIP -j $PACK_NAME-$VERSION.otf.zip fonts/otf/*.otf $DOCS
$ZIP $PACK_NAME-$VERSION.src.zip genfonts.sh scripts/ost-generate.py sources/*metadata.xml sources/*.sfd $DOCS
