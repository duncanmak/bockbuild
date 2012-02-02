class MonoMasterPackage(Package):
	OSX_FRAMEWORK_PATH = "/Library/Frameworks/Mono.framework/Versions/2.11/"

	def __init__(self):
		Package.__init__(self, 'mono', '2.11',
										 sources = ['git://github.com/mono/mono'],
										 configure_flags = ['--enable-nls=no',
																				'--prefix=' + self.OSX_FRAMEWORK_PATH,
																				],
										 source_dir_name = "mono-2.11.git"
                     )
		if Package.profile.name == 'darwin':
			self.configure_flags.extend([
					# fix build on lion, it uses 64-bit host even with -m32
					'--build=i386-apple-darwin11.2.0',
					])
			self.sources.extend(['patches/pkg-config'])

		self.configure = './autogen.sh'
		self.makeinstall = 'make install DESTDIR="%{prefix}"'

	def install(self):
		Package.install(self)
		if Package.profile.name == 'darwin':
			self.fixup_pkgconfig ()
			self.sh('rsync -azP %{prefix}/Library/Frameworks/Mono.framework/Versions/2.11/* %{prefix}')
			self.sh('rm -rf %{prefix}/Library/')

	def fixup_pkgconfig(self):
		if not os.path.exists("%s/bin/pkg-config.bin" % self.prefix):
			self.sh('cp %{prefix}/bin/pkg-config %{prefix}/bin/pkg-config.bin')
			
		pkgconfig = os.path.join(self.package_dest_dir(), os.path.basename(self.sources[1]))
		temp = pkgconfig + ".tmp"

		with open(pkgconfig) as input:
			with open(temp, "w") as output:
				for line in input:
					output.write(re.sub('VERSION="REPLACE ME"', 'VERSION="2.11"', line))

		os.rename(temp, pkgconfig)
		self.sh('cp %s %s' % (pkgconfig, '%{prefix}/bin/pkg-config'))

MonoMasterPackage()
