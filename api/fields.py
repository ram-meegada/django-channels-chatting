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
# from api.models import ChatStorageWithSessionIdModel
# from views import APIView
# from api.serializers import ChatSerializer
# from rest_framework import status


# class CollectionView(APIView):
#     def get_all_data_list(self, request, session_id,format=None):
#         all_data_obj=ChatStorageWithSessionIdModel.objects.filter(user=request.user.id, session = session_id)
#         serialized = ChatSerializer(all_data_obj, many = True)
#         return {"data": serialized.data, "message":"data fetch sucessfully","code":status.HTTP_200_OK}

# class NonCollectionView(APIView):
#     def get_all_non_data(self, request, user_id,session_id,format=None):
#         all_non_data_obj=ChatStorageWithSessionIdModel.objects.get(user=user_id, session=session_id)
