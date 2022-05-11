import os
import sys

# try:
#     from dal.data_store import DataStore
# finally:
#     print("just to avoid replacement while reformat :)")

import django.db
from django.apps import AppConfig


class MyDjangoAppConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    default_auto_field = 'django.db.models.AutoField'
    name = 'dal'  # python package containing generated django models


# there should be "settings.py" in the project root
# Google --> django settings.py location
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

# django.setup() should be called before importing/using generated django models -->
# AppRegistryNotReady("Apps aren't loaded yet.")
django.setup()

from django.core.management import execute_from_command_line

ds = DataStore()  # in fact, it is used only for generated DAO

if __name__ == "__main__":  # on running python main.py
    # app.run(debug=True)
    # sys.argv.append('runserver')
    execute_from_command_line(sys.argv)
