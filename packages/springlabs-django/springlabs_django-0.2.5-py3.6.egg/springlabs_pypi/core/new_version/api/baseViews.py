# Django libraries
# 3rd party libraries
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
# Standard/core python libraries
# Our custom libraries
from core.utils import response_maker_1
from .serializers import *
from models_app.models import *

# Example viewset POST
# class UserAppViewSetPost(mixins.CreateModelMixin, viewsets.GenericViewSet):
#     serializer_class = UserAppSerializerPost
#
#     def create(self, request, *args, **kwargs):
#         """
#             Descripción de método create en documentación
#         """
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         response = response_maker_1(
#             "Message", serializer.data, status.HTTP_200_OK)
#         return Response(response)
#
# user_app_post = UserAppViewSetPost.as_view(
#     name="UsersApp",
#     description="Crear y listar Usuarios",
#     actions={
#         'post': 'create'
#     }
# )
