from django.contrib import admin
from .models import Booking, Payment
from unfold.admin import ModelAdmin

# Register your models here.
@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    pass

@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    pass