import graphene
from graphene_django import DjangoObjectType
from .models import Features


class FeaturesType(DjangoObjectType):
    class Meta:
        model = Features


class Query(graphene.ObjectType):
    features_list = graphene.List(FeaturesType)
    feature = graphene.Field(FeaturesType, id=graphene.Int())

    def resolve_features_list(root, info, **kwargs):
        return Features.objects.all()

    def resolve_feature(root, info, id):
        return Features.objects.get(pk=id)


class CreateFeature(graphene.Mutation):
    feature = graphene.Field(FeaturesType)

    class Arguments:
        feature_name = graphene.String()
        feature_description = graphene.String()
        feature_type = graphene.String()
        feature_status = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, feature_name, feature_description, feature_type, feature_status):
        feature = Features(
            feature_name=feature_name,
            feature_description=feature_description,
            feature_type=feature_type,
            feature_status=feature_status
        )
        feature.save()
        return CreateFeature(feature=feature)


class UpdateFeature(graphene.Mutation):
    feature = graphene.Field(FeaturesType)

    class Arguments:
        id = graphene.Int()
        feature_name = graphene.String()
        feature_description = graphene.String()
        feature_type = graphene.String()
        feature_status = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id, feature_name, feature_description, feature_type, feature_status):
        feature = Features.objects.get(pk=id)
        feature.feature_name = feature_name
        feature.feature_description = feature_description
        feature.feature_type = feature_type
        feature.feature_staus = feature_status
        feature.save()
        return UpdateFeature(feature=feature)


class DeleteFeature(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.Int()

    @classmethod
    def mutate(cls, root, info, id):
        feature = Features.objects.get(pk=id)
        feature.delete()
        return DeleteFeature(success=True)


class Mutation(graphene.ObjectType):
    create_feature = CreateFeature.Field()
    update_feature = UpdateFeature.Field()
    delete_feature = DeleteFeature.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
