import graphene
from graphene_django import DjangoObjectType
from oauth2_provider.models import AccessToken
from .models import ExtendUser
from graphql_jwt.decorators import login_required
<<<<<<< HEAD
=======
from authentication.models import UserManagement
>>>>>>> 415bee1 (Add oauth, users, merchants, products along with CRUD operations)


class ExtendUserType(DjangoObjectType):
    class Meta:
        model = ExtendUser
<<<<<<< HEAD
        exclude = ('password', )
=======
        fields = ("email", "username", "first_name", "last_name", "user_id")
>>>>>>> 415bee1 (Add oauth, users, merchants, products along with CRUD operations)


class Query(graphene.ObjectType):
    all_users = graphene.List(ExtendUserType)
    logged_in_user = graphene.Field(ExtendUserType)
    
    def resolve_all_users(root, info):
        return ExtendUser.objects.all()
    
    @login_required
    def resolve_logged_in_user(root, info):
<<<<<<< HEAD
        return info.context.user
=======
        auth_user = UserManagement.objects.get(email=info.context.user.email)
        user = ExtendUser.objects.get(user_id=auth_user.user_id)
        if not user:
            raise Exception('User not found.')
        return user
>>>>>>> 415bee1 (Add oauth, users, merchants, products along with CRUD operations)
    

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
<<<<<<< HEAD
    def mutate(self, root, info, email, username, password, first_name=None, last_name=None):
=======
    def mutate(self, root, info, email, username, password, first_name, last_name):
        user_management = UserManagement(email=email, user_type='user')
        user_management.set_password(password)
        user_management.save()
>>>>>>> 415bee1 (Add oauth, users, merchants, products along with CRUD operations)
        try:
            ExtendUser.objects.get(email=email)
            return CreateUser(ok=False, error="User already exists")
        except ExtendUser.DoesNotExist:
            try:
<<<<<<< HEAD
                # Setting these fields as empty string if they are not given
                first_name = first_name or ''
                last_name = last_name or ''
                user = ExtendUser(email=email, username=username, first_name=first_name, last_name=last_name)
                user.set_password(password)
=======
                user = ExtendUser(user_id=user_management, email=email, username=username, first_name=first_name, last_name=last_name)
>>>>>>> 415bee1 (Add oauth, users, merchants, products along with CRUD operations)
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
<<<<<<< HEAD
        user = info.context.user
=======
        auth_user = UserManagement.objects.get(email=info.context.user.email)
        user = ExtendUser.objects.get(user_id=auth_user.user_id)
>>>>>>> 415bee1 (Add oauth, users, merchants, products along with CRUD operations)
        if email and email != user.email:
            try:
                ExtendUser.objects.get(email=email)
                return UpdateUser(ok=False, error="That email is already taken")
            except ExtendUser.DoesNotExist:
                user.email = email
<<<<<<< HEAD
=======
                auth_user.email = email
>>>>>>> 415bee1 (Add oauth, users, merchants, products along with CRUD operations)
        if username:
            user.username = username
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
<<<<<<< HEAD
        user.save()
        return UpdateUser(ok=True, user=user)
=======
        try:
            user.save()
            auth_user.save()
            return UpdateUser(ok=True, user=user)
        except Exception as e:
            return UpdateUser(ok=False, error=str(e))
>>>>>>> 415bee1 (Add oauth, users, merchants, products along with CRUD operations)
    

class DeleteUser(graphene.Mutation):
    ok = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info):
<<<<<<< HEAD
        user = info.context.user
        user.delete()
=======
        auth_user = UserManagement.objects.get(email=info.context.user.email)
        auth_user.delete()
>>>>>>> 415bee1 (Add oauth, users, merchants, products along with CRUD operations)
        return DeleteUser(ok=True)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
