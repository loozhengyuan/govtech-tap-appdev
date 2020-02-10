import datetime

from django.db.models import Count, Sum, Case, When
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from govgrant.api.models import Household, FamilyMember
from govgrant.api.serializers import HouseholdSerializer, FamilyMemberSerializer


class HouseholdViewSet(viewsets.ModelViewSet):
    """API endpoint for Household resource"""
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """Custom action for adding member to household"""

        # Patch household.pk to current member object
        household = self.get_object()
        request.data["household"] = household.pk

        # Validate request
        serializer = FamilyMemberSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Commit changes to return
        # TODO: Return household or just member instance?
        # TODO: Consider using status.HTTP_201_CREATED?
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def remove_member(self, request, pk=None):
        """Custom action for removing member from household"""

        # Get required key in request.data
        name = request.data.get("name")
        if not name:
            data = {
                "name": "field is required"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        # Delete object and return Response
        # TODO: Consider a better way to destroy model instance.
        # This is only done because the Serializer cannot successfully
        # validate this request object and because the pk of the member
        # cannot be derived from the url route.
        # TODO: Catch FamilyMember.DoesNotExist exception
        member = FamilyMember.objects.get(name=name)
        member.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

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

        # Filters based on housing type
        # NOTE: Uses case insensitive match
        housing_type = self.request.query_params.get('housing_type')
        if housing_type:
            filters["housing_type__name__iexact"] = housing_type

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
