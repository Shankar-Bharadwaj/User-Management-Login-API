import graphene
from graphene_django.types import DjangoObjectType
from .models import Merchant
from authentication.models import UserManagement
from products.models import Product
from graphql_jwt.decorators import login_required


class MerchantType(DjangoObjectType):
    class Meta:
        model = Merchant


class CreateMerchant(graphene.Mutation):
    merchant = graphene.Field(MerchantType)

    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        phone_number = graphene.String(required=True)
        address = graphene.String(required=True)
        product_id = graphene.UUID(required=True)

    def mutate(self, info, name, email, password, phone_number, address, product_id):
        merchant_management = UserManagement(email=email, user_type='merchant')
        merchant_management.set_password(password)
        merchant_management.save()

        product = Product.objects.get(product_id=product_id)
        merchant = Merchant(
            merchant_id=merchant_management,
            name=name,
            email=email,
            phone_number=phone_number,
            address=address,
            products=product
        )
        merchant.save()
        return CreateMerchant(merchant=merchant)


class UpdateMerchant(graphene.Mutation):
    merchant = graphene.Field(MerchantType)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String()
        phone_number = graphene.String()
        address = graphene.String()
        product_id = graphene.UUID()

    @classmethod
    @login_required
    def mutate(cls, root, info, name=None, email=None, phone_number=None, address=None, product_id=None):
        auth_merchant = UserManagement.objects.get(email=info.context.user.email)
        merchant = Merchant.objects.get(merchant_id=auth_merchant.user_id)

        if email and email != merchant.email:
            try:
                Merchant.objects.get(email=email)
                return UpdateMerchant(ok=False, error="That email is already taken")
            except Merchant.DoesNotExist:
                merchant.email = email
                auth_merchant.email = email
        if name:
            merchant.name = name
        if phone_number:
            merchant.phone_number = phone_number
        if address:
            merchant.address = address
        if product_id is not None:
            try:
                product = Product.objects.get(pk=product_id)
                merchant.products = product
            except Product.DoesNotExist:
                return UpdateMerchant(ok=False, error=f"Product with ID {product_id} does not exist")
        try:
            merchant.save()
            auth_merchant.save()
            return UpdateMerchant(ok=True, merchant=merchant)
        except Exception as e:
            return UpdateMerchant(ok=False, error=str(e))


class DeleteMerchant(graphene.Mutation):
    success = graphene.Boolean()
    
    @classmethod
    @login_required
    def mutate(cls, root, info):
        auth_merchant = UserManagement.objects.get(email=info.context.user.email)
        auth_merchant.delete()
        return DeleteMerchant(success=True)


class Query(graphene.ObjectType):
    logged_in_merchant = graphene.Field(MerchantType, name=graphene.String())
    all_merchants = graphene.List(MerchantType)

    @login_required
    def resolve_logged_in_merchant(self, info):
        auth_merchant = UserManagement.objects.get(email=info.context.user.email)
        merchant = Merchant.objects.get(merchant_id=auth_merchant.user_id)
        if not merchant:
            raise Exception('Merchant not found.')
        return merchant

    def resolve_all_merchants(self, info):
        if not info.context.user.is_authenticated:
            raise Exception("Not authorized to view merchants")
        return Merchant.objects.all()


class Mutation(graphene.ObjectType):
    create_merchant = CreateMerchant.Field()
    update_merchant = UpdateMerchant.Field()
    delete_merchant = DeleteMerchant.Field()
