import os
import sys

from django.core.management import execute_from_command_line

# try:
#     from dal.data_store import DataStore
# finally:
#     print("just to avoid replacement while reformat :)")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')


if __name__ == "__main__":  # on running python main.py
    # app.run(debug=True)
    # sys.argv.append('runserver')
    execute_from_command_line(sys.argv)
