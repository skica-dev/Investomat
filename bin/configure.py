"""
sets up a configuration file for the main module
"""


def make_config(location):
    with open(location, 'w') as settings:
        settings.writelines(input("please input your settings: "))
