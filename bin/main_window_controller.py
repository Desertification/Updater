# coding=utf-8

"""
Class controlling the main window of the application
"""

from PySide.QtCore import QFile
from PySide.QtCore import QObject
from PySide.QtGui import QComboBox
from PySide.QtGui import QLabel
from PySide.QtGui import QLineEdit
from PySide.QtGui import QProgressBar
from PySide.QtGui import QPushButton
from PySide.QtGui import QWidget
from PySide.QtUiTools import QUiLoader

from bin.convenience import is_valid_ipv4


class AddressType(object):
	"""
	Enum for address types in combobox
	"""
	Hostname = 0
	IPv4 = 1
	IPv6 = 2


class MainWindowController(QObject):
	"""
	Controller for the main window
	"""

	def __init__(self, *args, **kwargs):
		super(MainWindowController, self).__init__(*args, **kwargs)

		# vars
		self._address_valid = False

		# define ui members for type hinting
		self._ip_line_edit = self._window.IpAddressLineEdit  # type: QLineEdit
		self._status_label = self._window.Statuslabel  # type: QLabel
		self._update_button = self._window.UpdateButton  # type: QPushButton
		self._update_button = self._window.UpdateButton  # type: QPushButton
		self._progress_bar = self._window.progressBar  # type: QProgressBar
		self._combobox = self._window.comboBox  # type: QComboBox

		# load ui
		loader = QUiLoader()
		ui = QFile("ui/main_window.ui")
		ui.open(QFile.ReadOnly)
		self._window = loader.load(ui)  # type: QWidget
		ui.close()
		self._window.show()

		# init other elements
		self._init_ip_line_edit()

	def _init_ip_line_edit(self):
		"""
		configure and apply line edit logic
		"""
		self._ip_line_edit.setInputMask("000.000.000.000:00000")  # force input mask

		# apply validator
		self._ip_line_edit.textChanged.connect(self._ip_line_edit_textChanged)
		self._ip_line_edit.textChanged.emit(self._ip_line_edit.text())  # force first validation

	def _init_combobox(self):
		self._combobox.currentIndexChanged.connect(self._combobox_index_changed)

	def _combobox_index_changed(self, index):
		pass  # todo change line edit mask

	@property
	def address(self):
		"""
		:rtype: str
		"""
		return self._ip_line_edit.text()

	@address.setter
	def address(self, address):
		"""
		:param address: ip address
		:type address: str
		"""
		self._ip_line_edit.text(address)

	def _ip_line_edit_textChanged(self, text):
		"""
		Applies a visual to the ip address line edit if the user input is correct or not

		:param text: text to validate
		:type text: str
		"""
		# get ip and port form text
		split = text.split(":")
		ip = split[0]  # type: str
		try:
			port = int(split[1])  # type: str
		except ValueError:
			port = None

		# test validity of port and ip
		valid_ipv4 = is_valid_ipv4(ip)
		valid_port = False
		if not port or (port < 65536):
			valid_port = True

		# apply style sheet
		if valid_ipv4 and valid_port:
			self._ip_line_edit.setStyleSheet("")
			self._address_valid = True
		else:
			self._ip_line_edit.setStyleSheet("border: 1px solid red")
			self._address_valid = False

	def _test_connection(self):  # todo turn this into a worker object
		pass
