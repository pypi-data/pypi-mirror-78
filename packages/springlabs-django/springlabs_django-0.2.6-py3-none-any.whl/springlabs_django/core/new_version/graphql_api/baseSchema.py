# Django libraries
from django.contrib.auth.models import User
from django.db.models import Q
# 3rd Party libraries
import graphene
from graphql_jwt.decorators import login_required, user_passes_test, staff_member_required

# Standard/core python libraries
# Our custom libraries
from models_app.models import UserApp
from .types import ExampleDjangoType
# EXAMPLE QUERY GRAPHENE (Managed by SPRINGLABS_DJANGO)


class ExampleDjangoQueries(object):
    # FIELDS
    users = graphene.List(
        ExampleDjangoType,
        client=graphene.Argument(graphene.ID, required=True),
        role=graphene.Argument(graphene.String, required=False),
        agent=graphene.Argument(graphene.ID, required=False),
        description='Obtain all users.'
    )
    user = graphene.Field(
        ExampleDjangoType,
        id=graphene.Argument(graphene.ID, required=True),
        description='Lookup a user by ID or pk.'
    )

    # RESOLVES
    @login_required
    @user_passes_test(lambda user: user.is_staff or len(user.groups.filter(name='Administrador')) > 0)
    def resolve_users(self, info, **kwargs):
        users = UserApp.objects.filter(client=kwargs['client'])
        result = []
        for user in users:
            objUser = {
                "id_user": user.user.pk,
                "username": user.user.username,
                "email": user.user.email,
                "first_name": user.user.first_name,
                "last_name": user.last_name
            }
            result.append(objUser)
        return result

    @login_required
    @user_passes_test(lambda user: user.is_staff or len(user.groups.filter(name='Administrador')) > 0)
    def resolve_user(self, info, **kwargs):
        if UserApp.objects.filter(pk=kwargs['id']).exists():
            objUserApp = UserApp.objects.get(pk=kwargs['id'])
            objUser = {
                "id_user": objUserApp.user.pk,
                "username": objUserApp.user.username,
                "email": objUserApp.user.email,
                "first_name": objUserApp.user.first_name,
                "last_name": objUserApp.last_name
            }
            return objUser
# END EXAMPLE QUERY GRAPHENE (Managed by SPRINGLABS_DJANGO)
