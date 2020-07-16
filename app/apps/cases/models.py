from django.db import models
from utils.api_queries_bag import do_bag_search_id


class Address(models.Model):
    bag_id = models.CharField(max_length=255, null=False, unique=True)
    street_name = models.CharField(max_length=255, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    suffix_letter = models.CharField(max_length=1, null=True, blank=True)
    suffix = models.CharField(max_length=4, null=True, blank=True)
    postal_code = models.CharField(max_length=7, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    @property
    def full_address(self):
        full_address = f"{self.street_name} {self.number}"
        if self.suffix or self.suffix_letter:
            full_address = f"{full_address}-{self.suffix}{self.suffix_letter}"

        full_address = f"{full_address}, {self.postal_code}"

        return full_address

    def __str__(self):
        if self.street_name:
            return (
                f"{self.street_name}"
                f" {self.number}{self.suffix_letter}{self.suffix},"
                f" {self.postal_code}"
            )
        return self.bag_id

    def get(bag_id):
        return Address.objects.get_or_create(bag_id=bag_id)[0]

    def save(self, *args, **kwargs):
        bag_data = do_bag_search_id(self.bag_id)
        result = bag_data.get("results", [])[0]

        self.postal_code = result.get("postcode", "")
        self.street_name = result.get("straatnaam", "")
        self.number = result.get("huisnummer", "")
        self.suffix_letter = result.get("bag_huisletter", "")
        self.suffix = result.get("bag_toevoeging", "")

        return super().save(*args, **kwargs)


class CaseType(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)

    def get(name):
        return CaseType.objects.get_or_create(name=name)[0]

    def __str__(self):
        return self.name


class Case(models.Model):
    class Meta:
        ordering = ["start_date"]

    identification = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    case_type = models.ForeignKey(
        to=CaseType, null=False, on_delete=models.CASCADE, related_name="cases"
    )
    address = models.ForeignKey(
        to=Address, null=False, on_delete=models.CASCADE, related_name="cases"
    )

    def get(identification):
        return Case.objects.get_or_create(identification=identification)[0]

    def __str__(self):
        if self.identification:
            return self.identification
        return ""


class StateType(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)

    def get(name):
        return StateType.objects.get_or_create(name=name)[0]

    def __str__(self):
        return self.name


class State(models.Model):
    state_type = models.ForeignKey(
        to=StateType, null=False, on_delete=models.CASCADE, related_name="states"
    )
    case = models.ForeignKey(
        to=Case, null=False, on_delete=models.CASCADE, related_name="states"
    )
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    gauge_date = models.DateField(null=True)

    def __str__(self):
        return (
            f"{self.state_type}, {self.case.address}, {self.start_date} {self.end_date}"
            f" {self.gauge_date}"
        )
