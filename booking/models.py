from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel

# --- Abstract Bases ---

class BaseAvailabilityRange(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        abstract = True

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError(_("Start date cannot be after end date."))

class BaseAvailabilitySlot(models.Model):
    WEEKDAYS = [
        (0, _("Monday")),
        (1, _("Tuesday")),
        (2, _("Wednesday")),
        (3, _("Thursday")),
        (4, _("Friday")),
        (5, _("Saturday")),
        (6, _("Sunday")),
    ]
    weekday = models.IntegerField(choices=WEEKDAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        abstract = True

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError(_("Start time must be before end time."))

class BaseDateOverride(models.Model):
    date = models.DateField()
    is_available = models.BooleanField(default=False)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def clean(self):
        if self.is_available:
            if not self.start_time or not self.end_time:
                raise ValidationError(_("Start and end times are required if available."))
            if self.start_time >= self.end_time:
                raise ValidationError(_("Start time must be before end time."))

# --- Company Profile ---

class CompanyProfile(SingletonModel):
    brand_color = models.CharField(max_length=20, default="#682896")
    logo = models.ImageField(upload_to="branding/", null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    currency = models.CharField(max_length=10, default="EUR")

    def __str__(self):
        return str(_("Company Profile"))

    class Meta:
        verbose_name = _("Company Profile")

# --- Service Catalog ---

class EventType(models.Model):
    PAYMENT_MODELS = [
        ("PRE-PAID", _("Pre-paid")),
        ("POST-PAID", _("Post-paid")),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    payment_model = models.CharField(max_length=20, choices=PAYMENT_MODELS, default="POST-PAID")
    allow_overlap = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Event(models.Model):
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, related_name="events")
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.PositiveIntegerField()
    image = models.ImageField(upload_to="events/", null=True, blank=True)

    def __str__(self):
        return self.name

# --- Company Availability ---

class CompanyAvailability(BaseAvailabilityRange):
    class Meta:
        verbose_name_plural = _("Company Availabilities")

class CompanyWeekdaySlot(BaseAvailabilitySlot):
    class Meta:
        unique_together = ("weekday", "start_time", "end_time")

class CompanyDateOverride(BaseDateOverride):
    class Meta:
        verbose_name_plural = _("Company Date Overrides")

# --- Event Availability ---

class EventAvailability(BaseAvailabilityRange):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="availabilities")
    
    class Meta:
        verbose_name_plural = _("Event Availabilities")

class AvailabilitySlot(BaseAvailabilitySlot):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="slots")

    class Meta:
        unique_together = ("event", "weekday", "start_time", "end_time")

class EventDateOverride(BaseDateOverride):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="overrides")
    
    class Meta:
        verbose_name_plural = _("Event Date Overrides")

# --- Booking ---

class Booking(models.Model):
    STATUS_CHOICES = [
        ("PENDING", _("Pending")),
        ("CONFIRMED", _("Confirmed")),
        ("PAID", _("Paid")),
        ("CANCELLED", _("Cancelled")),
    ]
    services = models.ManyToManyField(Event, related_name="bookings")
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField(db_index=True, null=True, blank=True)
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING", db_index=True)
    google_event_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_payment_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.client_name} - {self.start_time}"

    class Meta:
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")

    def calculate_end_time(self):
        if not self.start_time:
            return None
        
        # We need to handle both new and existing instances
        # If it's new and hasn't been saved, services.all() will be empty
        total_duration = sum(event.duration_minutes for event in self.services.all())
        from datetime import timedelta
        return self.start_time + timedelta(minutes=total_duration)

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from datetime import timedelta

@receiver(m2m_changed, sender=Booking.services.through)
def update_booking_end_time(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        total_duration = sum(event.duration_minutes for event in instance.services.all())
        instance.end_time = instance.start_time + timedelta(minutes=total_duration)
        instance.save(update_fields=["end_time"])
