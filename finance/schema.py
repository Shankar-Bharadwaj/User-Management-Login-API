import graphene
from graphene_django import DjangoObjectType
from .models import Currency


class CurrencyType(DjangoObjectType):
    class Meta:
        model = Currency


class Query(graphene.ObjectType):
    all_currencies = graphene.List(CurrencyType)
    currency = graphene.Field(CurrencyType, id=graphene.Int())

    def resolve_all_currencies(self, info, **kwargs):
        return Currency.objects.all()

    def resolve_currency(self, info, id):
        return Currency.objects.get(pk=id)


class CreateCurrency(graphene.Mutation):
    currency = graphene.Field(CurrencyType)
    ok = graphene.Boolean()
    error = graphene.String()

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
        return CreateCurrency(ok=True, currency=currency)


class UpdateCurrency(graphene.Mutation):
    currency = graphene.Field(CurrencyType)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        id = graphene.Int()
        currency_name = graphene.String()
        currency_code = graphene.String()
        country_code = graphene.String()

    @classmethod
    def mutate(cls, root, info, id, currency_name, currency_code, country_code):
        try:
            currency = Currency.objects.get(pk=id)
        except Currency.DoesNotExist:
            return UpdateCurrency(ok=False, error="Currency with the given ID does not exist")
        currency.currency_name = currency_name
        currency.currency_code = currency_code
        currency.country_code = country_code
        currency.save()
        return UpdateCurrency(ok=True, currency=currency)


class DeleteCurrency(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        id = graphene.Int()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            currency = Currency.objects.get(pk=id)
        except Currency.DoesNotExist:
            return DeleteCurrency(ok=False, error="Currency with the given ID does not exist")
        currency.delete()
        return DeleteCurrency(ok=True)


class Mutation(graphene.ObjectType):
    create_currency = CreateCurrency.Field()
    update_currency = UpdateCurrency.Field()
    delete_currency = DeleteCurrency.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
