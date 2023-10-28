import datetime
from datetime import date
from django.shortcuts import render, redirect
from dashboard.models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from authentication.decorators import partnar_required
from django.db.models import Sum


@partnar_required
def partner_dashboard(request):
    today = date.today()
    start_date = date(today.year, today.month, 1)
    month = start_date + datetime.timedelta(days=30)
    partnr = Partnar.objects.get(user_id=request.user.id)
    total_hotel = Hotel.objects.filter(partner=partnr).count()
    booking = Booking.objects.filter(
        created_at__gte=start_date, created_at__lte=month, room__hotel__partner=partnr).count()
    data = {
        'total_hotel': total_hotel,
        'booking': booking
    }
    return render(request, 'partner/partner_dashboard.html', data)


@partnar_required
def partner_hotel(request):
    partnr = Partnar.objects.get(user_id=request.user.id)
    hotel = Hotel.objects.filter(partner=partnr)
    data = {
        'hotel': hotel
    }
    return render(request, 'partner/partnet_hotel.html', data)


@partnar_required
def pertner_hotel_fecilitis(request):
    fecilitis = Facilities_For_Hotels.objects.all()
    data = {
        'fec': fecilitis
    }
    return render(request, 'partner/partnet_hotel_fecilitis.html', data)


@partnar_required
def pertner_hotel_fecilitis_add(request):
    if request.method == "POST":
        feciliti = request.POST['feciliti']
        fec = Facilities_For_Hotels()
        fec.feciliti = feciliti
        fec.save()
        messages.success(request, "Fecilitis Added Successfully")
        return redirect('pertner_hotel_fecilitis')


@partnar_required
def pertner_hotel_fecilitis_update(request, id):
    if request.method == "POST":
        feciliti = request.POST['feciliti']
        fec = Facilities_For_Hotels(id=id)
        fec.feciliti = feciliti
        fec.save()
        messages.success(request, "Fecilitis Updated Successfully")
        return redirect('pertner_hotel_fecilitis')


@partnar_required
def partner_hotel_add(request):
    partnr = Partnar.objects.get(user_id=request.user.id)
    dst = Destination.objects.all()
    topdst = TopDestination.objects.all()
    fecilitis = Facilities_For_Hotels.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        rate = request.POST['rate']
        details = request.POST['details']
        logo = request.FILES['logo']
        thumbnails = request.FILES['thumbnails']
        mobile = request.POST['mobile']
        address = request.POST['address']
        mail = request.POST['mail']
        owner = request.POST['owner']
        dst_id = request.POST['dst_id']
        website = request.POST['website']
        promo_video = request.POST['promo_video']
        checkout = request.POST['checkout']
        min_stay = request.POST['min_stay']
        min_booking_number = request.POST['min_booking_number']
        feciliti = request.POST.getlist('feciliti[]')
        hotelgallery = request.FILES.getlist('hotelgallery[]')
        hotel = Hotel()
        hotel.name = name
        hotel.partner = partnr
        hotel.rate = rate
        hotel.details = details
        hotel.logo = logo
        hotel.thumbnails = thumbnails
        hotel.mobile = mobile
        hotel.address = address
        hotel.mail = mail
        hotel.destination_id = dst_id
        hotel.owner = owner
        hotel.website = website
        hotel.promo_video = promo_video
        hotel.checkout = checkout
        hotel.min_stay = min_stay
        hotel.min_booking_number = min_booking_number
        hotel.save()
        for fec in feciliti:
            fecs = Hotel_Facilities()
            fecs.feciliti = fec
            fecs.hotel = hotel
            fecs.save()
        for gallery in hotelgallery:
            gl = HotelGallery()
            gl.hotel = hotel
            gl.image = gallery
            gl.save()
        messages.success(request, "Hotel Added Successfully")
        return redirect('partner_hotel')
    data = {
        'fec': fecilitis,
        'dst': dst,
        'topdst': topdst
    }
    return render(request, 'partner/partner_hotel_add.html', data)


@partnar_required
def partner_hotel_edit(request, id):
    partnr = Partnar.objects.get(user_id=request.user.id)
    hotel = Hotel.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST['name']
        rate = request.POST['rate']
        details = request.POST['details']
        logo = request.FILES['logo']
        thumbnails = request.FILES['thumbnails']
        mobile = request.POST['mobile']
        address = request.POST['address']
        mail = request.POST['mail']
        owner = request.POST['owner']
        website = request.POST['website']
        promo_video = request.POST['promo_video']
        checkout = request.POST['checkout']
        min_stay = request.POST['min_stay']
        min_booking_number = request.POST['min_booking_number']
        hotel.name = name
        hotel.rate = rate
        hotel.details = details
        hotel.logo = logo
        hotel.thumbnails = thumbnails
        hotel.mobile = mobile
        hotel.address = address
        hotel.mail = mail
        hotel.owner = owner
        hotel.website = website
        hotel.promo_video = promo_video
        hotel.checkout = checkout
        hotel.min_stay = min_stay
        hotel.min_booking_number = min_booking_number
        hotel.save()
        messages.success(request, "Hotel Updated Successfully")
        return redirect('partner_hotel')
    data = {
        'hotel': hotel,
    }
    return render(request, 'partner/partner_hotel_edit.html', data)


@partnar_required
def partner_hotel_single(request, slug):
    partnr = Partnar.objects.get(user_id=request.user.id)
    hotel = get_object_or_404(Hotel, slug=slug, partner=partnr)
    feciliti = Hotel_Facilities.objects.filter(hotel=hotel)
    gallery = HotelGallery.objects.filter(hotel=hotel)
    room = Rooms.objects.filter(hotel=hotel)
    data = {
        'hotel': hotel,
        'fec': feciliti,
        'gl': gallery,
        'room': room
    }
    return render(request, 'partner/partnet_hotel_single.html', data)



@partnar_required
def pertner_hotel_copy(request, id):
    ht = Hotel.objects.get(id=id)
    hotel = Hotel()
    hotel.name = ht.name
    hotel.partner = ht.partner
    hotel.rate = ht.rate
    hotel.details = ht.details
    hotel.logo = ht.logo
    hotel.thumbnails = ht.thumbnails
    hotel.mobile = ht.mobile
    hotel.address = ht.address
    hotel.mail = ht.mail
    hotel.destination_id = ht.destination.pk
    hotel.owner = ht.owner
    hotel.website = ht.website
    hotel.promo_video = ht.promo_video
    hotel.checkout = ht.checkout
    hotel.min_stay = ht.min_stay
    hotel.min_booking_number = ht.min_booking_number
    hotel.save()
    messages.success(request, "Hotel Duplicated Successfully")
    return redirect('partner_hotel')



@partnar_required
def pertner_room_fecilitis(request):
    fecilitis = Facilities_For_Room.objects.all()
    data = {
        'fec': fecilitis
    }
    return render(request, 'partner/partnet_room_fecilitis.html', data)


@partnar_required
def pertner_room_fecilitis_add(request):
    if request.method == "POST":
        feciliti = request.POST['feciliti']
        fec = Facilities_For_Room()
        fec.feciliti = feciliti
        fec.save()
        messages.success(request, "Fecilitis Added Successfully")
        return redirect('pertner_room_fecilitis')


@partnar_required
def pertner_room_fecilitis_update(request, id):
    if request.method == "POST":
        feciliti = request.POST['feciliti']
        fec = Facilities_For_Room(id=id)
        fec.feciliti = feciliti
        fec.save()
        messages.success(request, "Fecilitis Updated Successfully")
        return redirect('pertner_room_fecilitis')


@partnar_required
def partner_room(request):
    partnr = Partnar.objects.get(user_id=request.user.id)
    # hotels = Hotel.objects.get(partner=partnr)
    fecilitis = Facilities_For_Room.objects.all()
    room = Rooms.objects.filter(hotel__partner=partnr)
    data = {
        'room': room
    }
    return render(request, 'partner/partner_room.html', data)


@partnar_required
def partner_room_add(request):
    partnr = Partnar.objects.get(user_id=request.user.id)
    hotels = Hotel.objects.filter(partner=partnr)
    fecilitis = Facilities_For_Room.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        hotel = request.POST['hotel']
        thumbnails = request.FILES['thumbnails']
        details = request.POST['details']
        number_of_room = request.POST['number_of_room']
        number_of_bed = request.POST['number_of_bed']
        number_of_adult = request.POST['number_of_adult']
        number_of_children = request.POST['number_of_children']
        room_footage = request.POST['room_footage']
        allow_cancel = request.POST['allow_cancel']
        arrive = request.POST['arrive']
        cancel_fee = request.POST['cancel_fee']
        price = request.POST['price']
        before_booking = request.POST['before_booking']
        min_stay = request.POST['min_stay']
        feciliti = request.POST.getlist('feciliti[]')
        roomgallery = request.FILES.getlist('roomgallery[]')
        room = Rooms()
        room.name = name
        room.hotel_id = hotel
        room.thumbnails = thumbnails
        room.details = details
        room.number_of_room = number_of_room
        room.number_of_bed = number_of_bed
        room.number_of_adult = number_of_adult
        room.number_of_children = number_of_children
        room.room_footage = room_footage
        if allow_cancel == "yes":
            room.allow_cancel = True
        else:
            room.allow_cancel = False
        room.arrive = arrive
        room.cancel_fee = cancel_fee
        room.price = price
        room.before_booking = before_booking
        room.min_stay = min_stay
        room.save()
        for fec in feciliti:
            fecs = RoomFacilities()
            fecs.feciliti = fec
            fecs.room = room
            fecs.save()
        for gallery in roomgallery:
            gl = RoomGallery()
            gl.room = room
            gl.image = gallery
            gl.save()
        messages.success(request, "Room Added Successfully")
        return redirect('partner_room')
    data = {
        'hotel': hotels,
        'fec': fecilitis
    }
    return render(request, 'partner/partner_room_add.html', data)


@partnar_required
def partner_room_edit(request, id):
    partnr = Partnar.objects.get(user_id=request.user.id)
    hotels = Hotel.objects.filter(partner=partnr)
    room = Rooms.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST['name']
        hotel = request.POST['hotel']
        thumbnails = request.FILES['thumbnails']
        details = request.POST['details']
        number_of_room = request.POST['number_of_room']
        number_of_bed = request.POST['number_of_bed']
        number_of_adult = request.POST['number_of_adult']
        number_of_children = request.POST['number_of_children']
        room_footage = request.POST['room_footage']
        allow_cancel = request.POST['allow_cancel']
        arrive = request.POST['arrive']
        cancel_fee = request.POST['cancel_fee']
        price = request.POST['price']
        before_booking = request.POST['before_booking']
        min_stay = request.POST['min_stay']
        room.name = name
        room.hotel_id = hotel
        room.thumbnails = thumbnails
        room.details = details
        room.number_of_room = number_of_room
        room.number_of_bed = number_of_bed
        room.number_of_adult = number_of_adult
        room.number_of_children = number_of_children
        room.room_footage = room_footage
        if allow_cancel == "yes":
            room.allow_cancel = True
        else:
            room.allow_cancel = False
        room.arrive = arrive
        room.cancel_fee = cancel_fee
        room.price = price
        room.before_booking = before_booking
        room.min_stay = min_stay
        room.save()
        messages.success(request, "Room Updated Successfully")
        return redirect('partner_room')
    data = {
        'hotel': hotels,
        'room': room
    }
    return render(request, 'partner/partner_room_edit.html', data)


@partnar_required
def partner_room_single(request, slug):
    partnr = Partnar.objects.get(user_id=request.user.id)
    room = Rooms.objects.get(slug=slug)
    feciliti = RoomFacilities.objects.filter(room=room)
    gallery = RoomGallery.objects.filter(room=room)
    data = {
        'room': room,
        'fec': feciliti,
        'gl': gallery,
    }
    return render(request, 'partner/partner_room_single.html', data)


@partnar_required
def partner_booking(request):
    partnr = Partnar.objects.get(user_id=request.user.id)
    # hotels = Hotel.objects.filter(partner=partnr).first()
    # fecilitis = Facilities_For_Room.objects.all()
    # room = Rooms.objects.get(hotel=hotels)
    book = Booking.objects.filter(room__hotel__partner=partnr)
    data = {
        # 'hotel': hotels,
        # 'fec': fecilitis,
        'book': book
    }
    return render(request, 'partner/partner_booking.html', data)


@partnar_required
def partner_booking_add(request):
    return render(request, 'partner/partner_booking_add.html')


def pertner_room_book_update(request, id):
    book = Booking.objects.get(id=id)
    if request.method == 'POST':
        status = request.POST['status']
        if status == "True":
            book.status = True
        else:
            book.status = False
        book.save()
        messages.success(request, "Booking Updated Successfully")
        return redirect('partner_booking')


def partner_enquiry(request):
    partnr = Partnar.objects.get(user_id=request.user.id)
    enquiry = Enquiry.objects.filter(
        hotel__partner=partnr).order_by('-created_at')
    data = {
        'enquiry': enquiry
    }
    return render(request, 'partner/enquiry.html', data)
