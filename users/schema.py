import graphene
from graphene_django import DjangoObjectType
from oauth2_provider.models import AccessToken
from .models import ExtendUser
from graphql_jwt.decorators import login_required
from authentication.models import UserManagement


class ExtendUserType(DjangoObjectType):
    class Meta:
        model = ExtendUser
        fields = ("email", "username", "first_name", "last_name", "user_id")


class Query(graphene.ObjectType):
    all_users = graphene.List(ExtendUserType)
    logged_in_user = graphene.Field(ExtendUserType)
    
    def resolve_all_users(root, info):
        return ExtendUser.objects.all()
    
    @login_required
    def resolve_logged_in_user(root, info):
        auth_user = UserManagement.objects.get(email=info.context.user.email)
        user = ExtendUser.objects.get(user_id=auth_user.user_id)
        if not user:
            raise Exception('User not found.')
        return user
    

class CreateUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String()
        last_name = graphene.String()

    user = graphene.Field(ExtendUserType)

    ok = graphene.Boolean()
    error = graphene.String()

    @classmethod
    def mutate(self, root, info, email, username, password, first_name, last_name):
        user_management = UserManagement(email=email, user_type='user')
        user_management.set_password(password)
        user_management.save()
        try:
            ExtendUser.objects.get(email=email)
            return CreateUser(ok=False, error="User already exists")
        except ExtendUser.DoesNotExist:
            try:
                user = ExtendUser(user_id=user_management, email=email, username=username, first_name=first_name, last_name=last_name)
                user.save()
                return CreateUser(ok=True, user=user)
            except Exception as e:
                print(e)
                return CreateUser(ok=False, error="Can't create user")


class UpdateUser(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        username = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()

    user = graphene.Field(ExtendUserType)
    ok = graphene.Boolean()
    error = graphene.String()

    @classmethod
    @login_required
    def mutate(cls, root, info, email=None, username=None, first_name=None, last_name=None):
        auth_user = UserManagement.objects.get(email=info.context.user.email)
        user = ExtendUser.objects.get(user_id=auth_user.user_id)
        if email and email != user.email:
            try:
                ExtendUser.objects.get(email=email)
                return UpdateUser(ok=False, error="That email is already taken")
            except ExtendUser.DoesNotExist:
                user.email = email
                auth_user.email = email
        if username:
            user.username = username
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        try:
            user.save()
            auth_user.save()
            return UpdateUser(ok=True, user=user)
        except Exception as e:
            return UpdateUser(ok=False, error=str(e))
    

class DeleteUser(graphene.Mutation):
    ok = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info):
        auth_user = UserManagement.objects.get(email=info.context.user.email)
        auth_user.delete()
        return DeleteUser(ok=True)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
