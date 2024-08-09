import graphene
from graphene_django import DjangoObjectType
from .models import CompanyDetail, CompanyFeatures
from location.models import Country
from features.models import AppFeatures
from graphene_file_upload.scalars import Upload


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


class CreateCompanyDetail(graphene.Mutation):
    company_detail = graphene.Field(CompanyDetailType)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        company_code = graphene.String(required=True)
        company_name = graphene.String(required=True)
        company_logo = Upload()
        company_gstin = graphene.String(required=True)
        company_status = graphene.String(required=True)
        company_dawn = graphene.Time(required=True)
        company_dusk = graphene.Time(required=True)
        company_timeslice = graphene.Time(required=True)
        country_id = graphene.Int(required=True)
        FSSAI = graphene.String(required=True)
        aadhar_number = graphene.String(required=True)
        pan = graphene.String(required=True)
        company_address = graphene.String(required=True)
        business_type = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, company_code, company_name, company_gstin, company_status,
               company_dawn, company_dusk, company_timeslice, country_id, FSSAI, aadhar_number, pan,
               company_address, business_type, company_logo=None):
        try:
            country = Country.objects.get(pk=country_id)
        except Country.DoesNotExist:
            return CreateCompanyDetail(ok=False, error="Country with the given ID does not exist.")
        
        company_detail = CompanyDetail(
            company_code=company_code,
            company_name=company_name,
            company_logo=company_logo,
            company_gstin=company_gstin,
            company_status=company_status,
            company_dawn=company_dawn,
            company_dusk=company_dusk,
            company_timeslice=company_timeslice,
            country_id=country,
            FSSAI=FSSAI,
            aadhar_number=aadhar_number,
            pan=pan,
            company_address=company_address,
            business_type=business_type
        )
        try:
            company_detail.full_clean()
            company_detail.save()
            return CreateCompanyDetail(company_detail=company_detail, ok=True)
        except Exception as e:
            error_messages = {field: messages[0] for field, messages in e.message_dict.items()}
            return CreateCompanyDetail(ok=False, error=error_messages)


class UpdateCompanyDetail(graphene.Mutation):
    company_detail = graphene.Field(CompanyDetailType)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)
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

    @classmethod
    def mutate(cls, root, info, id, company_code=None, company_name=None, company_logo=None, 
               company_gstin=None, company_status=None, company_dawn=None, company_dusk=None, 
               company_timeslice=None, country_id=None, FSSAI=None, aadhar_number=None, pan=None, 
               company_address=None, business_type=None):
        try:
            company_detail = CompanyDetail.objects.get(pk=id)
        except CompanyDetail.DoesNotExist:
            return UpdateCompanyDetail(ok=False, error="Company with the given ID does not exist.")

        if country_id:
            try:
                country = Country.objects.get(pk=country_id)
                company_detail.country_id = country
            except Country.DoesNotExist:
                return UpdateCompanyDetail(ok=False, error="Country with the given ID does not exist.")

        if company_code is not None:
            company_detail.company_code = company_code
        if company_name is not None:
            company_detail.company_name = company_name
        if company_logo is not None:
            company_detail.company_logo = company_logo
        if company_gstin is not None:
            company_detail.company_gstin = company_gstin
        if company_status is not None:
            company_detail.company_status = company_status
        if company_dawn is not None:
            company_detail.company_dawn = company_dawn
        if company_dusk is not None:
            company_detail.company_dusk = company_dusk
        if company_timeslice is not None:
            company_detail.company_timeslice = company_timeslice
        if FSSAI is not None:
            company_detail.FSSAI = FSSAI
        if aadhar_number is not None:
            company_detail.aadhar_number = aadhar_number
        if pan is not None:
            company_detail.pan = pan
        if company_address is not None:
            company_detail.company_address = company_address
        if business_type is not None:
            company_detail.business_type = business_type

        try:
            company_detail.full_clean()
            company_detail.save()
            return UpdateCompanyDetail(ok=True, company_detail=company_detail)
        except Exception as e:
            error_messages = {field: messages[0] for field, messages in e.message_dict.items()}
            return UpdateCompanyDetail(ok=False, error=error_messages)


class DeleteCompanyDetail(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    def mutate(cls, root, info, id):
        try:
            company_detail = CompanyDetail.objects.get(pk=id)
        except CompanyDetail.DoesNotExist:
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
            return UpdateCompanyFeatures(ok=False, error="Company Features with the given ID does not exist.")
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
