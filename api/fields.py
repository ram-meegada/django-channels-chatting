# from django.db import models
# from django.db.models import ForeignKey

# class ExternalDatabaseForeignKey(ForeignKey):
#     def __init__(self, to, on_delete, db_name, *args, **kwargs):
#         super().__init__(to, on_delete, *args, **kwargs)
#         self.db_name = db_name

#     def deconstruct(self):
#         name, path, args, kwargs = super().deconstruct()
#         kwargs['db_name'] = self.db_name
#         return name, path, args, kwargs
