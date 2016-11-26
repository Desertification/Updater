import os.path
import sys
import time
import urllib

from PySide.QtGui import QApplication

from bin.main_window_controller import MainWindowController

__version__ = "0.1.0"
__author__ = "maxim"
__description__ = "Minecraft mod list updater"
__name___ = "MMLU"

if __name__ == '__main__':
	# gui test
	q_application = QApplication(sys.argv)
	controller = MainWindowController()
	q_application.exec_()

if __name__ == "__main__sdfsf":
	addedfiles = []
	deletedfiles = []

	print "versie:" + __version__

	host = "http://141.134.182.253:8080/"

	longdir = os.getenv('APPDATA') + "/.minecraft/"

	dirname = "mods/"
	confname = "config/"

	if os.path.exists(longdir):
		dirname = longdir + "mods/"
		confname = longdir + "config/"

	if not os.path.exists(dirname):
		print "Minecraft niet gevonden/(plaats file in .Minecraft)"

	elif not os.path.exists(confname + "forge.cfg"):
		print "Forge niet geinstaleerd/start minecraft na installatie Forge"

	else:

		modshost = host + ""

		try:
			response = urllib.urlopen(modshost + 'index.php')
			html = response.read()
		except IOError as e:
			html = ""
			print(e.args[1])

		serverfiles = []
		# todo thread this
		for each_line in html.splitlines():

			filename = each_line
			serverfiles.append(filename)
			print "zoek: " + filename
			if not os.path.exists(dirname + filename):
				print "download: " + filename
				addedfiles.append("\t+ " + filename)
				dlink = filename.replace(" ", "%20")
				urllib.urlretrieve(modshost + dlink, dirname + filename)
				time.sleep(0.1)

			else:
				print "gevonden: " + filename

		locdoc = os.listdir(dirname)

		for x in locdoc:
			# fixme removes all the mods when no connection to the server could be made
			if not any(l == x for l in serverfiles):
				if os.path.exists(dirname + x):
					if not os.path.isdir(dirname + x):
						if not x[:1] == ".":
							print "verwijder: " + x
							os.remove(dirname + x)
							deletedfiles.append("\t- " + x)

	if addedfiles or deletedfiles:
		print "---------------------------------------------"

		for af in addedfiles:
			print af
		for df in deletedfiles:
			print df

		print "---------------------------------------------"

	print
	name = raw_input('druk enter voor door te gaan')
