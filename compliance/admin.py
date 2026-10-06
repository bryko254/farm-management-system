from django.contrib import admin

from .models import Certification


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuing_body', 'expiry_date', 'owner')
    search_fields = ('name', 'issuing_body')
