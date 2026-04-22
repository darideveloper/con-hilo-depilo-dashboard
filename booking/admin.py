from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.widgets import UnfoldAdminColorInputWidget
from project.admin import ModelAdminUnfoldBase
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
class CompanyProfileAdmin(SingletonModelAdmin, ModelAdminUnfoldBase):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "brand_color":
            kwargs["widget"] = UnfoldAdminColorInputWidget
        return super().formfield_for_dbfield(db_field, **kwargs)

@admin.register(EventType)
class EventTypeAdmin(ModelAdminUnfoldBase):
    list_display = ("name", "payment_model", "allow_overlap")

@admin.register(Event)
class EventAdmin(ModelAdminUnfoldBase):
    list_display = ("name", "event_type", "price", "duration_minutes")
    list_filter = ("event_type",)

@admin.register(CompanyAvailability)
class CompanyAvailabilityAdmin(ModelAdminUnfoldBase):
    list_display = ("start_date", "end_date")

@admin.register(CompanyWeekdaySlot)
class CompanyWeekdaySlotAdmin(ModelAdminUnfoldBase):
    list_display = ("weekday", "start_time", "end_time")
    list_filter = ("weekday",)

@admin.register(CompanyDateOverride)
class CompanyDateOverrideAdmin(ModelAdminUnfoldBase):
    list_display = ("date", "is_available", "start_time", "end_time")

@admin.register(EventAvailability)
class EventAvailabilityAdmin(ModelAdminUnfoldBase):
    list_display = ("event", "start_date", "end_date")
    list_filter = ("event",)

@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(ModelAdminUnfoldBase):
    list_display = ("event", "weekday", "start_time", "end_time")
    list_filter = ("event", "weekday")

@admin.register(EventDateOverride)
class EventDateOverrideAdmin(ModelAdminUnfoldBase):
    list_display = ("event", "date", "is_available", "start_time", "end_time")
    list_filter = ("event",)

@admin.register(Booking)
class BookingAdmin(ModelAdminUnfoldBase):
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
