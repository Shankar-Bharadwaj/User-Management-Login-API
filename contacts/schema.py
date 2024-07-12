import graphene
from graphene_django import DjangoObjectType
from .models import ContactDetail


class ContactDetailType(DjangoObjectType):
    class Meta:
        model = ContactDetail


class Query(graphene.ObjectType):
    all_contact_details = graphene.List(ContactDetailType)
    contact_detail = graphene.Field(ContactDetailType, id=graphene.Int())

    def resolve_all_contact_details(self, info, **kwargs):
        return ContactDetail.objects.all()

    def resolve_contact_detail(self, info, id):
        return ContactDetail.objects.get(pk=id)


class CreateContactDetail(graphene.Mutation):
    contact_detail = graphene.Field(ContactDetailType)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        phone = graphene.String()
        email = graphene.String()
        pincode = graphene.String()
        address1 = graphene.String()
        area = graphene.String()
        city = graphene.String()
        state = graphene.String()
        country = graphene.String()

    @classmethod
    def mutate(cls, root, info, phone, email, pincode, address1, area, city, state, country):
        contact_detail = ContactDetail(
            phone=phone,
            email=email,
            pincode=pincode,
            address1=address1,
            area=area,
            city=city,
            state=state,
            country=country
        )
        contact_detail.save()
        return CreateContactDetail(contact_detail=contact_detail)


class UpdateContactDetail(graphene.Mutation):
    contact_detail = graphene.Field(ContactDetailType)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        id = graphene.Int()
        phone = graphene.String()
        email = graphene.String()
        pincode = graphene.String()
        address1 = graphene.String()
        area = graphene.String()
        city = graphene.String()
        state = graphene.String()
        country = graphene.String()

    @classmethod
    def mutate(cls, root, info, id, phone, email, pincode, address1, area, city, state, country):
        try:
            contact_detail = ContactDetail.objects.get(pk=id)
        except ContactDetail.DoesNotExist:
            return UpdateContactDetail(ok=False, error="Contact with the given ID does not exist")
        contact_detail.phone = phone
        contact_detail.email = email
        contact_detail.pincode = pincode
        contact_detail.address1 = address1
        contact_detail.area = area
        contact_detail.city = city
        contact_detail.state = state
        contact_detail.country = country
        contact_detail.save()
        return UpdateContactDetail(contact_detail=contact_detail)


class DeleteContactDetail(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        id = graphene.Int()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            contact_detail = ContactDetail.objects.get(pk=id)
        except ContactDetail.DoesNotExist:
            return UpdateContactDetail(ok=False, error="Contact with the given ID does not exist")
        contact_detail.delete()
        return DeleteContactDetail(ok=True)


class Mutation(graphene.ObjectType):
    create_contact_detail = CreateContactDetail.Field()
    update_contact_detail = UpdateContactDetail.Field()
    delete_contact_detail = DeleteContactDetail.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
