import os
import shutil
from plistlib import Plist
from util import *
from unixprofile import UnixProfile

class MSysProfile (UnixProfile):
	def __init__ (self):
		UnixProfile.__init__ (self)
		
		self.name = 'msys'
		self.build_root = os.path.join (os.getcwd ().replace('c:\\', '/c/').replace ('\\', '/'), 'build-root')
		self.prefix = os.path.join (self.build_root, '_install').replace ('\\', '/')

		self.gcc_arch_flags = [ '-mms-bitfields', '-march=i686' ]
		
		self.gcc_flags.extend (self.gcc_arch_flags)
		self.ld_flags.extend (self.gcc_arch_flags)
		
		self.env.set ('CC',  'gcc')
		self.env.set ('CXX', 'g++')

		self.env.set ('BUILD_PREFIX', self.prefix)


