import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from database import db_session
from models import UserModel


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    user_by_id = graphene.Field(User, id=graphene.Int(required=True))

    def resolve_user_by_id(self, info, id):
        return db_session.query(UserModel).get(id)


schema = graphene.Schema(query=Query)
