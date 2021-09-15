import os, shutil
def make_archive(source, destination):
	base = os.path.basename(destination)
	name = ".".join(base.split('.')[0:-1])
	format = base.split('.')[-1]
	archive_from = os.path.dirname(source)
	archive_to = os.path.basename(source.strip(os.sep))
	shutil.make_archive(name, format, archive_from, archive_to)
	shutil.move('%s.%s'%(name,format), destination)

debug = True

def log(string):
	if debug:
		print(string)