from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Booking


# Register your models here.
@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    pass
