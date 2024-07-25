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
        id = graphene.Int()
        company_code = graphene.String()
        company_name = graphene.String()
        company_logo_path = graphene.String()
        company_business_id = graphene.Int()
        company_revenue_id = graphene.Int()
        company_website = graphene.String()
        company_gstin = graphene.String()
        company_status = graphene.String()
        feedback_flag = graphene.String()
        company_dawn = graphene.String()
        company_dusk = graphene.String()
        company_timeslice = graphene.String()
        bank_name = graphene.String()
        bank_code = graphene.String()
        country_id = graphene.Int()
        merchant_id = graphene.String()
        merchant_secret_key = graphene.String()
        latitude = graphene.String()
        longitude = graphene.String()
        radius = graphene.String()
        customer_app = graphene.String()
        appointment_auto_confirm = graphene.Int()
        FSSAI = graphene.String()

    @classmethod
    def mutate(cls, root, info, id, company_code, company_name, company_logo_path, company_business_id, 
               company_revenue_id, company_website, company_gstin, company_status, feedback_flag, 
               company_dawn, company_dusk, company_timeslice, bank_name, bank_code, country_id, 
               merchant_id, merchant_secret_key, latitude, longitude, radius, customer_app, 
               appointment_auto_confirm, FSSAI):
        try:
            country = Country.objects.get(pk=country_id)
            company_detail = CompanyDetail.objects.get(pk=id)
        except Country.DoesNotExist:
            return UpdateCompanyDetail(ok=False, error="Country with the given ID does not exist.")
        except CompanyDetail.DoesNotExist:
            return UpdateCompanyDetail(ok=False, error="Company with the given ID does not exist.")        
        company_detail.company_code = company_code
        company_detail.company_name = company_name
        company_detail.company_logo_path = company_logo_path
        company_detail.company_business_id = company_business_id
        company_detail.company_revenue_id = company_revenue_id
        company_detail.company_website = company_website
        company_detail.company_gstin = company_gstin
        company_detail.company_status = company_status
        company_detail.feedback_flag = feedback_flag
        company_detail.company_dawn = company_dawn
        company_detail.company_dusk = company_dusk
        company_detail.company_timeslice = company_timeslice
        company_detail.bank_name = bank_name
        company_detail.bank_code = bank_code
        company_detail.country_id = country
        company_detail.merchant_id = merchant_id
        company_detail.merchant_secret_key = merchant_secret_key
        company_detail.latitude = latitude
        company_detail.longitude = longitude
        company_detail.radius = radius
        company_detail.customer_app = customer_app
        company_detail.appointment_auto_confirm = appointment_auto_confirm
        company_detail.FSSAI = FSSAI
        company_detail.save()
        return UpdateCompanyDetail(ok=True, company_detail=company_detail)


class DeleteCompanyDetail(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        id = graphene.Int()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            company_detail = CompanyDetail.objects.get(pk=id)
        except CompanyDetail.DoesNotExist:
            return UpdateCompanyDetail(ok=False, error="Company with the given ID does not exist.")  
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
