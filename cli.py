import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from dal.data_store import create_ds
from dal.project import Project

if __name__ == "__main__":  # on running python main.py

    _ds = create_ds()

    _ds.begin()

    p = Project(p_name="p1")
    _ds.create_one(p)
    p = Project(p_name="p2")
    _ds.create_one(p)
    p = Project(p_name="p3")
    _ds.create_one(p)

    _ds.commit()

    print("Done")
