from django.test import TestCase

from govgrant.api.models import EnumModel, HousingType, Household, Gender, MaritalStatus, OccupationType, FamilyMember


# List of initial data fixtures
INITIAL_DATA_FIXTURES = (
    "initial.json",
)


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
    fixtures = INITIAL_DATA_FIXTURES

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
    fixtures = INITIAL_DATA_FIXTURES

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
