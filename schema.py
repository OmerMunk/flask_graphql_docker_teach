import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from database import db_session
from models import UserModel, SubjectModel


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (graphene.relay.Node,)


class Subject(SQLAlchemyObjectType):
    class Meta:
        model = SubjectModel
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    user_by_id = graphene.Field(User, id=graphene.Int(required=True))
    users_by_name = graphene.List(User, name_substring=graphene.String(required=True))
    subjects_by_name = graphene.List(Subject, name_substring=graphene.String(required=True))
    users_by_subject = graphene.List(User, subject_id=graphene.Int(required=True))

    subjects_by_user = graphene.List(Subject, user_id=graphene.Int(required=True))
    users_by_age = graphene.List(User, age=graphene.Int(required=True))
    users_by_age_range = graphene.List(User, min_age=graphene.Int(required=True), max_age=graphene.Int(required=True))
    users_by_birth_date = graphene.List(User, birth_date=graphene.String(required=True))
    users_by_country = graphene.List(User, country=graphene.String(required=True))

    def resolve_user_by_id(self, info, id):
        return db_session.query(UserModel).get(id)

    def resolve_users_by_name(self, info, name_substring):
        substring = f"%{name_substring}%"
        return db_session.query(UserModel).filter(
            UserModel.name.ilike(substring)
        ).all()

    def resolve_subjects_by_name(self, info, name_substring):
        substring = f"%{name_substring}%"
        return db_session.query(SubjectModel).filter(
            SubjectModel.name.ilike(substring)
        ).all()

    def resolve_users_by_subject(self, info, subject_id):
        return db_session.query(UserModel).join(
            UserModel.subjects
        ).filter(
            SubjectModel.id == subject_id
        ).all()



schema = graphene.Schema(query=Query)
