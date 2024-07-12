import graphene
from graphene_django import DjangoObjectType
from .models import BranchDetail
from companies.models import CompanyDetail
from contacts.models import ContactDetail


class BranchDetailType(DjangoObjectType):
    class Meta:
        model = BranchDetail


class Query(graphene.ObjectType):
    all_branch_details = graphene.List(BranchDetailType)
    branch_detail = graphene.Field(BranchDetailType, id=graphene.Int())

    def resolve_all_branch_details(root, info, **kwargs):
        return BranchDetail.objects.all()

    def resolve_branch_detail(root, info, id):
        return BranchDetail.objects.get(pk=id)


class CreateBranchDetail(graphene.Mutation):
    branch_detail = graphene.Field(BranchDetailType)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        company_id = graphene.Int()
        branch_status = graphene.String()
        contact_id = graphene.Int()
        branch_type = graphene.String()
        work_type = graphene.Int()
        cash_drawer = graphene.String()
        zone_id = graphene.Int()

    @classmethod
    def mutate(cls, root, info, company_id, branch_status, contact_id, branch_type, work_type, cash_drawer, zone_id):
        try:
            company = CompanyDetail.objects.get(pk=company_id)
            contact = ContactDetail.objects.get(pk=contact_id)
        except CompanyDetail.DoesNotExist:
            return CreateBranchDetail(ok=False, error="Company with the given ID does not exist.")
        except ContactDetail.DoesNotExist:
            return CreateBranchDetail(ok=False, error="Contact with the given ID does not exist.")
        branch_detail = BranchDetail(
            company_id=company_id,
            branch_status=branch_status,
            contact_id=contact_id,
            branch_type=branch_type,
            work_type=work_type,
            cash_drawer=cash_drawer,
            zone_id=zone_id
        )
        branch_detail.save()
        return CreateBranchDetail(ok=True, branch_detail=branch_detail)


class UpdateBranchDetail(graphene.Mutation):
    branch_detail = graphene.Field(BranchDetailType)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        id = graphene.Int()
        company_id = graphene.Int()
        branch_status = graphene.String()
        contact_id = graphene.Int()
        branch_type = graphene.String()
        work_type = graphene.Int()
        cash_drawer = graphene.String()
        zone_id = graphene.Int()

    @classmethod
    def mutate(cls, root, info, id, company_id, branch_status, contact_id, branch_type, work_type, cash_drawer, zone_id):
        try:
            company = CompanyDetail.objects.get(pk=company_id)
            contact = ContactDetail.objects.get(pk=contact_id)
            branch_detail = BranchDetail.objects.get(pk=id)
        except CompanyDetail.DoesNotExist:
            return UpdateBranchDetail(ok=False, error="Company with the given ID does not exist.")
        except ContactDetail.DoesNotExist:
            return UpdateBranchDetail(ok=False, error="Contact with the given ID does not exist.")
        except BranchDetail.DoesNotExist:
            return UpdateBranchDetail(ok=False, error="Branch with the given ID does not exist.")        
        branch_detail.company_id = company_id
        branch_detail.branch_status = branch_status
        branch_detail.contact_id = contact_id
        branch_detail.branch_type = branch_type
        branch_detail.work_type = work_type
        branch_detail.cash_drawer = cash_drawer
        branch_detail.zone_id = zone_id
        branch_detail.save()
        return UpdateBranchDetail(ok=True, branch_detail=branch_detail)


class DeleteBranchDetail(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        id = graphene.Int()

    @classmethod
    def mutate(cls, roots, info, id):
        try:
            branch_detail = BranchDetail.objects.get(pk=id)
        except BranchDetail.DoesNotExist:
            return UpdateBranchDetail(ok=False, error="Branch with the given ID does not exist.") 
        branch_detail.delete()
        return DeleteBranchDetail(ok=True)


class Mutation(graphene.ObjectType):
    create_branch_detail = CreateBranchDetail.Field()
    update_branch_detail = UpdateBranchDetail.Field()
    delete_branch_detail = DeleteBranchDetail.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
