from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, CheckboxSelectMultiple

from main.models.housing_group import HousingGroup
from main.models.job import Job
from main.models.transportation_method import TransportationMethod


class AttendanceProfile(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)

    user = models.ForeignKey(User)
    year = models.IntegerField()

    housing_type_preference = models.CharField(
        max_length=HousingGroup.HOUSING_TYPE_LENGTH,
        choices=HousingGroup.HOUSING_CHOICES,
        blank=True,
        null=True
    )
    housing_group = models.ForeignKey(HousingGroup, related_name='residents', null=True, blank=True)
    to_transportation_method = models.ForeignKey(TransportationMethod,
                                                 related_name='to_attendees',
                                                 null=True,
                                                 blank=True)
    from_transportation_method = models.ForeignKey(TransportationMethod,
                                                   related_name='from_attendees',
                                                   null=True,
                                                   blank=True)

    EARLY_ARRIVAL_CHOICES = (
        ('wednesday1', 'Wednesday (Early)'),
        ('thursday1', 'Thursday (Early)'),
        ('friday1', 'Friday (Early)'),
        ('saturday', 'Saturday (Early)'),
    )
    ARRIVAL_CHOICES = EARLY_ARRIVAL_CHOICES + (
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday2', 'Wednesday'),
        ('thursday2', 'Thursday'),
        ('friday2', 'Friday'),
    )
    arrival_date = models.CharField(
        max_length=16,
        choices=ARRIVAL_CHOICES,
        blank=True,
        null=True
    )

    LATE_DEPARTURE_CHOICES = (
        ('monday', 'Monday (Late Crew)'),
        ('tuesday', 'Tuesday (Late Crew)'),
    )
    DEPARTURE_CHOICES = (
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday (Man Burn)'),
        ('sunday', 'Sunday (Temple Burn)'),
    ) + LATE_DEPARTURE_CHOICES
    departure_date = models.CharField(
        max_length=16,
        choices=DEPARTURE_CHOICES,
        blank=True,
        null=True
    )

    has_early_pass = models.NullBooleanField(blank=True)
    has_ticket = models.NullBooleanField(blank=True)
    has_vehicle_pass = models.NullBooleanField(blank=True)
    paid_dues = models.BooleanField(default=False)

    bicycle_status = models.CharField(
        max_length=10,
        choices=(
            ('rent', 'Renting'),
            ('have', 'Have'),
            ('need', 'Need'),
        ),
        null=True,
        blank=True
    )

    job_preferences = models.ManyToManyField(Job, blank=True)
    shift_time_preference = models.CharField(
        max_length=10,
        choices=(
            ('day', 'Day shifts'),
            ('night', 'Evening shifts'),
            ('nopref', 'No preference'),
        ),
        null=True,
        blank=True
    )
    shift_day_preference = models.CharField(
        max_length=10,
        choices=(
            ('sameday', 'All same day'),
            ('b2b', 'Back to back days'),
            ('spread', 'Spread out'),
            ('nopref', 'No preference'),
        ),
        null=True,
        blank=True
    )

    @property
    def arrives_early(self) -> bool:
        return dict(AttendanceProfile.EARLY_ARRIVAL_CHOICES).get(self.arrival_date, False)

    @property
    def departs_late(self) -> bool:
        return dict(AttendanceProfile.LATE_DEPARTURE_CHOICES).get(self.departure_date, False)

    def __str__(self):
        return '{}[{}]'.format(self.user, self.year)


class AttendanceProfileForm(ModelForm):
    class Meta:
        model = AttendanceProfile
        fields = [
            'arrival_date',
            'departure_date',
            'to_transportation_method',
            'from_transportation_method',
            'has_early_pass',
            'has_ticket',
            'has_vehicle_pass',
            'housing_type_preference',
            'bicycle_status',
            'job_preferences',
            'shift_time_preference',
            'shift_day_preference',
        ]

        labels = {
            'arrival_date': 'What day do you plan to arrive?',
            'departure_date': 'What day do you plan to leave?',
            'to_transportation_method': 'How are you planning on getting there?',
            'from_transportation_method': 'How are you planning on leaving?',
            'has_early_pass': 'Do you have any early passes?',
            'has_ticket': 'Do you have any tickets yet?',
            'has_vehicle_pass': 'Do you have a vehicle pass?',
            'housing_type_preference': 'Where are you planning on sleeping?',
            'bicycle_status': 'What\'s your bicycle plan?',
            'job_preferences': 'Are there specific on-playa jobs you\'re interested in?',
            'shift_time_preference': 'Do you prefer daytime or evening shifts?',
            'shift_day_preference': 'How would you like to spread your shifts?',
        }

        widgets = {
            'job_preferences': CheckboxSelectMultiple(),
        }

    def to_transportation_method_description(self) -> str:
        if self.instance is None:
            return ''
        if not self.instance.to_transportation_method:
            return ''
        return self.instance.to_transportation_method.description

    def from_transportation_method_description(self) -> str:
        if self.instance is None:
            return ''
        if not self.instance.from_transportation_method:
            return ''
        if self.instance.from_transportation_method.description == self.to_transportation_method_description():
            return ''
        return self.instance.from_transportation_method.description

    def bicycle_description(self) -> str:
        if self.instance is None:
            return ''
        if not self.instance.bicycle_status:
            return ''
        if self.instance.bicycle_status == 'rent':
            return '''Playa Bike Repair (PBR) is a great place to get your burner bike.

            Reserve your bike at https://playabikerepair.com'''
        return ''
