
class UORMException(Exception):
    pass


class AbortTransaction(UORMException):
    def __init__(self):
        super(AbortTransaction, self).__init__("transaction aborted")


class InvalidShardId(UORMException):
    def __init__(self, shard_id):
        super(InvalidShardId, self).__init__(f"invalid shard_id \"{shard_id}\"")


class ConfigurationError(UORMException):
    pass


class ValidationError(UORMException):
    pass


class DoNotSave(UORMException):
    pass


class ObjectSaveRequired(UORMException):
    pass


class ModelDestroyed(UORMException):
    pass


class MissingShardId(UORMException):
    pass


class IntegrityError(UORMException):
    pass


class MissingSubmodel(UORMException):
    pass


class WrongSubmodel(UORMException):
    pass


class UnknownSubmodel(UORMException):
    pass
