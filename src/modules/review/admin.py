from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Review


# Register your models here.
@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    pass
