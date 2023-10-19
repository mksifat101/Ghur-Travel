from django.db import models
from customer.models import *
from dashboard.models import *

# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer")
    book_type = models.CharField(max_length=100)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE, null=True, blank=True, related_name="room")
    flight = models.ForeignKey(FlightBooking, on_delete=models.CASCADE, null=True, blank=True, related_name="flight")
    from_date = models.DateField()
    to_date = models.DateField()
    adult = models.CharField(max_length=10)
    child = models.CharField(max_length=10)
    payment = models.BooleanField(default=False, null=True, blank=True)
    price = models.IntegerField()
    cancel = models.BooleanField(default=False, null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user.first_name