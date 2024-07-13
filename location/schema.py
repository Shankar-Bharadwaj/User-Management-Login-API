import graphene
from graphene_django import DjangoObjectType
from .models import Country
from finance.models import Currency


class CountryType(DjangoObjectType):
    class Meta:
        model = Country


class Query(graphene.ObjectType):
    all_countries = graphene.List(CountryType)
    country = graphene.Field(CountryType, id=graphene.Int())

    def resolve_all_countries(self, info, **kwargs):
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
            currency_id=currency
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
    
    ok = graphene.Boolean()
    error = graphene.String()

    @classmethod
    def mutate(cls, root , info, id, country_code, country_name, mobile_format_id, currency_id):
        try:
            currency = Currency.objects.get(pk=currency_id)
            country = Country.objects.get(pk=id)
        except Currency.DoesNotExist:
            raise Exception("Currency with the given ID does not exist.")
        except Country.DoesNotExist:
            return UpdateCountry(ok=False, error="Country with the ID does not exist")
        country.country_code = country_code
        country.country_name = country_name
        country.mobile_format_id = mobile_format_id
        country.currency_id = currency
        country.save()
        return UpdateCountry(ok=True, country=country)


class DeleteCountry(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    ok = graphene.Boolean()
    error = graphene.String()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            country = Country.objects.get(pk=id)
        except Country.DoesNotExist:
            return DeleteCountry(ok=False, error="Country with the ID does not exist")
        country = Country.objects.get(pk=id)
        country.delete()
        return DeleteCountry(ok=True)


class Mutation(graphene.ObjectType):
    create_country = CreateCountry.Field()
    update_country = UpdateCountry.Field()
    delete_country = DeleteCountry.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
