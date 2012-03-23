#!/usr/bin/env python

import os
import sys

sys.path.append ('../..')

from bockbuild.msysprofile import MSysProfile
from packages import MSysGtkPackages

abs_pathself = os.path.realpath (os.path.abspath (sys.argv[0]))

class MSysGtkProfile (MSysProfile, MSysGtkPackages):
	def __init__ (self):
		MSysProfile.__init__ (self)
		MSysGtkPackages.__init__ (self)
		
		self.gcc_flags.extend ([ '-g' ])
		
		self_dir = os.path.dirname (abs_pathself)
		
MSysGtkProfile ().build ()

profname = "msys-gtk-env"
dir = os.path.dirname (abs_pathself)

envscript = '''#!/bin/sh
PROFNAME="%s"
INSTALLDIR=%s/build-root/_install
export DYLD_FALLBACK_LIBRARY_PATH="$INSTALLDIR/lib:/lib:/usr/lib:$DYLD_FALLBACK_LIBRARY_PATH"
export C_INCLUDE_PATH="$INSTALLDIR/include:$C_INCLUDE_PATH"
export ACLOCAL_PATH="$INSTALLDIR/share/aclocal:$ACLOCAL_PATH"
export ACLOCAL_FLAGS="-I $INSTALLDIR/share/aclocal $ACLOCAL_FLAGS"
export PKG_CONFIG_PATH="$INSTALLDIR/lib/pkgconfig:$INSTALLDIR/lib64/pkgconfig:$INSTALLDIR/share/pkgconfig:$PKG_CONFIG_PATH"
#export CONFIG_SITE="$INSTALLDIR/$PROFNAME-config.site"
export MONO_GAC_PREFIX="$INSTALLDIR:MONO_GAC_PREFIX"
export MONO_ADDINS_REGISTRY="$INSTALLDIR/addinreg"
export PATH="$INSTALLDIR/bin:$PATH"
export MONO_INSTALL_PREFIX="$INSTALLDIR"

#mkdir -p "$INSTALLDIR"
#echo "test \"\$prefix\" = NONE && prefix=\"$INSTALLDIR\"" > $CONFIG_SITE

PS1="[$PROFNAME] \w @ "
''' % ( profname, dir )

print os.path.join (dir, profname)

with open(os.path.join (dir, profname), 'w') as f:
       f.write (envscript)
