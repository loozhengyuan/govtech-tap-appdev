from collections import OrderedDict

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from govgrant.api.models import EnumModel, HousingType, Household, Gender, MaritalStatus, OccupationType, FamilyMember


# List of data fixtures
INITIAL_DATA_FIXTURES = "initial.json"
SAMPLE_DATA_FIXTURES = "sample.json"


class HousingTypeTestCase(TestCase):
    """TestCases for HousingType model"""

    def test_if_model_subclasses_enummodel(self):
        """Test if model subclasses EnumModel"""
        self.assertTrue(issubclass(HousingType, EnumModel))

    def test_if_dunder_str_method_returns_name_field(self):
        """Test if dunder str method returns name field"""
        name = "Hello World"
        e = HousingType.objects.create(name=name)
        self.assertEqual(str(e), name)


class HouseholdTestCase(TestCase):
    """TestCases for Household model"""

    # Load test fixtures
    fixtures = (
        INITIAL_DATA_FIXTURES,
    )

    def setUp(self):
        housing_type = HousingType.objects.get(pk=1)
        self.household = Household.objects.create(housing_type=housing_type)

    def test_if_dunder_str_method_returns_member_sequence(self):
        """Test if dunder str method returns member sequence"""
        self.assertEqual(str(self.household), "Household 1")


class GenderTestCase(TestCase):
    """TestCases for Gender model"""

    def test_if_model_subclasses_enummodel(self):
        """Test if model subclasses EnumModel"""
        self.assertTrue(issubclass(Gender, EnumModel))

    def test_if_dunder_str_method_returns_name_field(self):
        """Test if dunder str method returns name field"""
        name = "Hello World"
        e = Gender.objects.create(name=name)
        self.assertEqual(str(e), name)


class MaritalStatusTestCase(TestCase):
    """TestCases for MaritalStatus model"""

    def test_if_model_subclasses_enummodel(self):
        """Test if model subclasses EnumModel"""
        self.assertTrue(issubclass(MaritalStatus, EnumModel))

    def test_if_dunder_str_method_returns_name_field(self):
        """Test if dunder str method returns name field"""
        name = "Hello World"
        e = MaritalStatus.objects.create(name=name)
        self.assertEqual(str(e), name)


class OccupationTypeTestCase(TestCase):
    """TestCases for OccupationType model"""

    def test_if_model_subclasses_enummodel(self):
        """Test if model subclasses EnumModel"""
        self.assertTrue(issubclass(OccupationType, EnumModel))

    def test_if_dunder_str_method_returns_name_field(self):
        """Test if dunder str method returns name field"""
        name = "Hello World"
        e = OccupationType.objects.create(name=name)
        self.assertEqual(str(e), name)


class FamilyMemberTestCase(TestCase):
    """TestCases for FamilyMember model"""

    # Load test fixtures
    fixtures = (
        INITIAL_DATA_FIXTURES,
    )

    def setUp(self):
        self.name = "Tan Ah Kow"
        self.gender = Gender.objects.get(pk=1)
        self.marital_status = MaritalStatus.objects.get(pk=1)
        self.occupation_type = OccupationType.objects.get(pk=1)
        self.member = FamilyMember.objects.create(
            name=self.name,
            dob="1970-01-01",
            gender=self.gender,
            marital_status=self.marital_status,
            spouse=None,
            occupation_type=self.occupation_type,
            annual_income=10000,
            household=None,
        )

    def test_if_dunder_str_method_returns_name_field(self):
        """Test if dunder str method returns name field"""
        self.assertEqual(str(self.member), self.name)

    def test_if_save_method_updates_spouse_field_symmetrically(self):
        """Test if save method updates spouse field symmetrically"""

        # Create second spouse object (without saving)
        first = FamilyMember.objects.get(name=self.name)
        second = FamilyMember(
            name="Mavis Lim",
            dob="1970-01-01",
            gender=self.gender,
            marital_status=self.marital_status,
            spouse=first,  # Instance of the first spouse
            occupation_type=self.occupation_type,
            annual_income=10000,
            household=None,
        )

        # Assert that first spouse field is empty before calling
        # the save method
        self.assertEqual(first.spouse, None)

        # Assert that both spouses have the spouse field filled
        # after calling the save method
        second.save()
        self.assertEqual(first.spouse, second)
        self.assertEqual(second.spouse, first)


class HouseholdEndpointTestCase(APITestCase):
    """TestCases for /household/ endpoint"""

    # Load test fixtures
    fixtures = (
        INITIAL_DATA_FIXTURES,
    )

    def test_if_http_post_request_creates_a_household(self):
        """Test if HTTP POST request creates a household"""

        # Create data payload
        data = {
            "housing_type": "Landed",
        }
        expected = {
            "id": 1,
            "housing_type": "Landed",
            "members": [],
        }

        # Execute API call
        response = self.client.post(
            path="/households/",
            data=data,
            format="json",
        )

        # Assert API response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected)

    def test_if_http_get_request_lists_all_households(self):
        """Test if HTTP GET request lists all households"""

        # Create sample data
        housing_type = HousingType.objects.get(name="Landed")
        Household.objects.create(
            housing_type=housing_type,
        )
        expected = [
            OrderedDict(
                {
                    "id": 1,
                    "housing_type": "Landed",
                    "members": [],
                }
            ),
        ]

        # Execute API call
        response = self.client.get(
            path="/households/",
            format="json",
        )

        # Assert API response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_if_http_patch_request_adds_family_member_to_a_household(self):
        """Test if HTTP PATCH request adds family member to a household"""

        # Create a single Household object first
        housing_type = HousingType.objects.get(name="Landed")
        Household.objects.create(
            housing_type=housing_type,
        )

        # TODO: Assert that a member does not already exist
        # TODO: Assert operation appends instead of overwrite

        # Create data payload
        data = {
            "members": [
                {
                    "name": "Tan Ah Kow",
                    "gender": "Male",
                    "marital_status": "Single",
                    "spouse": None,
                    "occupation_type": "Employed",
                    "annual_income": 48000,
                    "dob": "2019-10-01",
                },
            ]
        }
        expected = {
            "id": 1,                                # Added in response
            "housing_type": "Landed",               # Added in response
            "members": [
                {
                    "id": 1,                        # Added in response
                    "name": "Tan Ah Kow",
                    "gender": "Male",
                    "marital_status": "Single",
                    "spouse": None,
                    "occupation_type": "Employed",
                    "annual_income": 48000,
                    "dob": "2019-10-01",
                    "household": 1,                 # Added in response
                },
            ]
        }

        # Execute API call
        response = self.client.patch(
            path="/households/1/",
            data=data,
            format="json",
        )

        # Assert API response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_if_http_get_request_lists_all_members_of_a_household(self):
        """Test if HTTP GET request lists all members of a household"""

        # Create a single Household object and associated FamilyMember objects
        housing_type = HousingType.objects.get(name="Landed")
        household = Household.objects.create(
            housing_type=housing_type,
        )
        gender = Gender.objects.get(name="Male")
        marital_status = MaritalStatus.objects.get(name="Single")
        occupation_type = OccupationType.objects.get(name="Employed")
        FamilyMember.objects.create(
            name="Tan Ah Kow",
            dob="2019-10-01",
            gender=gender,
            marital_status=marital_status,
            spouse=None,
            occupation_type=occupation_type,
            annual_income=48000,
            household=household,
        )

        # Create data payload
        expected = {
            "id": 1,
            "housing_type": "Landed",
            "members": [
                {
                    "id": 1,
                    "name": "Tan Ah Kow",
                    "gender": "Male",
                    "marital_status": "Single",
                    "spouse": None,
                    "occupation_type": "Employed",
                    "annual_income": 48000,
                    "dob": "2019-10-01",
                    "household": 1,
                },
            ]
        }

        # Execute API call
        response = self.client.get(
            path="/households/1/",
            format="json",
        )

        # Assert API response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)
