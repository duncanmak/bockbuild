class NantPackage (Package):
	def __init__(self):
		Package.__init__(self, 'nant', '0.91')
		self.sources = ['http://sourceforge.net/projects/nant/files/nant/0.91/nant-0.91-src.tar.gz']

NantPackage ()
