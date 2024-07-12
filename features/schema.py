import graphene
from graphene_django import DjangoObjectType
from .models import AppFeatures


class FeaturesType(DjangoObjectType):
    class Meta:
        model = AppFeatures


class Query(graphene.ObjectType):
    features_list = graphene.List(FeaturesType)
    feature = graphene.Field(FeaturesType, id=graphene.Int())

    def resolve_features_list(root, info, **kwargs):
        return AppFeatures.objects.all()

    def resolve_feature(root, info, id):
        return AppFeatures.objects.get(pk=id)


class CreateFeature(graphene.Mutation):
    feature = graphene.Field(FeaturesType)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        feature_name = graphene.String()
        feature_description = graphene.String()
        feature_type = graphene.String()
        feature_status = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, feature_name, feature_description, feature_type, feature_status):
        feature = AppFeatures(
            feature_name=feature_name,
            feature_description=feature_description,
            feature_type=feature_type,
            feature_status=feature_status
        )
        feature.save()
        return CreateFeature(ok=True, feature=feature)


class UpdateFeature(graphene.Mutation):
    feature = graphene.Field(FeaturesType)
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        id = graphene.Int()
        feature_name = graphene.String()
        feature_description = graphene.String()
        feature_type = graphene.String()
        feature_status = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id, feature_name, feature_description, feature_type, feature_status):
        try:
            feature = AppFeatures.objects.get(pk=id)
        except AppFeatures.DoesNotExist:
            return UpdateFeature(ok=False, error="App Feature with the given ID does not exist")
        feature.feature_name = feature_name
        feature.feature_description = feature_description
        feature.feature_type = feature_type
        feature.feature_staus = feature_status
        feature.save()
        return UpdateFeature(feature=feature, ok=True)


class DeleteFeature(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        id = graphene.Int()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            feature = AppFeatures.objects.get(pk=id)
        except AppFeatures.DoesNotExist:
            return UpdateFeature(ok=False, error="App Feature with the given ID does not exist")
        feature.delete()
        return DeleteFeature(ok=True)


class Mutation(graphene.ObjectType):
    create_feature = CreateFeature.Field()
    update_feature = UpdateFeature.Field()
    delete_feature = DeleteFeature.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
