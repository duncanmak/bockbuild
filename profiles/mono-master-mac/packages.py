import os
from bockbuild.darwinprofile import DarwinProfile

class MonoMasterPackages:
	def __init__(self):

		# Toolchain
		self.packages.extend([
				# 'autoconf.py',
				# 'automake.py',
				# 'libtool.py', 
				'gettext.py',
				'pkg-config.py'
				])

    # Mono
		self.packages.extend([
				'mono-master.py',
				# 'libgdiplus.py',
				# 'gtk-sharp.py',
				# 'mono-addins.py',
				])

		# # Base Libraries
		self.packages.extend([
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

		# # Theme
		self.packages.extend([
				'librsvg.py',
				'hicolor-icon-theme.py',
				'gtk-engines.py',
				'gtk-quartz-engine.py'
				])

		self.packages = [os.path.join('..', '..', 'packages', p) for p in self.packages]
