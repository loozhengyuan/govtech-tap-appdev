import datetime

from django.db.models import Count, Sum, Q, Case, When
from rest_framework import viewsets

from govgrant.api.models import Household
from govgrant.api.serializers import HouseholdSerializer


class HouseholdViewSet(viewsets.ModelViewSet):
    """API endpoint for Household resource"""
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer

    def get_queryset(self):
        """
        Optionally filters eligble households against query
        parameters given in the request URL.

        This allows the end-user to filter the list of households
        and match those that qualifies for a specific grant based
        on the qualifying criteria.
        """

        # Filter keys
        household_income_above = self.request.query_params.get('household_income_above', 0)
        household_income_below = self.request.query_params.get('household_income_below', 2147024809)
        spouse_count_at_least = self.request.query_params.get('spouse_count_at_least', 0)
        members_age_above = self.request.query_params.get('members_age_above', 0)
        members_age_below = self.request.query_params.get('members_age_below', 150)

        # TODO: Using timedelta is not accurate because it does not
        # take leap years into consideration. Consider using the
        # dateutil.relativedelta module instead.
        queryset = Household.objects.annotate(
            household_income=Sum('members__annual_income'),
            spouse_count=Count(Case(When(members__spouse__isnull=False, then=1))),
            members_age_above=Count('members', filter=Q(members__dob__lt=datetime.date.today() - datetime.timedelta(days=members_age_above * 365))),
            members_age_below=Count('members', filter=Q(members__dob__gt=datetime.date.today() - datetime.timedelta(days=members_age_below * 365))),
        ).filter(
            household_income__gt=household_income_above,
            household_income__lt=household_income_below,
            spouse_count__gte=spouse_count_at_least,
            members_age_above__gt=0,
            members_age_below__gt=0,
        )
        return queryset
