from django.contrib import admin
from .models import Hotel, Room, RoomType, Service
from unfold.admin import ModelAdmin

# Register your models here.
@admin.register(Hotel)
class HotelAdmin(ModelAdmin):
    pass

@admin.register(Room)
class RoomAdmin(ModelAdmin):
    pass

@admin.register(RoomType)
class RoomTypeAdmin(ModelAdmin):
    pass

@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    pass