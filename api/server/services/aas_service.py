from sdk.basyx import ObjectStore


class aas_service:
    def __init__(self, global_object_store: ObjectStore):
        self.obj_store = global_object_store
