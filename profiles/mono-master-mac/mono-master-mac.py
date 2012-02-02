#!/usr/bin/python -B

import fileinput, glob, os, pprint, re, sys

sys.path.append ('../..')

from bockbuild.darwinprofile import DarwinProfile
from bockbuild.util import *
from packages import MonoMasterPackages

class MonoMasterProfile (DarwinProfile, MonoMasterPackages):
	def __init__ (self):
		DarwinProfile.__init__ (self)
		MonoMasterPackages.__init__ (self)
		
		self_dir = os.path.realpath (os.path.dirname (sys.argv[0]))
		aclocal_dir = os.path.join (self.prefix, "share", "aclocal")
		if not os.path.exists(aclocal_dir):
			os.makedirs (aclocal_dir)

		self.RELEASE_VERSION = "2.11" # REMEMBER TO UPDATE


	def install_root (self, subdir):
		return r"(/\w+)+/bockbuild/profiles/mono-master-mac/build-root/_install/%s/" % subdir

	def framework_path (self, subdir):
		return "/Library/Frameworks/Mono.framework/Versions/%s/%s/" % (self.RELEASE_VERSION, subdir)

	def relocate_pc_files (self):
		pkgconfig_dir = os.path.join (self.prefix, "lib", "pkgconfig")
		print pkgconfig_dir
		print "Processing .pc files"
		for pc in glob.glob ("%s/*.pc" % pkgconfig_dir):
			print os.path.basename (pc) + " ",
			for line in fileinput.input (os.path.join (pkgconfig_dir, pc), inplace = 1):
				if re.compile (r'^prefix=.*').match (line):
					print 'prefix=${pcfiledir}/../..'
				else:
					print line,
		print

	def is_type (self, file, type):
		result = backtick ("file " + file)[0]
		return result.find (type) > 0

	def relocate (self, subdir):
		for root, dirs, files in os.walk (os.path.join (self.prefix, subdir)):
			if re.search ("\.git", root): pass
			print "Relocating: %s" % root
			for file in files:
				f = os.path.join (root, file)
				if os.path.islink (f): pass
				if self.is_type (f, "Mach-O"):
					self.relocate_mach_o (f, file)
				elif self.is_type (f, "shell script"):
					self.relocate_shell_script (f)
			print

	def relocate_mach_o (self, file, name):
		print os.path.basename (file) + " ",
		run_shell ("install_name_tool -id %s %s" % (os.path.join (self.framework_path ("lib"), name), file))
		otool_output = backtick ("otool -L %s" % file)
		lib = r"((\w+)+/bockbuild/profiles/.*/build-root/_install/lib/(\S+\.dylib))"
		substitutions = []
		for output in otool_output:
			match = re.search (lib, output)
			if match:
				# root = self.framework_path ("lib")
				root = "@loader_path"
				substitutions.append ([match.group (1), os.path.join (root, match.group (3)), file])
				for old, new, file in substitutions:
					run_shell ("install_name_tool -change %s %s %s" % (old, new, file))

	def relocate_shell_script (self, file):
		print os.path.basename (file) + " ",
		for line in fileinput.input (file, inplace = 1):
			line = re.sub (self.install_root ("bin"), self.framework_path ("bin"), line)
			line = re.sub (self.install_root ("lib"), self.framework_path ("lib"), line)
			print line,

	def remove_files (self, subdir = "lib", prefix = "*"):
		dir = os.path.join (self.prefix, subdir)
		print "Removing la files in " + dir
		for la in backtick ('find %s -name "%s"' % (dir, prefix)):
			os.remove (la)

	def include_libgdiplus (self):
		config = os.path.join (self.prefix, "etc", "mono", "config")
		temp = config + ".tmp"
		lib = self.framework_path("lib")
		with open(config) as c:
			with open(temp, "w") as output:
				for line in c:
					if re.search(r'</configuration>', line):
						# Insert libgdiplus entries before the end of the file
						output.write('\t<dllmap dll="gdiplus" target="%slibgdiplus.dylib" />\n' % lib)
						output.write('\t<dllmap dll="gdiplus.dll" target="%slibgdiplus.dylib" />\n' % lib)
					output.write(line)

		os.rename(temp, config)

	def make_package_symlinks(self):

		base = os.path.join(self.prefix, "Library", "Frameworks", "Mono.framework", "Versions", "Current")
		print "path %s" % base
		# os.mkdir(path)
		os.symlink (os.path.join (self.prefix, "bin"),     os.path.join (base, "Commands"))
		os.symlink (os.path.join (self.prefix, "include"), os.path.join (base, "Headers"))
		os.symlink (os.path.join (self.prefix, "lib"),     os.path.join (base, "Libraries"))
		os.symlink (os.path.join (base, "Current"),        os.path.join (base, "Home"))
		os.symlink (os.path.join (self.prefix, "lib", "libmono-2.0.dylib"), os.path.join (base, "Mono"))

	def prepare_package_layout (self):
		self.make_package_symlinks()

	def run_package_maker (pkg = 'pkg', pkg_root = 'pkg_root', resources_dir = 'resources_dir',
												 info_plist = 'info.plist', description_plist = 'description.plist'):x
		packagemaker = '/Developer/Applications/Utilities/PackageMaker.app/Contents/MacOS/PackageMaker'
		cmd = ' '.join([packagemaker, '-build', '-p', pkg, '-f', pkg_root, '-r', resources_dir, '-i', info_plist, '-d', description_plist])
		print cmd
		# self.run_shell (cmd)

	def build_package (self):
		self.prepare_package_layout ()
		self.run_package_maker ()

	# THIS IS THE MAIN METHOD FOR MAKING A PACKAGE
	def package (self):
		self.remove_files (prefix = '*.la')
		self.remove_files (prefix = '*.a')
		self.relocate_pc_files ()
		self.relocate ("bin")
		self.relocate ("lib")
		self.include_libgdiplus ()
		self.build_package ()

MonoMasterProfile ().build ()

profname = "mono-master-mac-env"
dir = os.path.realpath (os.path.dirname (sys.argv[0]))
envscript = '''#!/bin/sh
PROFNAME="%s"
INSTALLDIR=%s/build-root/_install
export DYLD_FALLBACK_LIBRARY_PATH="$INSTALLDIR/lib:/lib:/usr/lib:$DYLD_FALLBACK_LIBRARY_PATH"
export C_INCLUDE_PATH="$INSTALLDIR/include:$C_INCLUDE_PATH"
export ACLOCAL_PATH="$INSTALLDIR/share/aclocal:$ACLOCAL_PATH"
export ACLOCAL_FLAGS="-I $INSTALLDIR/share/aclocal $ACLOCAL_FLAGS"
export PKG_CONFIG_PATH="$INSTALLDIR/lib/pkgconfig:$INSTALLDIR/lib64/pkgconfig:$INSTALLDIR/share/pkgconfig:$PKG_CONFIG_PATH"
export CONFIG_SITE="$INSTALLDIR/$PROFNAME-config.site"
export MONO_GAC_PREFIX="$INSTALLDIR:MONO_GAC_PREFIX"
export MONO_ADDINS_REGISTRY="$INSTALLDIR/addinreg"
export PATH="$INSTALLDIR/bin:$PATH"
export MONO_INSTALL_PREFIX="$INSTALLDIR"

#mkdir -p "$INSTALLDIR"
#echo "test \"\$prefix\" = NONE && prefix=\"$INSTALLDIR\"" > $CONFIG_SITE

PS1="[$PROFNAME] \w @ "
''' % ( profname, dir )

with open(os.path.join (dir, profname), 'w') as f:
	f.write (envscript)
