import sys

try:
    from dal.data_store import DataStore
finally:
    print("just to avoid replacement while reformat :)")

from django.core.management import execute_from_command_line

ds = DataStore()  # it is used only for generated DAO

if __name__ == "__main__":  # on running python main.py
    # app.run(debug=True)
    # sys.argv.append('runserver')
    execute_from_command_line(sys.argv)
