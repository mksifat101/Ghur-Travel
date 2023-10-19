from django.db import models
from authentication.models import User


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    father = models.CharField(max_length=255, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='customer/', null=True, blank=True)
    passport = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.CharField(max_length=150, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    nid = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=150, null=True, blank=True)
    state = models.CharField(max_length=150, null=True, blank=True)
    zip = models.CharField(max_length=150, null=True, blank=True)
    country = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user.first_name


