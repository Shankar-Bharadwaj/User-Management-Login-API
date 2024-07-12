import graphene
from graphene_django import DjangoObjectType
from .models import Country
from finance.models import Currency


class CountryType(DjangoObjectType):
    class Meta:
        model = Country


class Query(graphene.ObjectType):
    countries = graphene.List(CountryType)
    country = graphene.Field(CountryType, id=graphene.Int())

    def resolve_countries(self, info, **kwargs):
        return Country.objects.all()

    def resolve_country(self, info, id):
        return Country.objects.get(pk=id)


class CreateCountry(graphene.Mutation):
    country = graphene.Field(CountryType)

    class Arguments:
        country_code = graphene.String()
        country_name = graphene.String()
        mobile_format_id = graphene.Int()
        currency_id = graphene.Int()

    @classmethod
    def mutate(cls, root, info, country_code, country_name, mobile_format_id, currency_id):
        try:
            currency = Currency.objects.get(pk=currency_id)
        except Currency.DoesNotExist:
            raise Exception("Currency with the given ID does not exist.")
        country = Country(
            country_code=country_code,
            country_name=country_name,
            mobile_format_id=mobile_format_id,
            currency_id=currency_id
        )
        country.save()
        return CreateCountry(country=country)


class UpdateCountry(graphene.Mutation):
    country = graphene.Field(CountryType)

    class Arguments:
        id = graphene.Int()
        country_code = graphene.String()
        country_name = graphene.String()
        mobile_format_id = graphene.Int()
        currency_id = graphene.Int()

    @classmethod
    def mutate(cls, root , info, id, country_code, country_name, mobile_format_id, currency_id):
        try:
            currency = Currency.objects.get(pk=currency_id)
        except Currency.DoesNotExist:
            raise Exception("Currency with the given ID does not exist.")
        country = Country.objects.get(pk=id)
        country.country_code = country_code
        country.country_name = country_name
        country.mobile_format_id = mobile_format_id
        country.currency_id = currency_id
        country.save()
        return UpdateCountry(country=country)


class DeleteCountry(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.Int()

    @classmethod
    def mutate(cls, root, info, id):
        country = Country.objects.get(pk=id)
        country.delete()
        return DeleteCountry(success=True)


class Mutation(graphene.ObjectType):
    create_country = CreateCountry.Field()
    update_country = UpdateCountry.Field()
    delete_country = DeleteCountry.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)