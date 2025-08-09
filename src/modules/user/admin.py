from django.contrib import admin
from unfold.admin import ModelAdmin

from modules.user.models import User

# Register your models here.

@admin.register(User)
class UserAdmin(ModelAdmin):
    
    pass