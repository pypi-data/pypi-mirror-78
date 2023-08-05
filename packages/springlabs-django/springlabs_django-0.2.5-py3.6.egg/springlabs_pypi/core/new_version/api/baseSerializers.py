# Django libraries
from django.contrib.auth.models import User
# 3rd party libraries
from rest_framework import serializers
# Standard/core python libraries
# Our custom libraries
from models_app.models import *


# Example serializers.Serializer
# class UserAppSerializerPost(serializers.Serializer):
#     email = serializers.EmailField(label="User's email",
#                                    help_text="A unique string value identifying User",
#                                    required=True,
#                                    max_length=100)
#     username = serializers.CharField(label="Username",
#                                      help_text="A unique string value identifying User",
#                                      required=True,
#                                      max_length=100)
#     def validate_email(self, value):
#         """
#             Breve descripción de método que valida campo email.
#
#             Descripción detallada de método que valida campo email, esta
#             descripción detallada puede llevar varias lineas.
#             Parámetros:
#                 param           [Type]          Descripción de param
#             Excepciones:
#                 Excepcion       [Type]          Descripción de excepción
#             Retorno:
#                 retorno        [Type]          Descripción de retorno
#         """
#         return value
#
#     def validate(self, validated_data):
#         """
#             Breve descripción de método validate.
#
#             Descripción detallada de método validate, esta
#             descripción detallada puede llevar varias lineas.
#             Parámetros:
#                 param           [Type]          Descripción de param
#             Excepciones:
#                 Excepcion       [Type]          Descripción de excepción
#             Retorno:
#                 retorno        [Type]          Descripción de retorno
#         """
#         return validated_data
#
#     def create(self, validated_data):
#         """
#             Breve descripción de método create.
#
#             Descripción detallada de método validate, esta
#             descripción detallada puede llevar varias lineas.
#             Parámetros:
#                 param           [Type]          Descripción de param
#             Excepciones:
#                 Excepcion       [Type]          Descripción de excepción
#             Retorno:
#                 retorno        [Type]          Descripción de retorno
#         """
#         return validated_data

# Example serializers.ModelSerializer
# class UserSerializerPost(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ("username",
#                   "email",
#                   )
#     def validate_email(self, value):
#         """
#             Breve descripción de método que valida campo email.
#
#             Descripción detallada de método que valida campo email, esta
#             descripción detallada puede llevar varias lineas.
#             Parámetros:
#                 param           [Type]          Descripción de param
#             Excepciones:
#                 Excepcion       [Type]          Descripción de excepción
#             Retorno:
#                 retorno        [Type]          Descripción de retorno
#         """
#         return value
#
#     def validate(self, validated_data):
#         """
#             Breve descripción de método validate.
#
#             Descripción detallada de método validate, esta
#             descripción detallada puede llevar varias lineas.
#             Parámetros:
#                 param           [Type]          Descripción de param
#             Excepciones:
#                 Excepcion       [Type]          Descripción de excepción
#             Retorno:
#                 retorno        [Type]          Descripción de retorno
#         """
#         return validated_data
#
#     def create(self, validated_data):
#         """
#             Breve descripción de método create.
#
#             Descripción detallada de método validate, esta
#             descripción detallada puede llevar varias lineas.
#             Parámetros:
#                 param           [Type]          Descripción de param
#             Excepciones:
#                 Excepcion       [Type]          Descripción de excepción
#             Retorno:
#                 retorno        [Type]          Descripción de retorno
#         """
#         return validated_data
