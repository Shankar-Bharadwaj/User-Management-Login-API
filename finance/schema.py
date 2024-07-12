import graphene
from graphene_django import DjangoObjectType
from .models import Currency


class CurrencyType(DjangoObjectType):
    class Meta:
        model = Currency


class Query(graphene.ObjectType):
    currencies = graphene.List(CurrencyType)
    currency = graphene.Field(CurrencyType, id=graphene.Int())

    def resolve_currencies(self, info, **kwargs):
        return Currency.objects.all()

    def resolve_currency(self, info, id):
        return Currency.objects.get(pk=id)


class CreateCurrency(graphene.Mutation):
    currency = graphene.Field(CurrencyType)

    class Arguments:
        currency_name = graphene.String()
        currency_code = graphene.String()
        country_code = graphene.String()

    @classmethod
    def mutate(cls, root, info, currency_name, currency_code, country_code):
        currency = Currency(
            currency_name=currency_name,
            currency_code=currency_code,
            country_code=country_code
        )
        currency.save()
        return CreateCurrency(currency=currency)


class UpdateCurrency(graphene.Mutation):
    currency = graphene.Field(CurrencyType)

    class Arguments:
        id = graphene.Int()
        currency_name = graphene.String()
        currency_code = graphene.String()
        country_code = graphene.String()

    @classmethod
    def mutate(cls, root, info, id, currency_name, currency_code, country_code):
        currency = Currency.objects.get(pk=id)
        currency.currency_name = currency_name
        currency.currency_code = currency_code
        currency.country_code = country_code
        currency.save()
        return UpdateCurrency(currency=currency)


class DeleteCurrency(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.Int()

    @classmethod
    def mutate(cls, root, info, id):
        currency = Currency.objects.get(pk=id)
        currency.delete()
        return DeleteCurrency(success=True)


class Mutation(graphene.ObjectType):
    create_currency = CreateCurrency.Field()
    update_currency = UpdateCurrency.Field()
    delete_currency = DeleteCurrency.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
