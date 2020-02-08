from rest_framework import viewsets

from govgrant.api.models import Household
from govgrant.api.serializers import HouseholdSerializer


class HouseholdViewSet(viewsets.ModelViewSet):
    """API endpoint for Household resource"""
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer
