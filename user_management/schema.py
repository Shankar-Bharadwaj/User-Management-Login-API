import graphene
import users.schema
import branches.schema
import companies.schema
import features.schema
import contacts.schema
import location.schema
import finance.schema

class Query(users.schema.Query, branches.schema.Query, companies.schema.Query, features.schema.Query, 
            contacts.schema.Query, location.schema.Query, finance.schema.Query, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation, branches.schema.Mutation, companies.schema.Mutation, 
               features.schema.Mutation, contacts.schema.Mutation, location.schema.Mutation, 
               finance.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
