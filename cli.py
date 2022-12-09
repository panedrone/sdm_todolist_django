import os

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from dal.data_store import create_ds
from dal.group import Group


if __name__ == "__main__":  # on running python main.py

    _ds = create_ds()

    _ds.begin()

    gr = Group(g_name="g1")
    _ds.create_one(gr)
    gr = Group(g_name="g2")
    _ds.create_one(gr)
    gr = Group(g_name="g3")
    _ds.create_one(gr)

    _ds.commit()

    print("Done")
