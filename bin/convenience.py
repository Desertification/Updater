# coding=utf-8
"""
Stores convenience functions
"""
import os
import socket
import sys


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
