class DatabaseRouter:
    """
    Route Activity model to MongoDB.
    Everything else goes to PostgreSQL.
    """

    route_app_labels = {
        "activities",
    }

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "mongodb"

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "mongodb"

        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._state.db == "mongodb" or obj2._state.db == "mongodb":
            return False
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == "mongodb"

        if db == "mongodb":
            return False

        return db == "default"
