from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from solo.admin import SingletonModelAdmin
from .models import (
    CompanyProfile,
    EventType,
    Event,
    CompanyAvailability,
    CompanyWeekdaySlot,
    CompanyDateOverride,
    EventAvailability,
    AvailabilitySlot,
    EventDateOverride,
    Booking,
)

@admin.register(CompanyProfile)
class CompanyProfileAdmin(SingletonModelAdmin, ModelAdmin):
    pass

@admin.register(EventType)
class EventTypeAdmin(ModelAdmin):
    list_display = ("name", "payment_model", "allow_overlap")

@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_display = ("name", "event_type", "price", "duration_minutes")
    list_filter = ("event_type",)

@admin.register(CompanyAvailability)
class CompanyAvailabilityAdmin(ModelAdmin):
    list_display = ("start_date", "end_date")

@admin.register(CompanyWeekdaySlot)
class CompanyWeekdaySlotAdmin(ModelAdmin):
    list_display = ("weekday", "start_time", "end_time")
    list_filter = ("weekday",)

@admin.register(CompanyDateOverride)
class CompanyDateOverrideAdmin(ModelAdmin):
    list_display = ("date", "is_available", "start_time", "end_time")

@admin.register(EventAvailability)
class EventAvailabilityAdmin(ModelAdmin):
    list_display = ("event", "start_date", "end_date")
    list_filter = ("event",)

@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(ModelAdmin):
    list_display = ("event", "weekday", "start_time", "end_time")
    list_filter = ("event", "weekday")

@admin.register(EventDateOverride)
class EventDateOverrideAdmin(ModelAdmin):
    list_display = ("event", "date", "is_available", "start_time", "end_time")
    list_filter = ("event",)

@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    list_display = ("client_name", "start_time", "end_time", "status")
    list_filter = ("status", "start_time")
    search_fields = ("client_name", "client_email")
    filter_horizontal = ("services",)
    readonly_fields = ("end_time",)
    
    fieldsets = (
        (_("Client Information"), {
            "fields": ("client_name", "client_email", "client_phone")
        }),
        (_("Scheduling"), {
            "fields": ("start_time", "end_time", "status")
        }),
        (_("Services"), {
            "fields": ("services",)
        }),
        (_("Integrations"), {
            "fields": ("google_event_id", "stripe_payment_id"),
            "classes": ("collapse",)
        }),
    )
