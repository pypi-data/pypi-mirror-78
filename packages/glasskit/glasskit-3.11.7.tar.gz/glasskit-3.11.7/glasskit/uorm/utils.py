from functools import wraps
from bson.objectid import ObjectId, InvalidId
from .errors import ObjectSaveRequired


def resolve_id(id_):
    # ObjectId(None) apparently generates a new unique object id
    # which is not a behaviour we need
    if id_ is not None:
        try:
            objid_expr = ObjectId(id_)
            if str(objid_expr) == id_:
                id_ = objid_expr
        except (InvalidId, TypeError):
            pass
    return id_


def save_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        this = args[0]
        if this.is_new:
            raise ObjectSaveRequired("This object must be saved first")
        return func(*args, **kwargs)

    return wrapper


def pick_rw_shard():
    from .db import db
    from random import choice

    return choice(db.rw_shards)
