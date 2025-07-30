from django.contrib import admin
from .models import Spot

@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "rating", "created_at")
    search_fields = ("name",)