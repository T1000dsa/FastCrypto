from collections import namedtuple

from src.core.config.settings import settings

# Define the menu item structure
MenuItem = namedtuple('MenuItem', ['title', 'url'])

# Create menu items with additional parameters

prefix = settings.prefix.api_data.prefix
menu_items = [
    MenuItem('Home', '/'),
    MenuItem('Docs', '/docs'),

    MenuItem('Registration',  prefix + '/register'),
    MenuItem('Login',  prefix + '/login'),
    MenuItem('Logout',  prefix + '/logout'),
]

def get_menu():
    return [item for item in menu_items]


def choice_from_menu(name:str=None):
    if name:
        for i in menu_items:
            if name.lower() == i.title.lower() or name.lower() == i.url.lower():
                return i