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

        # Construct filters
        filters = {}

        # Filters based on aggregate household income
        min_income = self.request.query_params.get('min_income')
        if min_income:
            filters["household_income__gt"] = min_income
        max_income = self.request.query_params.get('max_income')
        if max_income:
            filters["household_income__lt"] = max_income

        # Filters based on members' age
        min_age = self.request.query_params.get('min_age')
        if min_age:
            filters["members__dob__lt"] = datetime.date.today() - datetime.timedelta(days=int(min_age) * 365)
        max_age = self.request.query_params.get('max_age')
        if max_age:
            filters["members__dob__gt"] = datetime.date.today() - datetime.timedelta(days=int(max_age) * 365)

        # TODO: Consider using a better logic that checks
        # if the spouse is related to one another within
        # the same household.
        if self.request.query_params.get('with_spouse'):
            filters["spouse_count__gte"] = 2

        # TODO: Using timedelta is not accurate because it does not
        # take leap years into consideration. Consider using the
        # dateutil.relativedelta module instead.
        queryset = Household.objects.annotate(
            household_income=Sum('members__annual_income'),
            spouse_count=Count(Case(When(members__spouse__isnull=False, then=1))),
        ).filter(**filters)

        return queryset
