"""
sets up a configuration
"""


def make_config(location):
    with open(location, 'w') as settings:
        settings.writelines(input("please input your settings: "))
