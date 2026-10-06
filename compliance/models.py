from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

EXPIRY_WARNING_DAYS = 30


class Certification(models.Model):
    name = models.CharField(max_length=150)
    issuing_body = models.CharField(max_length=150)
    reference_number = models.CharField(max_length=100, blank=True)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True, help_text='Leave blank if it does not expire')
    notes = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['expiry_date', 'name']

    def __str__(self):
        return self.name

    @property
    def status(self):
        if not self.expiry_date:
            return 'No expiry'
        today = timezone.localdate()
        if self.expiry_date < today:
            return 'Expired'
        if self.expiry_date <= today + timedelta(days=EXPIRY_WARNING_DAYS):
            return 'Expiring soon'
        return 'Valid'
