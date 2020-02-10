from rest_framework import serializers

from govgrant.api.models import HousingType, Household, Gender, MaritalStatus, OccupationType, FamilyMember


class FamilyMemberSerializer(serializers.ModelSerializer):
    gender = serializers.SlugRelatedField(slug_field="name", queryset=Gender.objects.all())
    marital_status = serializers.SlugRelatedField(slug_field="name", queryset=MaritalStatus.objects.all())
    occupation_type = serializers.SlugRelatedField(slug_field="name", queryset=OccupationType.objects.all())
    spouse = serializers.SlugRelatedField(slug_field="name", queryset=FamilyMember.objects.all(), required=False, allow_null=True)

    class Meta:
        model = FamilyMember
        fields = (
            "id",
            "name",
            "gender",
            "marital_status",
            "spouse",
            "occupation_type",
            "annual_income",
            "dob",
            "household",
        )


class HouseholdSerializer(serializers.ModelSerializer):
    housing_type = serializers.SlugRelatedField(slug_field="name", queryset=HousingType.objects.all())
    members = FamilyMemberSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Household
        fields = (
            "id",
            "housing_type",
            "members",
        )
