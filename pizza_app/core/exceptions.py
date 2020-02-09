class CoreException(Exception):
    def __init__(self, message: str, field: str = None):
        self.field = field
        self.message = message


class EntityNotFound(Exception):
    def __init__(self, entity: str, uid: str):
        self.entity = entity
        self.uid = uid


QUANTITY_MUST_BE_POSITIVE = "Quantity must be positive"
