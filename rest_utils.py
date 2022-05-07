from django.db import models


def to_json(obj):
    if isinstance(obj, list):
        if len(obj) > 0:
            if isinstance(obj[0], models.Model):
                res = [o.__dict__ for o in obj]
                # there is no '_sa_instance_state' for __abstract__
                if '_state' in res[0]:
                    [r.pop('_state', None) for r in res]
            else:
                res = obj
        else:
            res = obj
    elif isinstance(obj, models.Model):
        # https://stackoverflow.com/questions/1958219/how-to-convert-sqlalchemy-row-object-to-a-python-dict
        res = dict(obj.__dict__)
        res.pop('_state', None)
    else:
        if isinstance(obj, dict):
            res = obj
        else:
            res = obj.__dict__
    return res
