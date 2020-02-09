import datetime

from django.db.models import Count, Sum, Case, When
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

        # TODO: Using timedelta is not accurate because it does not
        # take leap years into consideration. Consider using the
        # dateutil.relativedelta module instead.
        queryset = Household.objects.annotate(
            household_income=Sum('members__annual_income'),
            spouse_count=Count(Case(When(members__spouse__isnull=False, then=1))),
        )

        # Filters based on aggregate household income
        household_income_above = self.request.query_params.get('household_income_above')
        if household_income_above:
            queryset.filter(household_income__gt=household_income_above)
        household_income_below = self.request.query_params.get('household_income_below')
        if household_income_below:
            queryset.filter(household_income__lt=household_income_below)

        # Filters based on members' age
        members_age_above = self.request.query_params.get('members_age_above')
        if members_age_above:
            queryset.filter(Count(Case(When(members__dob__lt=datetime.date.today() - datetime.timedelta(days=members_age_above * 365)))))
        members_age_below = self.request.query_params.get('members_age_below')
        if members_age_below:
            queryset.filter(Count(Case(When(members__dob__gt=datetime.date.today() - datetime.timedelta(days=members_age_below * 365)))))

        # FIXME: This uses a simplistic filtering method of checking
        # if spouses exists in household but does not check if they
        # are related to one another.
        has_spouse = self.request.query_params.get('has_spouse')
        if has_spouse:
            queryset.filter(spouse_count__gte=2)

        return queryset
