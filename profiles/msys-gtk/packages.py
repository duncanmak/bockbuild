import os
from bockbuild.msysprofile import MSysProfile

class MSysGtkPackages:
	def __init__ (self):
		# Toolchain
		self.packages.extend ([
			'xz.py',
			'tar.py',
			'autoconf.py',
			'automake.py',
			'libtool.py',
			'gettext.py',
			'pkg-config.py'
		])

		# Base Libraries
		self.packages.extend ([
			'libpng.py',
			'libjpeg.py',
			'libtiff.py',
			'libxml2.py',
			'freetype.py',
			'fontconfig.py',
			'pixman.py',
			'cairo.py',
			'glib.py',
			'pango.py',
			'atk.py',
			'intltool.py',
			'gdk-pixbuf.py',
			'gtk+.py',
			'libglade.py',
		])

		# Theme
		self.packages.extend ([
			'librsvg.py',
			'hicolor-icon-theme.py',
			'gtk-engines.py',
			'murrine.py',
			'gtk-quartz-engine.py'
		])

		self.packages = [os.path.join ('..', '..', 'packages', p).replace ('\\', '/')
			for p in self.packages]
