# coding=utf-8
"""
Stores convenience functions
"""
import os
import re
import socket
import sys

from ipaddr import IPv6Address, AddressValueError


def find_substrings_in_list(substring, list):
	"""
	Search a list for substrings

	:param substring: substring to search for
	:type substring: basestring
	:param list: list containing strings
	:type list: list
	:return: List containing all the found substrings
	:rtype: list
	"""
	return [result for result in list if substring in result]


def is_frozen():
	"""
	Returns if the application is frozen or not

	:return: frozen?
	:rtype: bool
	"""
	return hasattr(sys, "frozen")


def module_path():
	""" This will get us the program's directory,
	even if we are frozen using py2exe"""

	if is_frozen():
		return os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))

	return os.path.dirname(unicode(__file__, sys.getfilesystemencoding()))


def is_valid_ipv4(ip):
	"""
	Tests if an ip address string is a valid ip address

	:param ip: ip address
	:type ip: basestring
	:return: valid or not
	:rtype: bool
	"""
	try:
		socket.inet_aton(ip)
		return True
	except socket.error:
		return False


def is_valid_ipv6(ip):
	"""
	Tests if an ip address string is a valid ipv6 address

	:param ip: ipv6 address string
	:type ip: basestring
	:return: valid or not
	:rtype: bool
	"""
	try:
		IPv6Address(ip)
		return True
	except AddressValueError:
		return False


def is_valid_hostname(hostname):
	"""
	http://stackoverflow.com/a/33214423
	validates the fqdn hostname

	:param hostname:
	:return:
	"""
	if hostname[-1] == ".":
		# strip exactly one dot from the right, if present
		hostname = hostname[:-1]
	if len(hostname) > 253:
		return False
	# must be not all-numeric, so that it can't be confused with an ip-address
	if re.match(r"[\d.]+$", hostname):
		return False

	allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
	return all(allowed.match(x) for x in hostname.split("."))


def is_valid_port(port):
	"""
	Test if the port is in a valid range

	:param port: port number
	:type port: int
	:return: valid or not
	:rtype: bool
	"""
	return 0 <= port < 65536
