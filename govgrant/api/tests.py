import json

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
        self.assertEqual(json.loads(response.content), expected)

    def test_if_http_get_request_lists_all_households(self):
        """Test if HTTP GET request lists all households"""

        # Create sample data
        housing_type = HousingType.objects.get(name="Landed")
        Household.objects.create(
            housing_type=housing_type,
        )
        expected = [
            {
                "id": 1,
                "housing_type": "Landed",
                "members": [],
            },
        ]

        # Execute API call
        response = self.client.get(
            path="/households/",
            format="json",
        )

        # Assert API response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), expected)

    def test_if_http_post_request_adds_family_member_to_a_household(self):
        """Test if HTTP POST request adds family member to a household"""

        # Create a single Household object first
        housing_type = HousingType.objects.get(name="Landed")
        Household.objects.create(
            housing_type=housing_type,
        )

        # TODO: Assert that a member does not already exist
        # TODO: Assert operation appends instead of overwrite

        # Create data payload
        data = {
            "name": "Tan Ah Kow",
            "gender": "Male",
            "marital_status": "Single",
            "spouse": None,
            "occupation_type": "Employed",
            "annual_income": 48000,
            "dob": "2019-10-01",
        }
        expected = {
            "id": 1,                        # Added in response
            "name": "Tan Ah Kow",
            "gender": "Male",
            "marital_status": "Single",
            "spouse": None,
            "occupation_type": "Employed",
            "annual_income": 48000,
            "dob": "2019-10-01",
            "household": 1,                 # Added in response
        }

        # Execute API call
        response = self.client.post(
            path="/households/1/add_member/",
            data=data,
            format="json",
        )

        # Assert API response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), expected)

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
        self.assertEqual(json.loads(response.content), expected)

    def test_if_http_delete_request_deletes_a_household_and_its_related_members(self):
        """Test if HTTP DELETE request deletes a household and its related members"""

        # Create a single Household object and associated FamilyMember objects
        housing_type = HousingType.objects.get(name="Landed")
        household = Household.objects.create(
            housing_type=housing_type,
        )
        gender = Gender.objects.get(name="Male")
        marital_status = MaritalStatus.objects.get(name="Single")
        occupation_type = OccupationType.objects.get(name="Employed")
        member = FamilyMember.objects.create(
            name="Tan Ah Kow",
            dob="2019-10-01",
            gender=gender,
            marital_status=marital_status,
            spouse=None,
            occupation_type=occupation_type,
            annual_income=48000,
            household=household,
        )

        # Assert that household and member exists
        self.assertNotEqual(household, None)
        self.assertNotEqual(member, None)
        self.assertEqual(household.members.count(), 1)

        # Execute API call
        response = self.client.delete(
            path=f"/households/{household.pk}/",
            format="json",
        )

        # Assert API response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Assert that household and member no longer exists
        with self.assertRaises(Household.DoesNotExist):
            Household.objects.get(pk=household.pk)
        with self.assertRaises(FamilyMember.DoesNotExist):
            FamilyMember.objects.get(pk=member.pk)

    def test_if_http_delete_request_deletes_a_member_from_its_household(self):
        """Test if HTTP DELETE request deletes a member from its household"""

        # Create a single Household object first
        housing_type = HousingType.objects.get(name="Landed")
        household = Household.objects.create(
            housing_type=housing_type,
        )

        # Create data payload
        data = {
            "name": "Tan Ah Kow",
            "gender": "Male",
            "marital_status": "Single",
            "spouse": None,
            "occupation_type": "Employed",
            "annual_income": 48000,
            "dob": "2019-10-01",
        }

        # Add member
        response = self.client.post(
            path=f"/households/{household.pk}/add_member/",
            data=data,
            format="json",
        )

        # Assert that household and member exists
        household.refresh_from_db()  # Sync obj with db
        self.assertNotEqual(household, None)
        self.assertEqual(household.members.count(), 1)

        # Execute API call
        response = self.client.delete(
            path=f"/households/{household.pk}/remove_member/",
            data={"name": data["name"]},  # Only 'name' key is needed
            format="json",
        )

        # Create expected data payload
        expected = {
            "id": 1,
            "housing_type": "Landed",
            "members": []
        }

        # Assert API response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), expected)

        # Assert that household exists but member does not
        household.refresh_from_db()  # Sync obj with db
        self.assertNotEqual(household, None)
        self.assertEqual(household.members.count(), 0)

    def test_if_http_delete_request_fails_without_name_key(self):
        """Test if HTTP DELETE request fails without name key"""

        # Create a single Household object first
        housing_type = HousingType.objects.get(name="Landed")
        household = Household.objects.create(
            housing_type=housing_type,
        )

        # Execute API call
        response = self.client.delete(
            path=f"/households/{household.pk}/remove_member/",
            data={},  # 'name' key missing in api request
            format="json",
        )

        # Create expected data payload
        expected = {
            "name": "field is required"
        }

        # Assert API response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), expected)

    def test_if_http_delete_request_fails_if_member_not_found_in_household(self):
        """Test if HTTP DELETE request fails if member not found in household"""

        # Create a single Household object first
        housing_type = HousingType.objects.get(name="Landed")
        household = Household.objects.create(
            housing_type=housing_type,
        )

        # Assert that household exists but member does not
        self.assertNotEqual(household, None)
        self.assertEqual(household.members.count(), 0)

        # Execute API call
        name = "David Copperfield"
        response = self.client.delete(
            path=f"/households/{household.pk}/remove_member/",
            data={"name": name},  # nonexistent member
            format="json",
        )

        # Create expected data payload
        expected = {
            "name": f"could not find '{name}' in current household"
        }

        # Assert API response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), expected)


class GrantEligibilityTestCase(APITestCase):
    """TestCases for filtering Household resource using query parameters"""

    # Load test fixtures
    fixtures = (
        INITIAL_DATA_FIXTURES,
        SAMPLE_DATA_FIXTURES,
    )

    # TODO: datetime.date.today() in views.py needs to be mocked so
    # that the tests remain consistent regardless of the current date

    def test_if_endpoint_returns_eligible_households_for_student_encouragement_bonus(self):
        """Test if endpoint returns eligible households for Student Encouragement Bonus"""

        # Create query params
        params = {
            "max_age": 16,
            "max_income": 150000,
        }
        expected = [
            {
                "id": 1,
                "housing_type": "Landed",
                "members": [
                    {
                        "id": 1,
                        "name": "Paul Tan",
                        "gender": "Male",
                        "marital_status": "Single",
                        "spouse": None,
                        "occupation_type": "Employed",
                        "annual_income": 10000,
                        "dob": "2010-01-01",
                        "household": 1,
                    },
                ],
            },
        ]

        # Execute API call
        response = self.client.get(
            path="/households/",
            data=params,
            format="json",
        )

        # Assert API response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), expected)

    def test_if_endpoint_returns_eligible_households_for_family_togetherness_scheme(self):
        """Test if endpoint returns eligible households for Family Togetherness Scheme"""

        # Create query params
        params = {
            "with_spouse": True,
            "max_age": 18,
        }
        expected = [
            {
                "id": 2,
                "housing_type": "HDB",
                "members": [
                    {
                        "id": 2,
                        "name": "John Doe",
                        "gender": "Male",
                        "marital_status": "Married",
                        "spouse": "Mary Doe",
                        "occupation_type": "Employed",
                        "annual_income": 88000,
                        "dob": "1980-01-01",
                        "household": 2,
                    },
                    {
                        "id": 3,
                        "name": "Mary Doe",
                        "gender": "Female",
                        "marital_status": "Married",
                        "spouse": "John Doe",
                        "occupation_type": "Employed",
                        "annual_income": 88000,
                        "dob": "2010-01-01",
                        "household": 2,
                    },
                ],
            },
        ]

        # Execute API call
        response = self.client.get(
            path="/households/",
            data=params,
            format="json",
        )

        # Assert API response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), expected)

    def test_if_endpoint_returns_eligible_households_for_elder_bonus(self):
        """Test if endpoint returns eligible households for Elder Bonus"""

        # Create query params
        params = {
            "housing_type": "hdb",  # Case insensitive
            "min_age": 50,
        }
        expected = [
            {
                "id": 3,
                "housing_type": "HDB",
                "members": [
                    {
                        "id": 4,
                        "name": "Tan Ah Kow",
                        "gender": "Male",
                        "marital_status": "Single",
                        "spouse": None,
                        "occupation_type": "Employed",
                        "annual_income": 10000,
                        "dob": "1960-01-01",
                        "household": 3,
                    },
                ],
            },
        ]

        # Execute API call
        response = self.client.get(
            path="/households/",
            data=params,
            format="json",
        )

        # Assert API response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), expected)

    def test_if_endpoint_returns_eligible_households_for_baby_sunshine_grant(self):
        """Test if endpoint returns eligible households for Baby Sunshine Grant"""

        # Create query params
        params = {
            "max_age": 5,
        }
        expected = [
            {
                "id": 4,
                "housing_type": "HDB",
                "members": [
                    {
                        "id": 5,
                        "name": "Linus Torvalds",
                        "gender": "Male",
                        "marital_status": "Single",
                        "spouse": None,
                        "occupation_type": "Employed",
                        "annual_income": 200000,
                        "dob": "2019-01-01",
                        "household": 4,
                    },
                ],
            },
        ]

        # Execute API call
        response = self.client.get(
            path="/households/",
            data=params,
            format="json",
        )

        # Assert API response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), expected)

    def test_if_endpoint_returns_eligible_households_for_yolo_gst_grant(self):
        """Test if endpoint returns eligible households for YOLO GST Grant"""

        # Create query params
        params = {
            "housing_type": "hdb",  # Case insensitive
            "max_income": 100000,
        }
        expected = [
            {
                "id": 3,
                "housing_type": "HDB",
                "members": [
                    {
                        "id": 4,
                        "name": "Tan Ah Kow",
                        "gender": "Male",
                        "marital_status": "Single",
                        "spouse": None,
                        "occupation_type": "Employed",
                        "annual_income": 10000,
                        "dob": "1960-01-01",
                        "household": 3,
                    },
                ],
            },
        ]

        # Execute API call
        response = self.client.get(
            path="/households/",
            data=params,
            format="json",
        )

        # Assert API response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), expected)
