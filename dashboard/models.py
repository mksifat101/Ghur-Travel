from django.db import models
from django.urls.base import reverse
from django.template.defaultfilters import slugify
from partner.models import Partnar
from customer.models import Customer


class TopDestination(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(
        upload_to='topdestination/', null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('top_destination', kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Destination(models.Model):
    top = models.ForeignKey(TopDestination, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    image = models.ImageField(
        upload_to='destination/', null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('destination', kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class NewsCategory(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('categories', kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class News(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    categories = models.ForeignKey(NewsCategory, on_delete=models.CASCADE)
    thumbnails = models.ImageField(upload_to='news/', null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('news', kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Facilities_For_Hotels(models.Model):
    feciliti = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.feciliti


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    partner = models.ForeignKey(Partnar, on_delete=models.CASCADE)
    logo = models.ImageField(
        upload_to='partner/hotel_logo/', null=True, blank=True)
    thumbnails = models.ImageField(
        upload_to='partner/hotel_thumbnails/', null=True, blank=True)
    rate = models.IntegerField()
    details = models.TextField(null=True, blank=True)
    owner = models.CharField(max_length=100)
    min_booking_number = models.IntegerField()
    checkout = models.TimeField(null=True, blank=True)
    min_stay = models.IntegerField()
    address = models.CharField(max_length=255)
    mail = models.EmailField(max_length=150)
    mobile = models.CharField(max_length=20)
    website = models.CharField(max_length=255)
    booked = models.BooleanField(null=True, blank=True, default=False)
    promo_video = models.CharField(max_length=225, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('hotel', kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class HotelGallery(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='partner/hotel_gallery/')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.hotel.name


class Hotel_Facilities(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    feciliti = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.feciliti


class Facilities_For_Room(models.Model):
    feciliti = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.feciliti


class Rooms(models.Model):
    name = models.CharField(max_length=100)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)
    thumbnails = models.ImageField(
        upload_to='partner/room_thumbnails/', null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    number_of_room = models.IntegerField()
    number_of_bed = models.IntegerField()
    number_of_adult = models.IntegerField()
    number_of_children = models.IntegerField()
    room_footage = models.IntegerField()
    allow_cancel = models.BooleanField(null=True, blank=True, default=False)
    arrive = models.IntegerField()
    cancel_fee = models.IntegerField()
    price = models.IntegerField()
    before_booking = models.IntegerField()
    min_stay = models.IntegerField()
    booked = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('room', kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class RoomGallery(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='partner/room_gallery/')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.room.name


class RoomFacilities(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    feciliti = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.room.name


class RoomBooking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    adult = models.IntegerField()
    child = models.IntegerField()
    check_in = models.DateField()
    check_out = models.DateField()
    book_by = models.CharField(max_length=100)
    status = models.BooleanField(default=False, null=True, blank=True)
    payment = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.book_by


class Enquiry(models.Model):
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rate = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.customer.user.username


class FlightBooking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    price = models.IntegerField()
    destination = models.CharField(max_length=150)
    origin = models.CharField(max_length=150)
    cabin = models.CharField(max_length=150)
    adult = models.IntegerField(null=True, blank=True)
    child = models.IntegerField(null=True, blank=True)
    takeof = models.DateTimeField()
    land = models.DateTimeField()
    time = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    payment = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.customer.user.username



class Coupons(models.Model):
    codes = models.CharField(max_length=100)
    discount = models.IntegerField()
    active = models.DateField(null=True, blank=True)
    expiry = models.DateField(null=True, blank=True)
    is_price = models.BooleanField(default=False)
    status = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.codes
    


class Team(models.Model):
    name = models.CharField(max_length=255)
    postition = models.CharField(max_length=255)
    image = models.ImageField(upload_to='team/')
    facebook = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, null=True, blank=True)
    linkedin = models.CharField(max_length=255, null=True, blank=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.book_by