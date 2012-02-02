class IronLanguagesPackage(Package):
	def __init__(self):
		Package.__init__(self, 'iron', '2.11',
						 sources = ['git://github.com/mono/mono'],
						 configure_flags = ['--enable-nls=no',
											'--prefix=' + self.OSX_FRAMEWORK_PATH,
											],
						 source_dir_name = "mono-2.11.git"
						 )
