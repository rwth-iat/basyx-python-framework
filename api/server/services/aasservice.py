from basyx import ObjectStore


class AasService:
    def __init__(self, global_object_store: ObjectStore):
        self.obj_store = global_object_store
