from django.shortcuts import render, redirect
from datetime import date
import datetime
from authentication.models import User
from django.contrib import messages
from partner.models import Partnar
from django.shortcuts import get_object_or_404
from dashboard.models import *
from django.core.paginator import Paginator
from customer.models import Customer
from authentication.decorators import admin_required
from home.models import *


@admin_required
def dashboard(request):
    hotel = Hotel.objects.all().count()
    today = date.today()
    start_date = date(today.year, today.month, 1)
    month = start_date + datetime.timedelta(days=30)
    booking = Booking.objects.filter(
        created_at__gte=start_date, created_at__lte=month).count()
    data = {
        'hotel': hotel,
        'book': booking
    }
    return render(request, 'dashboard/dashboard.html', data)


@admin_required
def destination(request):
    topdst = TopDestination.objects.all()
    dst_page = Destination.objects.all()
    paginator = Paginator(dst_page, 10)
    page_rc = request.GET.get('page')
    dst = paginator.get_page(page_rc)
    data = {
        'topdst': topdst,
        'dst': dst
    }
    return render(request, 'dashboard/destination.html', data)


@admin_required
def topdestination(request):
    topdst_page = TopDestination.objects.all()
    paginator = Paginator(topdst_page, 10)
    page_rc = request.GET.get('page')
    topdst = paginator.get_page(page_rc)
    data = {
        'topdst': topdst
    }
    return render(request, 'dashboard/topdestination.html', data)


@admin_required
def add_top_destination(request):
    if request.method == "POST":
        topdst = request.POST['topdst']
        image = request.FILES['image']
        dst = TopDestination()
        dst.name = topdst
        dst.image = image
        dst.save()
        messages.success(request, "Top Destination Added Successfully")
        return redirect('topdestination')


@admin_required
def top_destination_edit(request, id):
    dst = TopDestination.objects.get(id=id)
    if request.method == "POST":
        topdst = request.POST['topdst']
        image = request.FILES['image']
        dst.name = topdst
        dst.image = image
        dst.save()
        messages.success(request, "Top Destination Updated Successfully")
        return redirect('topdestination')


@admin_required
def top_destination_delete(request, id):
    dst = TopDestination.objects.get(id=id)
    dst.delete()
    messages.success(request, "Top Destination Deleted Successfully")
    return redirect('topdestination')


@admin_required
def add_destination(request):
    if request.method == "POST":
        topdst = request.POST['topdst']
        dst = request.POST['dst']
        dstm = Destination()
        dstm.top_id = topdst
        dstm.name = dst
        dstm.save()
        messages.success(request, "Destination Added Successfully")
        return redirect('destination')



@admin_required
def destination_edit(request, id):
    dstm = Destination.objects.get(id=id)
    if request.method == "POST":
        topdst = request.POST['topdst']
        dst = request.POST['dst']
        dstm.top_id = topdst
        dstm.name = dst
        dstm.save()
        messages.success(request, "Destination Updated Successfully")
        return redirect('destination')



@admin_required
def destination_delete(request, id):
    dstm = Destination.objects.get(id=id)
    dstm.delete()
    messages.success(request, "Destination Deleted Successfully")
    return redirect('destination')



@admin_required
def partner(request):
    partnr = Partnar.objects.all()
    data = {
        'partner': partnr
    }
    return render(request, 'dashboard/partner.html', data)


@admin_required
def add_partner(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        company = request.POST['company']
        tin_no = request.POST['tin_no']
        website = request.POST['website']
        address = request.POST['address']
        nid_front = request.FILES['nid_front']
        nid_back = request.FILES['nid_back']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username Already Exists")
            return redirect('partner')
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Exists")
            return redirect('partner')
        elif User.objects.filter(phone=phone).exists():
            messages.error(request, "Contact Number Already Exists")
            return redirect('partner')
        else:
            user = User()
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.phone = phone
            user.username = username
            user.set_password(password)
            user.is_partner = True
            user.is_active = True
            user.save()
            partnr = Partnar(user=user)
            partnr.company = company
            partnr.tin_no = tin_no
            partnr.website = website
            partnr.address = address
            partnr.nid_front = nid_front
            partnr.nid_back = nid_back
            partnr.save()
            messages.success(request, "Partner Added Successfully")
            return redirect('partner')
    return render(request, 'dashboard/add_partner.html')


@admin_required
def single_partner(request, username):
    partnr = get_object_or_404(Partnar, user__username=username)
    data = {
        'partner': partnr
    }
    return render(request, 'dashboard/single_partner.html', data)


@admin_required
def edit_partner(request, id):
    partnr = Partnar.objects.get(id=id)
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        company = request.POST['company']
        tin_no = request.POST['tin_no']
        website = request.POST['website']
        address = request.POST['address']
        status = request.POST['status']
        nid_front = request.FILES['nid_front']
        nid_back = request.FILES['nid_back']
        user = User.objects.get(id=partnr.user.pk)
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.email = email
        user.save()
        partnr.company = company
        partnr.tin_no = tin_no
        partnr.website = website
        partnr.address = address
        partnr.nid_front = nid_front
        partnr.nid_back = nid_back
        if status == "verified":
            partnr.status = True
        else:
            partnr.status = False
        partnr.save()
        messages.success(request, "Partner Updated Successfully")
        return redirect('partner')
    data = {
        'partnr': partnr
    }
    return render(request, 'dashboard/edit_partner.html', data)


@admin_required
def delete_partner(request, id):
    partnr = Partnar.objects.get(id=id)
    user = User.objects.get(id=partnr.user.pk)
    user.delete()
    messages.success(request, "Partner Deleted Successfully")
    return redirect('partner')


@admin_required
def dashboard_hotel_list(request):
    hotel = Hotel.objects.all()
    data = {
        'hotel': hotel
    }
    return render(request, 'dashboard/hotel_list.html', data)


@admin_required
def dashboard_hotel_fecilitis(request):
    fecilitis = Facilities_For_Hotels.objects.all()
    data = {
        'fec': fecilitis
    }
    return render(request, 'dashboard/hotel_fecilitis.html', data)


@admin_required
def dashboard_hotel_fecilitis_add(request):
    if request.method == "POST":
        feciliti = request.POST['feciliti']
        fec = Facilities_For_Hotels()
        fec.feciliti = feciliti
        fec.save()
        messages.success(request, "Fecilitis Added Successfully")
        return redirect('dashboard_hotel_fecilitis')


@admin_required
def dashboard_hotel_fecilitis_update(request, id):
    fec = Facilities_For_Hotels.objects.get(id=id)
    if request.method == "POST":
        feciliti = request.POST['feciliti']
        fec.feciliti = feciliti
        fec.save()
        messages.success(request, "Fecilitis Updated Successfully")
        return redirect('dashboard_hotel_fecilitis')
    

@admin_required
def dashboard_hotel_fecilitis_delete(request, id):
    fec = Facilities_For_Hotels.objects.get(id=id)
    fec.delete()
    messages.success(request, "Fecilitis Deleted Successfully")
    return redirect('dashboard_hotel_fecilitis')


@admin_required
def dashboard_hotel_add(request):
    dst = Destination.objects.all()
    topdst = TopDestination.objects.all()
    fecilitis = Facilities_For_Hotels.objects.all()
    partnet = Partnar.objects.all()
    if request.method == 'POST':
        partnr = request.POST['partnr']
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
        hotel.partner_id = partnr
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
        return redirect('dashboard_hotel_list')
    data = {
        'partnet': partnet,
        'fec': fecilitis,
        'dst': dst,
        'topdst': topdst
    }
    return render(request, 'dashboard/hotel_add.html', data)


@admin_required
def dashboard_hotel_edit(request, id):
    dst = Destination.objects.all()
    topdst = TopDestination.objects.all()
    fecilitis = Facilities_For_Hotels.objects.all()
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
        return redirect('dashboard_hotel_list')
    data = {
        'hotel': hotel,
        'fec': fecilitis,
        'dst': dst,
        'topdst': topdst
    }
    return render(request, 'dashboard/hotel_edit.html', data)


@admin_required
def dashboard_hotel_delete(request, id):
    room = Hotel.objects.get(id=id)
    room.delete()
    messages.success(request, "Hotel Deleted Successfully")
    return redirect('dashboard_hotel_list')


@admin_required
def dashboard_hotel_single(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug)
    feciliti = Hotel_Facilities.objects.filter(hotel=hotel)
    gallery = HotelGallery.objects.filter(hotel=hotel)
    room = Rooms.objects.filter(hotel=hotel)
    data = {
        'hotel': hotel,
        'fec': feciliti,
        'gl': gallery,
        'room': room
    }
    return render(request, 'dashboard/hotel_single.html', data)


@admin_required
def dashboard_room_fecilitis(request):
    fecilitis = Facilities_For_Room.objects.all()
    data = {
        'fec': fecilitis
    }
    return render(request, 'dashboard/room_fecilitis.html', data)


@admin_required
def dashboard_room_fecilitis_add(request):
    if request.method == "POST":
        feciliti = request.POST['feciliti']
        fec = Facilities_For_Room()
        fec.feciliti = feciliti
        fec.save()
        messages.success(request, "Fecilitis Added Successfully")
        return redirect('dashboard_room_fecilitis')


@admin_required
def dashboard_room_fecilitis_update(request, id):
    if request.method == "POST":
        feciliti = request.POST['feciliti']
        fec = Facilities_For_Room(id=id)
        fec.feciliti = feciliti
        fec.save()
        messages.success(request, "Fecilitis Updated Successfully")
        return redirect('dashboard_room_fecilitis')


@admin_required
def dashboard_room(request):
    fecilitis = Facilities_For_Room.objects.all()
    room = Rooms.objects.all()
    data = {
        'room': room
    }
    return render(request, 'dashboard/room.html', data)


@admin_required
def dashboard_room_add(request):
    hotels = Hotel.objects.all()
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
        return redirect('dashboard_room')
    data = {
        'hotel': hotels,
        'fec': fecilitis
    }
    return render(request, 'dashboard/room_add.html', data)


@admin_required
def dashboard_room_edit(request, id):
    room = Rooms.objects.get(id=id)
    hotels = Hotel.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
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
        return redirect('dashboard_room')
    data = {
        'hotel': hotels,
        'room': room
    }
    return render(request, 'dashboard/room_edit.html', data)


@admin_required
def dashboard_room_delete(request, id):
    room = Rooms.objects.get(id=id)
    room.delete()
    messages.success(request, "Room Deleted Successfully")
    return redirect('dashboard_room')


@admin_required
def dashboard_customer(request):
    customer = Customer.objects.all()
    data = {
        'customer': customer
    }
    return render(request, 'dashboard/customer.html', data)


@admin_required
def dashboard_room(request):
    room = Rooms.objects.all()
    data = {
        'room': room
    }
    return render(request, 'dashboard/room.html', data)



@admin_required
def dashboard_room_single(request, slug):
    room = Rooms.objects.get(slug=slug)
    feciliti = RoomFacilities.objects.filter(room=room)
    gallery = RoomGallery.objects.filter(room=room)
    data = {
        'room': room,
        'fec': feciliti,
        'gl': gallery,
    }
    return render(request, 'dashboard/room_single.html', data)


@admin_required
def dashboard_booking(request):
    book = Booking.objects.filter(book_type="Room")
    data = {
        'book': book
    }
    return render(request, 'dashboard/booking.html', data)

@admin_required
def dashboard_flight_booking(request):
    # book = FlightBooking.objects.all()
    book = Booking.objects.filter(book_type="Flight")
    data = {
        'book': book
    }
    return render(request, 'dashboard/flight_booking.html', data)


@admin_required
def dashboard_booking_add(request):
    return render(request, 'dashboard/add_booking.html')


@admin_required
def dashboard_news_categories(request):
    news = NewsCategory.objects.all()
    data = {
        'news': news
    }
    return render(request, 'dashboard/news_category.html', data)


@admin_required
def dashboard_news_categories_add(request):
    if request.method == "POST":
        name = request.POST['name']
        cat = NewsCategory()
        cat.name = name
        cat.save()
        messages.success(request, "Category Added Successfully")
        return redirect('dashboard_news_categories')


@admin_required
def pertner_hotel_news_update(request, slug):
    if request.method == "POST":
        name = request.POST['name']
        cat = NewsCategory.objects.get(slug=slug)
        cat.name = name
        cat.save()
        messages.success(request, "Category Updated Successfully")
        return redirect('dashboard_news_categories')


@admin_required
def dashboard_news(request):
    news = News.objects.all()
    data = {
        'news': news
    }
    return render(request, 'dashboard/news.html', data)


@admin_required
def dashboard_news_add(request):
    cat = NewsCategory.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        cats = request.POST['cat']
        thumbnails = request.FILES['thumbnails']
        details = request.POST['details']
        news = News()
        news.name = name
        news.categories_id = cats
        news.thumbnails = thumbnails
        news.details = details
        news.save()
        messages.success(request, "News Blogs Added Successfully")
        return redirect('dashboard_news')
    data = {
        'cat': cat
    }
    return render(request, 'dashboard/news_add.html', data)


@admin_required
def dashboard_enquiry(request):
    enquiry = Enquiry.objects.all().order_by('-created_at')
    data = {
        'enquiry': enquiry
    }
    return render(request, 'dashboard/enquiry.html', data)


@admin_required
def dashboard_team(request):
    team = Team.objects.all()
    data = {
        'team': team
    }
    return render(request, 'dashboard/team.html', data)


@admin_required
def dashboard_team_add(request):
    if request.method == "POST":
        name = request.POST['name']
        postition = request.POST['postition']
        image = request.FILES['image']
        facebook = request.POST['facebook']
        twitter = request.POST['twitter']
        linkedin = request.POST['linkedin']
        instagram = request.POST['instagram']
        team = Team()
        team.name = name
        team.postition = postition
        team.image = image
        team.facebook = facebook
        team.twitter = twitter
        team.linkedin = linkedin
        team.instagram = instagram
        team.save()
        messages.success(request, "Team Member Added Successfully")
        return redirect('dashboard_team')
    

@admin_required
def dashboard_team_edit(request, id):
    team = Team.objects.get(id=id)
    if request.method == "POST":
        name = request.POST['name']
        postition = request.POST['postition']
        image = request.FILES['image']
        facebook = request.POST['facebook']
        twitter = request.POST['twitter']
        linkedin = request.POST['linkedin']
        instagram = request.POST['instagram']
        team.name = name
        team.postition = postition
        team.image = image
        team.facebook = facebook
        team.twitter = twitter
        team.linkedin = linkedin
        team.instagram = instagram
        team.save()
        messages.success(request, "Team Member Updated Successfully")
        return redirect('dashboard_team')
    

@admin_required
def dashboard_team_delete(request, id):
    team = Team.objects.get(id=id)
    team.delete()
    messages.success(request, "Team Member Deleted Successfully")
    return redirect('dashboard_team')