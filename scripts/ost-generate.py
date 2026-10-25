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

import fontforge
from os.path import dirname
from os import makedirs

script_dir = dirname(__file__)
base_name = "OldStandard"
full_name = "Old Standard"
styles = ("Regular", "Italic", "Bold")

sources_dir = script_dir + "/../sources/"
otf_dir = script_dir + "/../fonts/otf/"
woff_dir = script_dir + "/../fonts/woff/"
ttf_dir = script_dir + "/../fonts/ttf/"

makedirs(otf_dir, exist_ok=True)
makedirs(woff_dir, exist_ok=True)
makedirs(ttf_dir, exist_ok=True)

def process_font(name, fname, style):

    filename = name + "-" + style
    font = fontforge.open(sources_dir + filename + ".sfd")

    # Add localized Fullname entries. Since we change family name for TTF output,
    # there is no reason to store them directly in the file
    ttnames = list( font.sfnt_names )
    for ttname in ttnames:
        if ttname[1] == 'SubFamily':
            ttnames.append( ( ttname[0],'Fullname',"%s %s" % ( fname,ttname[2] ) ) )
    font.sfnt_names = tuple( ttnames )

    font.gasp_version = 1
    font.gasp = (
            ( 10   , ( 'antialias', 'symmetric-smoothing' ) ),
            ( 20   , ( 'gridfit', 'gridfit+smoothing' ) ),
            ( 65535, ( 'antialias', 'gridfit', 'symmetric-smoothing', 'gridfit+smoothing' ) ),
        )
    font.generate( otf_dir + filename + ".otf",flags=( "opentype","winkern","no-FFTM-table","no-mac-names" ),layer="Fore" )

    woff_meta = base_name + "-WOFF-metadata.xml"
    f = open( sources_dir + woff_meta,'r' )
    lines = f.readlines()
    f.close()
    font.woffMetadata = "".join( lines )
    font.generate( woff_dir + filename + ".woff",flags=( "opentype","winkern","no-FFTM-table","no-mac-names" ),layer="TTF" )

    # Append the 'TT' suffix to various font names, including localized entries
    for i in range( 0,len( ttnames )):
        ttname = ttnames[i]
        if ttname[1] == 'Fullname':
            ttnames[i] = ( ttname[0],'Fullname',ttname[2].replace( fname,fname + " TT" ) )
    font.sfnt_names = tuple( ttnames )
    font.familyname = fname + " TT"
    font.fullname = fname + " TT " + style
    font.fontname = name + "TT-" + style

    font.generate(ttf_dir + filename + ".ttf",flags=( "opentype","winkern","no-FFTM-table","no-mac-names" ),layer="TTF" )

    font.close()

for style in styles:
    fontforge.setPrefs( "AutoHint",False )
    fontforge.setPrefs( "ClearInstrsBigChanges",False )
    fontforge.setPrefs( "CopyTTFInstrs",False )
    process_font( base_name, full_name, style )
