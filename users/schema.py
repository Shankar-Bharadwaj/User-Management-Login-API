import graphene
from graphene_django import DjangoObjectType
from oauth2_provider.models import AccessToken
from .models import UserDetail, UserCompanies, UserBranchDetail
from graphql_jwt.decorators import login_required
from authentication.models import UserLogin
from companies.models import CompanyDetail, CompanyFeatures
from branches.models import BranchDetail
from companies.schema import CompanyFeaturesType


class UserDetailType(DjangoObjectType):
    class Meta:
        model = UserDetail


class UserCompaniesType(DjangoObjectType):
    class Meta:
        model = UserCompanies


class UserBranchDetailType(DjangoObjectType):
    class Meta:
        model = UserBranchDetail
    

class Query(graphene.ObjectType):
    all_user_details = graphene.List(UserDetailType)
    user_detail = graphene.Field(UserDetailType, id=graphene.Int())
    logged_in_user = graphene.Field(UserDetailType)
    logged_in_user_company = graphene.Field(UserCompaniesType)
    logged_in_user_branch = graphene.Field(UserBranchDetailType)
    logged_in_user_company_features = graphene.List(CompanyFeaturesType)
    all_user_companies = graphene.List(UserCompaniesType)
    user_company = graphene.Field(UserCompaniesType, id=graphene.Int())
    all_user_branch_details = graphene.List(UserBranchDetailType)
    user_branch_detail = graphene.Field(UserBranchDetailType, id=graphene.Int())

    def all_resolve_user_details(root, info, **kwargs):
        return UserDetail.objects.all()

    def resolve_user_detail(root, info, id):
        return UserDetail.objects.get(pk=id)

    @login_required
    def resolve_logged_in_user(root, info):
        auth_user = UserLogin.objects.get(email=info.context.user.email)
        user = UserDetail.objects.get(user_id=auth_user.user_id)
        if not user:
            raise Exception('User not found.')
        return user

    @login_required
    def resolve_logged_in_user_branch(root, info):
        auth_user = UserLogin.objects.get(email=info.context.user.email)
        user_branch = UserBranchDetail.objects.get(user_id=auth_user.user_id)
        if not user_branch:
            raise Exception('User Branches not found.')
        return user_branch

    @login_required
    def resolve_logged_in_user_company(root, info):
        auth_user = UserLogin.objects.get(email=info.context.user.email)
        user_company = UserCompanies.objects.get(user_id=auth_user.user_id)
        if not user_company:
            raise Exception('User Companies not found.')
        return user_company

    @login_required
    def resolve_logged_in_user_company_features(root, info):
        auth_user = UserLogin.objects.get(email=info.context.user.email)
        user_company = UserCompanies.objects.get(user_id=auth_user.user_id)
        if not user_company:
            raise Exception('User Companies not found.')
        company_id = user_company.company_id
        company_features = CompanyFeatures.objects.filter(company_id=company_id)
        return company_features

    def resolve_all_user_companies(root, info, **kwargs):
        return UserCompanies.objects.all()

    def resolve_user_company(root, info, id):
        return UserCompanies.objects.get(pk=id)

    def resolve_all_user_branch_details(root, info, **kwargs):
        return UserBranchDetail.objects.all()

    def resolve_user_branch_detail(root, info, id):
        return UserBranchDetail.objects.get(pk=id)


class CreateUserDetail(graphene.Mutation):
    class Arguments:
        user_mobile = graphene.Int(required=True)
        international_calling_code = graphene.Int(required=True)
        calling_country = graphene.String(required=True)
        email = graphene.String(required=True)
        user_pin = graphene.String(required=True)
        isPinResetRequested = graphene.Boolean(required=False)

        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        user_dob = graphene.Date(required=True)
        marital_status = graphene.Boolean(required=False)
        user_gender = graphene.Boolean(required=False)
        user_status = graphene.Boolean(required=False)

    user = graphene.Field(UserDetailType)

    ok = graphene.Boolean()
    error = graphene.String()

    @classmethod
    def mutate(cls, root, info, user_mobile, international_calling_code, calling_country, 
               email, user_pin, isPinResetRequested, first_name, last_name, user_dob,
               marital_status, user_gender, user_status):
        try:
            UserLogin.objects.get(email=email)
            return CreateUserDetail(ok=False, error="User already exists")
        except UserLogin.DoesNotExist:
            try:
                user_login = UserLogin(user_mobile=user_mobile, 
                                        international_calling_code=international_calling_code, 
                                        calling_country=calling_country, email=email,
                                        isPinResetRequested=isPinResetRequested)
                user_login.set_user_pin(user_pin)
                user = UserDetail(user_id=user_login, first_name=first_name, last_name=last_name, user_dob=user_dob, 
                                  marital_status=marital_status, user_gender=user_gender, 
                                  user_status=user_status)
                user_login.save()
                user.save()
                return CreateUserDetail(ok=True, user=user)
            except Exception as e:
                print(e)
                return CreateUserDetail(ok=False, error="Can't create user")


class UpdateUserDetail(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        user_mobile = graphene.Int(required=True)
        international_calling_code = graphene.Int(required=True)
        calling_country = graphene.String(required=True)
        email = graphene.String(required=True)
        isPinResetRequested = graphene.Boolean(required=False)

        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        user_dob = graphene.Date(required=True)
        marital_status = graphene.Boolean(required=False)
        user_gender = graphene.Boolean(required=False)
        user_status = graphene.Boolean(required=False)

    user = graphene.Field(UserDetailType)
    ok = graphene.Boolean()
    error = graphene.String()

    @classmethod
    # @login_required
    def mutate(cls, root, info, id, email, first_name, last_name, user_dob, 
               marital_status, user_gender, user_status):
        try:
            auth_user = UserLogin.objects.get(user_id=id)
        except UserLogin.DoesNotExist:
            return UpdateUserDetail(ok=False, error="User with the given ID does not exist.")
        user_detail = UserDetail.objects.get(user_id=auth_user.user_id)
        if email and email != auth_user.email:
            try:
                UserLogin.objects.get(email=email)
                return UpdateUserDetail(ok=False, error="That email is already taken")
            except UserDetail.DoesNotExist:
                auth_user.email = email
        if first_name:
            user_detail.first_name = first_name
        if last_name:
            user_detail.last_name = last_name
        if user_dob:
            user_detail.user_dob = user_dob
        if marital_status:
            user_detail.marital_status = marital_status
        if user_gender:
            user_detail.user_gender = user_gender
        if user_status:
            user_detail.user_status = user_status
        try:
            user_detail.save()
            auth_user.save()
            return UpdateUserDetail(ok=True, user=user_detail)
        except Exception as e:
            return UpdateUserDetail(ok=False, error=str(e))
    

class DeleteUserDetail(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.String()

    @classmethod
    # @login_required
    def mutate(cls, root, info, id):
        try:
            auth_user = UserLogin.objects.get(user_id=id)
        except UserLogin.DoesNotExist:
            return UpdateUserDetail(ok=False, error="User with the given ID does not exist.")
        auth_user.delete()
        return DeleteUserDetail(ok=True)
    

class CreateUserCompanies(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        company_id = graphene.Int(required=True)
        user_type = graphene.Boolean()
        status = graphene.Boolean()

    user_companies = graphene.Field(UserCompaniesType)
    ok = graphene.Boolean()
    error = graphene.String()

    @classmethod
    def mutate(cls, root, info, user_id, company_id, user_type, status):
        try:
            company = CompanyDetail.objects.get(pk=company_id)
            auth_user = UserLogin.objects.get(pk=user_id)
        except CompanyDetail.DoesNotExist:
            return UpdateUserDetail(ok=False, error="Company with the given ID does not exist.")
        except UserLogin.DoesNotExist:
            return UpdateUserDetail(ok=False, error="User with the given ID does not exist.")
        user_companies = UserCompanies(
            user_id=auth_user,
            company_id=company,
            user_type=user_type,
            status=status
        )
        user_companies.save()
        return CreateUserCompanies(user_companies=user_companies, ok=True)
    

class UpdateUserCompanies(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        user_id = graphene.Int(required=True)
        company_id = graphene.Int(required=True)
        user_type = graphene.Boolean()
        status = graphene.Boolean()

    user_companies = graphene.Field(UserCompaniesType)
    ok = graphene.Boolean()
    error = graphene.String()

    @classmethod
    def mutate(cls, root, info, id, user_id, company_id, user_type=None, status=None):
        try:
            company = CompanyDetail.objects.get(pk=company_id)
            user = UserLogin.objects.get(pk=id)
            user2 = UserLogin.objects.get(pk=user_id)
        except CompanyDetail.DoesNotExist:
            return UpdateUserCompanies(ok=False, error="Company with the given ID does not exist.")
        except UserLogin.DoesNotExist:
            return UpdateUserCompanies(ok=False, error="User with the given ID does not exist.")
        user_companies = UserCompanies.objects.get(user_id=user.user_id)
        user_companies.user_id = user2
        user_companies.company_id = company
        user_companies.user_type = user_type
        user_companies.status = status
        user_companies.save()
        return UpdateUserCompanies(ok=True, user_companies=user_companies)


class DeleteUserCompanies(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        company_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    error = graphene.String()

    @classmethod
    def mutate(cls, root, info, user_id, company_id):
        try:
            user_companies = UserCompanies.objects.get(user_id=user_id, company_id=company_id)
            user_companies.delete()
            return DeleteUserCompanies(ok=True)
        except UserCompanies.DoesNotExist:
            return DeleteUserCompanies(ok=False, error="UserCompany does not exist")


class CreateUserBranchDetail(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        branch_id = graphene.Int(required=True)
        user_branch_status = graphene.Boolean()

    user_branch_detail = graphene.Field(UserBranchDetailType)
    ok = graphene.Boolean()
    error = graphene.String()

    @classmethod
    def mutate(cls, root, info, user_id, branch_id, user_branch_status):
        try:
            branch = BranchDetail.objects.get(pk=branch_id)
            user = UserLogin.objects.get(pk=user_id)
        except BranchDetail.DoesNotExist:
            return CreateUserBranchDetail(ok=False, error="Branch with the given ID does not exist.")
        except UserLogin.DoesNotExist:
            return CreateUserBranchDetail(ok=False, error="User with the given ID does not exist.")
        user_branch_detail = UserBranchDetail(
            user_id=user,
            branch_id=branch,
            user_branch_status=user_branch_status,
        )
        user_branch_detail.save() 
        return CreateUserBranchDetail(ok=True, user_branch_detail=user_branch_detail)


class UpdateUserBranchDetail(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        user_id = graphene.Int(required=True)
        branch_id = graphene.Int(required=True)
        user_branch_status = graphene.Int()

    user_branch_detail = graphene.Field(UserBranchDetailType)
    ok = graphene.Boolean()
    error = graphene.String()

    @classmethod
    def mutate(cls, root, info, id, user_id, branch_id, user_branch_status=None):
        try:
            branch = BranchDetail.objects.get(pk=branch_id)
            user = UserLogin.objects.get(pk=id)
            user2 = UserLogin.objects.get(pk=user_id)
        except BranchDetail.DoesNotExist:
            return UpdateUserBranchDetail(ok=False, error="Branch with the given ID does not exist.")
        except UserLogin.DoesNotExist:
            return UpdateUserBranchDetail(ok=False, error="User with the given ID does not exist.")
        user_branch_detail = UserBranchDetail.objects.get(user_id=user.user_id)
        user_branch_detail.user_id = user2
        user_branch_detail.branch_id = branch
        user_branch_detail.user_branch_status = user_branch_status
        user_branch_detail.save()
        return UpdateUserBranchDetail(ok=True, user_branch_detail=user_branch_detail)
        

class DeleteUserBranchDetail(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        branch_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    error = graphene.String()

    @classmethod
    def mutate(cls, root, info, user_id, branch_id):
        try:
            user_branch_detail = UserBranchDetail.objects.get(user_id=user_id, branch_id=branch_id)
            user_branch_detail.delete()
            return DeleteUserBranchDetail(ok=True)
        except UserBranchDetail.DoesNotExist:
            return DeleteUserBranchDetail(ok=False, error="UserBranchDetail does not exist")
        

class Mutation(graphene.ObjectType):
    create_user = CreateUserDetail.Field()
    update_user = UpdateUserDetail.Field()
    delete_user = DeleteUserDetail.Field()
    create_user_company = CreateUserCompanies.Field()
    update_user_company = UpdateUserCompanies.Field()
    delete_user_company = DeleteUserCompanies.Field()
    create_user_branch_detail = CreateUserBranchDetail.Field()
    update_user_branch_detail = UpdateUserBranchDetail.Field()
    delete_user_branch_detail = DeleteUserBranchDetail.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
