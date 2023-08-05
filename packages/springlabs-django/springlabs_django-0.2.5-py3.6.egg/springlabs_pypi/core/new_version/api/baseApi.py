# Django libraries
# 3rd Party libraries
import graphene
# Standard/core python libraries
# Our custom libraries
from .users.schema import UserQueries

# QUERY EXPOSE TO SCHEMA GRPAHENE


class Query(UserQueries, graphene.ObjectType):
    pass


# SCHEMA
schema = graphene.Schema(query=Query, auto_camelcase=False)
