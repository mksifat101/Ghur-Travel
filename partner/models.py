from django.db import models
from authentication.models import *
from django.urls.base import reverse
from django.template.defaultfilters import slugify


class Partnar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=150, null=True, blank=True)
    tin_no = models.CharField(max_length=200, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    nid_front = models.ImageField(
        upload_to='partner/nid/', null=True, blank=True)
    nid_back = models.ImageField(
        upload_to='partner/nid/', null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user.first_name
