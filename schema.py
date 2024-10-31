import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from datetime import datetime, date
from database import db_session
from models import UserModel, SubjectModel, AddressModel


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

    def resolve_subjects_by_user(self, info, user_id):
        user = db_session.query(UserModel).get(user_id)
        if user:
            return user.subjects
        else:
            return []

    def resolve_users_by_age(self, info, age):
        today = date.today()
        birth_date = date(today.year - age, today.month, today.day)
        return db_session.query(UserModel).filter(
            UserModel.birth_date == birth_date
        ).all()

    def resolve_users_by_age_range(self, info, min_age=None, max_age=None):
        today = date.today()
        query = db_session.query(UserModel)
        if min_age is not None:
            max_birth_date = date(today.year - min_age, today.month, today.day)
            query = query.filter(UserModel.birth_date <= max_birth_date)
        if max_age is not None:
            min_birth_date = date(today.year - max_age, today.month, today.day)
            query = query.filter(UserModel.birth_date >= min_birth_date)
        return query.all()

    def resolve_users_by_birth_date(self, info, birth_date):
        try:
            birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date()
        except ValueError:
            return []
        return db_session.query(UserModel).filter(
            UserModel.birth_date == birth_date_obj
        ).all()

    def resolve_users_by_country(self, info, country):
        return db_session.query(UserModel).join(
            UserModel.address
        ).filter(
            AddressModel.country == country
        ).all()



# Mutations

class AddAddress(graphene.Mutation):
    class Arguments:
        street = graphene.String(required=True)
        city = graphene.String(required=True)
        country = graphene.String(required=True)

    address = graphene.Field(lambda: AddressModel)

    def mutate(self, info, street, city, country):
        new_address = AddressModel(street=street, city=city, country=country)
        db_session.add(new_address)
        db_session.commit()
        return AddAddress(address=new_address)


class AddUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        birth_date = graphene.String(required=True)  # Format: 'YYYY-MM-DD'
        address_id = graphene.Int(required=False)

    user = graphene.Field(lambda: User)

    def mutate(self, info, name, birth_date, address_id=None):
        try:
            birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date()
        except ValueError:
            raise Exception("Invalid birth date format. Expected 'YYYY-MM-DD'")
        new_user = UserModel(name=name, birth_date=birth_date_obj, address_id=address_id)
        db_session.add(new_user)
        db_session.commit()
        return AddUser(user=new_user)


class UpdateUserName(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        new_name = graphene.String(required=True)

    user = graphene.Field(lambda: User)

    def mutate(self, info, user_id, new_name):
        user = db_session.query(UserModel).get(user_id)
        if not user:
            raise Exception("User not found")
        user.name = new_name
        db_session.commit()
        return UpdateUserName(user=user)


class DeleteAddress(graphene.Mutation):
    class Arguments:
        address_id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, address_id):
        address = db_session.query(AddressModel).get(address_id)
        if not address:
            return DeleteAddress(ok=False)
        db_session.delete(address)
        db_session.commit()
        return DeleteAddress(ok=True)


class DeleteSubject(graphene.Mutation):
    class Arguments:
        subject_id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, subject_id):
        subject = db_session.query(SubjectModel).get(subject_id)
        if not subject:
            return DeleteSubject(ok=False)
        db_session.delete(subject)
        db_session.commit()
        return DeleteSubject(ok=True)


class DeleteUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, user_id):
        user = db_session.query(UserModel).get(user_id)
        if not user:
            return DeleteUser(ok=False)
        db_session.delete(user)
        db_session.commit()
        return DeleteUser(ok=True)


class Mutation(graphene.ObjectType):
    add_address = AddAddress.Field()
    add_user = AddUser.Field()
    update_user_name = UpdateUserName.Field()
    delete_address = DeleteAddress.Field()
    delete_subject = DeleteSubject.Field()
    delete_user = DeleteUser.Field()



schema = graphene.Schema(query=Query)
