import graphene
from graphene_django.types import DjangoObjectType
from .models import Product

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class CreateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        price = graphene.Float(required=True)

    def mutate(self, info, name, description, price):
        product = Product(name=name, description=description, price=price)
        product.save()
        return CreateProduct(product=product)

class UpdateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        product_id = graphene.UUID(required=True)
        name = graphene.String()
        description = graphene.String()
        price = graphene.Float()

    def mutate(self, info, product_id, name=None, description=None, price=None):
        product = Product.objects.get(pk=product_id)

        if name:
            product.name = name
        if description:
            product.description = description
        if price:
            product.price = price

        product.save()
        return UpdateProduct(product=product)

class DeleteProduct(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        product_id = graphene.UUID(required=True)

    def mutate(self, info, product_id):
        product = Product.objects.get(pk=product_id)
        product.delete()
        return DeleteProduct(success=True)

class Query(graphene.ObjectType):
    product = graphene.Field(ProductType, name=graphene.String())
    products = graphene.List(ProductType)

    def resolve_product(self, info, name):
        return Product.objects.get(name=name)

    def resolve_products(self, info):
        return Product.objects.all()

class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
