"""
set up a configuration
"""


def makeConfig(location):
    with open(location, 'w') as settings:
        settings.writelines(raw_input("please input your settings: "))
