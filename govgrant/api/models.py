from django.db import models


class EnumModel(models.Model):
    """
    Abstract base class for enumerated types

    This base class is suitable for any type of
    models where ``models.TextChoices`` or
    ``models.IntegerChoices`` is a good fit.
    """

    name = models.CharField(max_length=255, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class HousingType(EnumModel):
    """Represents the type of a physical housing unit"""
    pass


class Household(models.Model):
    """Represents a single physical housing unit"""

    housing_type = models.ForeignKey(HousingType, on_delete=models.PROTECT)

    def __str__(self):
        return f"Household {self.pk}"


class Gender(EnumModel):
    """Represents the gender orientation of an individual"""
    pass


class MaritalStatus(EnumModel):
    """Represents the marital status of an individual"""
    pass


class OccupationType(EnumModel):
    """Represents the occupation type of an individual"""
    pass


class FamilyMember(models.Model):
    """Represents a single member of a family"""

    name = models.CharField(max_length=255, unique=True)
    dob = models.DateField()
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    marital_status = models.ForeignKey(MaritalStatus, on_delete=models.PROTECT)
    spouse = models.OneToOneField("self", on_delete=models.SET_NULL, null=True)
    occupation_type = models.ForeignKey(OccupationType, on_delete=models.PROTECT)
    annual_income = models.PositiveIntegerField()
    household = models.ForeignKey(Household, related_name="members", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Symmetrically mirror self.spouse relationship between
        two family members.

        This method extends the save() method in the superclass
        by also updating the spouse's 'spouse' field as itself.

        Reference:
            https://code.djangoproject.com/ticket/7689
        """

        # FIXME: The following behaviour does not seem to
        # work on the Model.objects.create() method. Not that
        # it matters for now, but this should be reviewed.
        super().save(*args, **kwargs)
        if self.spouse and not self.spouse.spouse:
            self.spouse.spouse = self
            self.spouse.save()
