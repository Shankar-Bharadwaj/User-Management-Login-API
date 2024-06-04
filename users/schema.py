import graphene, graphql_jwt
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from .models import ExtendUser


class ExtendUserType(DjangoObjectType):
    class Meta:
        model = ExtendUser
        exclude = ('password', )


class Query(graphene.ObjectType):
    user = graphene.List(ExtendUserType)
    logged_in = graphene.Field(ExtendUserType)
    
    def resolve_user(root, info):
        return ExtendUser.objects.all()
    
    @login_required
    def resolve_logged_in(root, info):
        return info.context.user
    

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
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
