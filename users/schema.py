import graphene, graphql_jwt
from graphene_django import DjangoObjectType
from oauth2_provider.models import AccessToken
from .models import ExtendUser
from django.utils import timezone


class ExtendUserType(DjangoObjectType):
    class Meta:
        model = ExtendUser
        exclude = ('password', )


class Query(graphene.ObjectType):
    all_users = graphene.List(ExtendUserType)
    logged_in_user = graphene.Field(ExtendUserType)
    
    def resolve_all_users(root, info):
        return ExtendUser.objects.all()
    
    def resolve_logged_in_user(root, info):
        request = info.context
        token = request.META.get('HTTP_AUTHORIZATION')
        # print(token)

        if token is None:
            raise Exception("No access token provided")
        
        token = token.split()[1]

        try:
            access_token = AccessToken.objects.get(token=token)
        except AccessToken.DoesNotExist:
            raise Exception("Invalid access token")

        if access_token.expires < timezone.now():
            raise Exception("Access token has expired")

        return access_token.user
    

class CreateUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(ExtendUserType)

    @classmethod
    def mutate(cls, root, info, email, username, password):
        user = ExtendUser(email=email, username=username)
        user.set_password(password)
        user.save()
        return CreateUser(user=user)
    

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
