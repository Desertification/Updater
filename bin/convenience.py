# coding=utf-8
"""
Stores convenience functions
"""


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
