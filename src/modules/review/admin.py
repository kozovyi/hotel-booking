from django.contrib import admin
from .models import  Review
from unfold.admin import ModelAdmin

# Register your models here.
@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    pass
