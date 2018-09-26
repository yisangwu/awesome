
"""
https://docs.djangoproject.com/zh-hans/2.1/topics/db/multi-db/
"""


class MultiMysqlRouter:
    """
    A router to control all database operations on models in the
    auth application.
    """
    APP_LABEL = None
    DB_NAME = None

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to db.
        """
        if model._meta.app_label == self.APP_LABEL:
            return self.DB_NAME
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to db.
        """
        if model._meta.app_label == self.APP_LABEL:
            return self.DB_NAME
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == self.APP_LABEL or obj2._meta.app_label == self.APP_LABEL:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the db
        database.
        """
        if db == self.DB_NAME:
            return app_label == self.APP_LABEL
        elif app_label == self.APP_LABEL:
            return False
        return None
