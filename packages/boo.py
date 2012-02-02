class BooPackage (Package):
	def __init__(self):
		Package.__init__ (self, 'boo', '0.9.4.9')
		self.sources = ['http://dist.codehaus.org/boo/distributions/boo-0.9.4.9.tar.gz']

BooPackage ()
