import graphene
import users.schema
import merchants.schema
import products.schema

class Query(users.schema.Query, merchants.schema.Query, products.schema.Query, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation, merchants.schema.Mutation, products.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
