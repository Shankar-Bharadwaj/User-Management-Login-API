import graphene
from graphene_django import DjangoObjectType
from .models import CompanyDetail, CompanyFeatures
from location.models import Country
from features.models import AppFeatures
from graphene_file_upload.scalars import Upload
from django.core.exceptions import ValidationError
from user_management.utils import get_object


class CompanyDetailType(DjangoObjectType):
    class Meta:
        model = CompanyDetail


class CompanyFeaturesType(DjangoObjectType):
    class Meta:
        model = CompanyFeatures


class Query(graphene.ObjectType):
    all_company_details = graphene.List(CompanyDetailType)
    company_detail = graphene.Field(CompanyDetailType, id=graphene.Int())
    all_company_features = graphene.List(CompanyFeaturesType)
    company_feature = graphene.Field(CompanyFeaturesType, id=graphene.Int())

    def resolve_all_company_details(self, info, **kwargs):
        return CompanyDetail.objects.all()

    def resolve_company_detail(self, info, id):
        return CompanyDetail.objects.get(pk=id)

    def resolve_all_company_features(self, info, **kwargs):
        return CompanyFeatures.objects.all()

    def resolve_company_feature(self, info, id):
        return CompanyFeatures.objects.get(pk=id)


class CompanyDetailInput(graphene.InputObjectType):
    company_code = graphene.String()
    company_name = graphene.String()
    company_logo = Upload()
    company_gstin = graphene.String()
    company_status = graphene.String()
    company_dawn = graphene.Time()
    company_dusk = graphene.Time()
    company_timeslice = graphene.Time()
    country_id = graphene.Int()
    FSSAI = graphene.String()
    aadhar_number = graphene.String()
    pan = graphene.String()
    company_address = graphene.String()
    business_type = graphene.String()


class CreateCompanyDetail(graphene.Mutation):
    company_detail = graphene.Field(CompanyDetailType)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        input = CompanyDetailInput(required=True)

    @classmethod
    def mutate(cls, root, info, input):
        country = get_object(Country, input.country_id)
        if country is None:
            return CreateCompanyDetail(ok=False, error="Country with the given ID does not exist.")
        
        company_detail = CompanyDetail()
        for key, value in input.items():
            if value is not None and key != 'country_id':
                setattr(company_detail, key, value)
        
        company_detail.country_id = country

        try:
            company_detail.full_clean()
            company_detail.save()
            return CreateCompanyDetail(company_detail=company_detail, ok=True)
        except ValidationError as e:
            error_messages = {field: messages[0] for field, messages in e.message_dict.items()}
            return CreateCompanyDetail(ok=False, error=error_messages)
        except Exception as e:
            return CreateCompanyDetail(ok=False, error=str(e))


class UpdateCompanyDetail(graphene.Mutation):
    company_detail = graphene.Field(CompanyDetailType)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)
        input = CompanyDetailInput(required=True)

    @classmethod
    def mutate(cls, root, info, id, input):
        company_detail = get_object(CompanyDetail, id)
        if company_detail is None:
            return UpdateCompanyDetail(ok=False, error="Company with the given ID does not exist.")

        if input.country_id:
            country = get_object(Country, input.country_id)
            if country is None:
                return UpdateCompanyDetail(ok=False, error="Country with the given ID does not exist.")
            company_detail.country_id = country

        for key, value in input.items():
            if key != 'country_id':
                setattr(company_detail, key, value)

        try:
            company_detail.full_clean()
            company_detail.save()
            return UpdateCompanyDetail(ok=True, company_detail=company_detail)
        except ValidationError as e:
            error_messages = {field: messages[0] for field, messages in e.message_dict.items()}
            return UpdateCompanyDetail(ok=False, error=error_messages)
        except Exception as e:
            return UpdateCompanyDetail(ok=False, error=str(e))


class DeleteCompanyDetail(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    def mutate(cls, root, info, id):
        company_detail = get_object(CompanyDetail, id)
        if company_detail is None:
            return DeleteCompanyDetail(ok=False, error="Company with the given ID does not exist.")
        company_detail.delete()
        return DeleteCompanyDetail(ok=True)


class CreateCompanyFeatures(graphene.Mutation):
    company_feature = graphene.Field(CompanyFeaturesType)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        feature_id = graphene.Int()
        company_id = graphene.Int()
        company_feature_status = graphene.String()

    @classmethod
    def mutate(cls, root, info, feature_id, company_id, company_feature_status):
        try:
            features = AppFeatures.objects.get(pk=feature_id)
            company = CompanyDetail.objects.get(pk=company_id)
        except AppFeatures.DoesNotExist:
            return CreateCompanyFeatures(ok=False, error="App Features with the given ID does not exist")
        except CompanyDetail.DoesNotExist:
            return CreateCompanyFeatures(ok=False, error="Company with the given ID does not exist.")
        company_feature = CompanyFeatures(
            feature_id=features,
            company_id=company,
            company_feature_status=company_feature_status
        )
        company_feature.save()
        return CreateCompanyFeatures(ok=True, company_feature=company_feature)


class UpdateCompanyFeatures(graphene.Mutation):
    company_feature = graphene.Field(CompanyFeaturesType)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        id = graphene.Int()
        feature_id = graphene.Int()
        company_id = graphene.Int()
        company_feature_status = graphene.String()

    @classmethod
    def mutate(cls, root, info, id, feature_id, company_id, company_feature_status):
        try:
            features = AppFeatures.objects.get(pk=feature_id)
            company = CompanyDetail.objects.get(pk=company_id)
            company_feature = CompanyFeatures.objects.get(pk=id)
        except AppFeatures.DoesNotExist:
            return UpdateCompanyFeatures(ok=True, error="App Features with the given ID does not exist.")
        except CompanyDetail.DoesNotExist:
            return UpdateCompanyFeatures(ok=False, error="Company with the given ID does not exist.")
        except CompanyFeatures.DoesNotExist:
            return UpdateCompanyFeatures(ok=False, error="Company Features with the given ID does not exist.")
        company_feature = CompanyFeatures.objects.get(pk=id)
        company_feature.feature_id = features
        company_feature.company_id = company
        company_feature.company_feature_status = company_feature_status
        company_feature.save()
        return UpdateCompanyFeatures(ok=False, company_feature=company_feature)


class DeleteCompanyFeatures(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        id = graphene.Int()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            company_feature = CompanyFeatures.objects.get(pk=id)
        except CompanyFeatures.DoesNotExist:
            return DeleteCompanyFeatures(ok=False, error="Company Features with the given ID does not exist.")
        company_feature.delete()
        return DeleteCompanyFeatures(ok=True)


class Mutation(graphene.ObjectType):
    create_company_detail = CreateCompanyDetail.Field()
    update_company_detail = UpdateCompanyDetail.Field()
    delete_company_detail = DeleteCompanyDetail.Field()
    create_company_features = CreateCompanyFeatures.Field()
    update_company_features = UpdateCompanyFeatures.Field()
    delete_company_features = DeleteCompanyFeatures.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
