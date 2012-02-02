class XspPackage (Package):
	def __init__(self):
		Package.__init__ (self, 'xsp', '2.10.2')
		self.sources = ['http://ftp.novell.com/pub/mono/sources/xsp/xsp-2.10.2.tar.bz2']

XspPackage ()
