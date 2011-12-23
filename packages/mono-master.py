class MonoMasterPackage(Package):
	def __init__(self):
		Package.__init__(self, 'mono', '2.11',
                     sources = ['git://github.com/mono/mono'],
                     configure_flags = ['--enable-nls=no',
                                        ]
                     )
		if Package.profile.name == 'darwin':
			self.configure_flags.extend([
          # fix build on lion, it uses 64-bit host even with -m32
          '--build=i386-apple-darwin11.2.0',
          ])

		self.configure = './autogen.sh --prefix="%{prefix}"'
    
		# Mono(in libgc) likes to fail to build randomly
		self.make = 'make'

#	def prep(self):
#		Package.prep(self)
#		self.sh('patch -p1 < "%{sources[1]}"')

	def install(self):
		Package.install(self)
		if Package.profile.name == 'darwin':
			self.sh('sed -ie "s/libcairo.so.2/libcairo.2.dylib/" "%{prefix}/etc/mono/config"')

MonoMasterPackage()
