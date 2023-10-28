import requests
from amadeus import Client, ResponseError
from django.shortcuts import render, redirect
from dashboard.models import *
from customer.models import Customer
from django.contrib import messages
from django.db.models import Q
from authentication.decorators import customer_required
from django.core.mail import send_mail
from decimal import Decimal
from django.conf import settings
from core.settings import API_KEY, API_SERECT
from django.template.loader import render_to_string
from django.http import JsonResponse
from home.models import *



# bKash Info
app = "4f6o0cjiki2rfm34kfdadl1eqq"
secret = "2is7hdktrekvrbljjh44ll3d9l1dtjo4pasmjvs5vl5qr3fug4b"
username = "sandboxTokenizedUser02"
password = "sandboxTokenizedUser02@12345"



def get_bkash_token():
    url = 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant'
    # url = 'https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant'
    headers = {
        "Accept": "application/json",
        "username": username,
        "password": password,
        "Content-type": "application/json"
    }
    payload = {
        "app_secret": secret,
        "app_key": app
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        return response_data.get('id_token')
    else:
        return None


# Flight iataCode
# Resource From https://aviationstack.com/
IATA_API = "bdcb02b659c2afca4c9983207dc072a2"


def home(request):
    news = News.objects.all()[:3]
    hotel = Hotel.objects.filter(booked=False)
    topdst = TopDestination.objects.all()[:3]
    data = {
        'news': news,
        'hotel': hotel,
        'topdst': topdst
    }
    return render(request, 'home/home.html', data)


def top_destination_view(request, slug):
    topdst = TopDestination.objects.get(slug=slug)
    dst = Destination.objects.filter(top=topdst)
    hotel = Hotel.objects.filter(destination__top=topdst)
    data = {
        'dst': dst,
        'hotel': hotel
    }
    return render(request, 'home/top_destination.html', data)


def news_single(request, slug):
    pnews = News.objects.all()[:4]
    news = News.objects.get(slug=slug)
    data = {
        'news': news,
        'pnews': pnews
    }
    return render(request, 'home/news_single.html', data)


def contact(request):
    return render(request, 'home/contact.html')


def about(request):
    return render(request, 'home/about.html')


def news(request):
    news = News.objects.all()
    data = {
        'news': news
    }
    return render(request, 'home/news.html', data)


# https://api.aviationstack.com/v1/airports?access_key=YOUR_API_KEY&search=London

def get_airline_logo(carrier_code):
    return "https://s1.apideeplink.com/images/airlines/" + carrier_code + ".png"


def flight_search(request):
    icode = {
        "Dhaka": "DAC",
        "Barisal": "BZL",
        "Cox's Bazar": "CXB",
        "Ishurdi": "IRD",
        "Jashore": "JSR",
        "Ishwardi": "IRD",
        "Sylhet": "ZYL",
        "Saidpur": "SPD",
        "Chittagong": "CGP",
        "Rajshahi": "RJH"
    }
    amadeus = Client(
        client_id='rwNBFAxuT1rSft2YZS4dAP5A0J3GRwRE',
        client_secret='hW3GUDOi4qOXbWB5'
    )
    if request.method == "GET":
        orgloc = request.GET.get('orgloc', '')
        dstloc = request.GET.get('dstloc', '')
        dstdate = request.GET.get('dstdate', '')
        trclass = request.GET.get('trclass', '')
        adult = request.GET.get('adult_number', '')
        child = request.GET.get('child_number', '')
        # print(orgloc)
        # parm = {
        #     "access_key": "bdcb02b659c2afca4c9983207dc072a2",
        #     "search": "London"
        # }
        # idst = "http://api.aviationstack.com/v1/airports"
        # idst_data = requests.get(idst, parm)
        # print(idst_data.json())
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=icode[orgloc],
            destinationLocationCode=icode[dstloc],
            departureDate=dstdate,
            adults=adult, children=child, travelClass=trclass)
        data = {
            'result': response.data,
            'count': len(response.data),
            'org': orgloc,
            'dst': dstloc,
            'time': dstdate,
            'adult': adult,
            'child': child,
            'trclass': trclass
        }
        # print(response.data)
    return render(request, 'home/flight.html', data)


def hotels(request):
    fec = Facilities_For_Hotels.objects.all()
    hotel = Hotel.objects.filter(booked=False)
    thotel = Hotel.objects.filter(booked=False).count()
    data = {
        'hotel': hotel,
        'thotel': thotel,
        'fec': fec
    }
    return render(request, 'home/hotels.html', data)


def hotel_single(request, slug):
    hotel = Hotel.objects.get(slug=slug)
    room = Rooms.objects.filter(hotel=hotel, booked=False)
    fc = Hotel_Facilities.objects.filter(hotel=hotel)
    hotel1 = Hotel.objects.all()[:3]
    data = {
        'hotel': hotel,
        'hotel1': hotel1,
        'room': room,
        'fc': fc
    }
    return render(request, 'home/hotel_single.html', data)


def hotel_enquiry(request, slug):
    hotel = Hotel.objects.get(slug=slug)
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        comment = request.POST['message']
        enq = Enquiry()
        enq.hotel = hotel
        enq.name = name
        enq.email = email
        enq.comment = comment
        enq.save()
        messages.success(request, "Your Enquiry Submited")
        return redirect('hotel_single', hotel.slug)


def hotel_search(request):
    if request.method == "POST":
        dst = request.POST['destination']
        checkin = request.POST['checkin']
        checkout = request.POST['checkout']
        room_number = request.POST['room_number']
        adult_number = request.POST['adult_number']
        child_number = request.POST['child_number']
        fec = Facilities_For_Hotels.objects.all()
        hotel = Hotel.objects.filter(Q(destination__name__icontains=dst))
        thotel = Hotel.objects.filter(Q(destination__name__icontains=dst)).count()
        data = {
            'hotel': hotel,
            'fec': fec,
            'thotel': thotel
        }
        return render(request, 'home/hotel_search.html', data)


def fac_by_hotel(request):
    if request.method == "POST":
        fec = request.POST['fac']
        fec1 = Facilities_For_Hotels.objects.all()
        hotel = Hotel_Facilities.objects.filter(feciliti=fec)
        data = {
            'hotel': hotel,
            'fec': fec1
        }
    return render(request, 'home/hotel_search.html', data)


def user_room_search(request, slug):
    if request.method == "POST":
        # fromdt = request.POST['fromdt']
        # todt = request.POST['todt']
        # hotelid = request.POST['hotelid']
        hotel = Hotel.objects.get(slug=slug)
        room = Rooms.objects.filter(hotel=hotel, booked=False)
        fc = Hotel_Facilities.objects.filter(hotel=hotel)
    data = {
        'hotel': hotel,
        'room': room,
        'fc': fc
    }
    return render(request, 'home/hotel_room_search.html', data)


def single_room(request, slug):
    room = Rooms.objects.get(slug=slug)
    gallery = RoomGallery.objects.filter(room=room)
    rlroom = Rooms.objects.all()[:2]
    data = {
        'room': room,
        'gallery': gallery,
        'rlroom': rlroom
    }
    return render(request, 'home/single_room.html', data)


@customer_required
def room_booking(request, id):
    user = Customer.objects.get(user_id=request.user.id)
    room = Rooms.objects.get(id=id)
    fac = RoomFacilities.objects.filter(room=room)
    if request.method == "GET":
        # room_id = request.GET.get('room')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        adult = request.GET.get('adult')
        rooms = request.GET.get('room')
        price = request.GET.get('total') 
        adult = request.GET.get('adult')
        child = request.GET.get('child')
    data = {
        'room': room,
        'user': user,
        'fac': fac,
        'room_id': room.pk,
        'from_date': from_date,
        'to_date': to_date,
        'adult': adult,
        'price': price,
        'rooms': rooms,
        'child': child
    }
    return render(request, 'home/room_booking.html', data)




@customer_required
def flight_booking(request):
    user = Customer.objects.get(user_id=request.user.id)
    if request.method == "POST":
        orglocation = request.GET.get('orglocation')
        orgtime = request.GET.get('orgtime')
        dstlocation = request.GET.get('dstlocation')
        dsttime = request.GET.get('dsttime')
        price = request.GET.get('price')
        time = request.GET.get('time')
        duration = request.GET.get('duration')
        adult = request.GET.get('duration')
        child = request.GET.get('child')
        trclass = request.GET.get('trclass')
    data = {
        'user': user,
        'org': orglocation,
        'dst': dstlocation,
        'dstt': dsttime,
        'price': price,
        'orgt': orgtime,
        'time': time,
        'duration': duration,
        'adult': adult,
        'child': child,
        'trclass': trclass
    }
    return render(request, 'home/flight_booking.html', data)


def user_flight_booking_bkash(request):
    user = Customer.objects.get(user_id=request.user.id)
    if request.method == "POST":
        orglocation = request.GET.get('orglocation')
        orgtime = request.GET.get('orgtime')
        dstlocation = request.GET.get('dstlocation')
        dsttime = request.GET.get('dsttime')
        price = request.GET.get('price')
        time = request.GET.get('time')
        duration = request.GET.get('duration')
        child = request.GET.get('child')
        trclass = request.GET.get('trclass')
        adult = request.GET.get('adult')
        pay = request.GET.get('pay')
        if pay == "cash":
            flgit = FlightBooking()
            flgit.origin = orglocation
            flgit.destination = dstlocation
            flgit.takeof = orgtime
            flgit.land = dsttime
            flgit.price = Decimal(price)
            flgit.cabin = "Economy"
            flgit.adult = adult
            flgit.time = time
            flgit.customer_id = user.pk
            flgit.payment = False
            flgit.save()
            subject = "Thank Your For Flight Booking"
            message = render_to_string(
                'mail/booking.html', {"user": user})
            email_from = settings.EMAIL_HOST_USER
            recpipient_list = [user.user.email]
            send_mail(subject=subject, message=message,
                        from_email=email_from, recipient_list=recpipient_list)
            return redirect('user_dashboard')
        elif pay == "bkash":
            url = 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant'
            # url = 'https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant'
            headers = {
                "Accept": "application/json",
                "username": username,
                "password": password,
                "Content-type": "application/json"
            }
            payload = {
                "app_secret": secret,
                "app_key": app
            }
            response = requests.post(url, json=payload, headers=headers)
            token = response.json()['id_token']
            url2 = 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/create'
            # url2 = 'https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/create'
            payload2 = {
                "merchantInvoiceNumber": "012",
                "intent": "sale",
                "currency": "BDT",
                "amount": price,
                "callbackURL": "http://127.0.0.1:8000/success",
                "mode": "0011",
                "payerReference": "10"
            }
            headers2 = {
                "accept": "application/json",
                "Authorization": token,
                "X-APP-Key": app,
                "content-type": "application/json"
            }
            response2 = requests.post(url2, json=payload2, headers=headers2)
            request.session['payid'] = response2.json()['paymentID']
            request.session['price'] = price
            request.session['token'] = token
            request.session['orglocation'] = orglocation
            request.session['orgtime'] = orgtime
            request.session['dstlocation'] = dstlocation
            request.session['dsttime'] = dsttime
            request.session['time'] = time
            request.session['adult'] = adult
            bkashurl = response2.json()['bkashURL']
            print(bkashurl)
            payment_success(request)
            return redirect(bkashurl)
        

def user_flight_booking_cod(request):
    user = Customer.objects.get(user_id=request.user.id)
    if request.method == "POST":
        orglocation = request.POST['orglocation']
        orgtime = request.POST['orgtime']
        dstlocation = request.POST['dstlocation']
        dsttime = request.POST['dsttime']
        price = request.POST['price']
        time = request.POST['time']
        # duration = request.POST['duration']
        child = request.POST['child']
        trclass = request.POST['trclass']
        adult = request.POST['adult']
        # pay = request.POST['pay']
        flgit = FlightBooking()
        flgit.origin = orglocation
        flgit.destination = dstlocation
        flgit.takeof = orgtime
        flgit.land = dsttime
        flgit.price = Decimal(price)
        flgit.cabin = trclass
        flgit.adult = adult
        flgit.child = child
        flgit.time = time
        flgit.customer_id = user.pk
        flgit.payment = False
        flgit.save()
        book = Booking()
        book.user = user
        book.book_type = "Room"
        book.flight = flgit
        book.from_date = orgtime
        book.to_date = dsttime
        book.adult = adult
        book.child = child
        book.price = price
        book.payment = False
        book.cancel = False
        book.status = False
        book.save()
        subject = "Thank Your For Flight Booking"
        message = render_to_string(
            'mail/booking.html', {"user": user})
        email_from = settings.EMAIL_HOST_USER
        recpipient_list = [user.user.email]
        send_mail(subject=subject, message=message,
                    from_email=email_from, recipient_list=recpipient_list)
        return redirect('user_dashboard')


@customer_required
def user_room_booking(request):
    user = Customer.objects.get(user_id=request.user.id)
    if request.method == "POST":
        userid = request.POST['userid']
        address = request.POST['address']
        nid = request.POST['nid']
        city = request.POST['city']
        state = request.POST['state']
        zip = request.POST['zip']
        country = request.POST['country']
        book_from = request.POST['book_from']
        book_to = request.POST['book_to']
        roomid = request.POST['room']
        pay = request.POST['pay']
        room = Rooms.objects.get(id=roomid)
        if pay == "cash":
            usr = Customer.objects.get(id=userid)
            usr.address = address
            usr.nid = nid
            usr.city = city
            usr.state = state
            usr.zip = zip
            usr.country = country
            usr.save()
            bk = Booking()
            bk.customer_id = userid
            bk.room_id = roomid
            bk.adult = room.number_of_adult
            bk.child = room.number_of_children
            bk.check_in = book_from
            bk.check_out = book_to
            bk.book_by = "cash"
            bk.status = False
            bk.save()
            subject = "Thank Your For Registration"
            message = render_to_string(
                'mail/booking.html', {"user": usr})
            email_from = settings.EMAIL_HOST_USER
            recpipient_list = [usr.user.email]
            send_mail(subject=subject, message=message,
                      from_email=email_from, recipient_list=recpipient_list)
            return redirect('user_dashboard')


def user_room_booking_bkash(request):
    user = Customer.objects.get(user_id=request.user.id)
    if request.method == "POST":
        room_id = request.POST['room']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        guest = request.POST['guest']
        price = request.POST['price']
        user_id = user.pk
        # time = request.POST['time']
        # duration = request.POST['duration']
        # adult = request.POST['adult']
        # pay = request.POST['pay']
        url = 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant'
        # url = 'https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant'
        headers = {
            "Accept": "application/json",
            "username": username,
            "password": password,
            "Content-type": "application/json"
        }
        payload = {
            "app_secret": secret,
            "app_key": app
        }
        response = requests.post(url, json=payload, headers=headers)
        token = response.json()['id_token']
        url2 = 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/create'
        # url2 = 'https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/create'
        payload2 = {
            "merchantInvoiceNumber": "012",
            "intent": "sale",
            "currency": "BDT",
            "amount": price,
            "callbackURL": "http://127.0.0.1:8000/success",
            "mode": "0011",
            "payerReference": "10"
        }
        headers2 = {
            "accept": "application/json",
            "Authorization": token,
            "X-APP-Key": app,
            "content-type": "application/json"
        }
        response2 = requests.post(url2, json=payload2, headers=headers2)
        request.session['payid'] = response2.json()['paymentID']
        request.session['price'] = price
        request.session['token'] = token
        request.session['room_id'] = room_id
        request.session['from_date'] = from_date
        request.session['to_date'] = to_date
        request.session['guest'] = guest
        request.session['user_id'] = user_id
        bkashurl = response2.json()['bkashURL']
        # print(bkashurl)
        room_book_payment_success(request)
        return redirect(bkashurl)
    
def room_book_payment_success(request):
    pay = request.session.get('payid')
    price = request.session.get('price')
    room_id = request.session.get('room_id')
    from_date = request.session.get('from_date')
    to_date = request.session.get('to_date')
    guest = request.session.get('guest')
    user_id = request.session.get('user_id')
    # time = request.session.get('time')
    # adult = request.session.get('adult')
    token = request.session.get('token')
    url3 = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/execute"
    # url3 = "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/execute"
    payload3 = {"paymentID": pay}
    headers3 = {
        "accept": "application/json",
        "Authorization": token,
        "X-APP-Key": app,
        "content-type": "application/json",
    }
    response3 = requests.post(url3, json=payload3, headers=headers3)
    status = response3.json()["statusMessage"]
    url5 = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/payment/status"
    # url5 = "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/payment/status"
    payload5 = {"paymentID": pay}
    headers5 = {
        "accept": "application/json",
        "Authorization": token,
        "X-APP-Key": app,
        "content-type": "application/json",
    }
    response4 = requests.post(url5, json=payload5, headers=headers5)
    payment_status2 = response4.json()["transactionStatus"]
    if response4.status_code == 200:
        if status == "Successful":
            payment_status = response4.json()["transactionStatus"]
            if payment_status == 'Completed':
                book = Booking()
                book.user_id = user_id
                book.room_id = room_id,
                book.from_date = from_date
                book.to_date = to_date
                book.book_type = "Room"
                book.status = True
                book.guest = guest
                book.price = price
                book.save()
                subject = "Thank Your For Flight Booking"
                # message = render_to_string(
                #     'mail/booking.html', {"user": user})
                # email_from = settings.EMAIL_HOST_USER
                # recpipient_list = [user.email]
                # send_mail(subject=subject, message=message,
                #             from_email=email_from, recipient_list=recpipient_list)
                return redirect('user_dashboard')
    return render(request, 'home/payment-success.html')

def user_room_booking_cod(request):
    user = Customer.objects.get(user_id=request.user.id)
    if request.method == "POST":
        room_id = request.POST['room']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        adult = request.POST['adult']
        child = request.POST['child']
        price = request.POST['price']
        book = Booking()
        book.user = user
        book.book_type = "Room"
        book.room_id = room_id
        book.from_date = from_date
        book.to_date = to_date
        book.adult = adult
        book.child = child
        book.price = price
        book.payment = False
        book.cancel = False
        book.status = False
        book.save()
        subject = "Thank Your For Flight Booking"
        message = render_to_string(
            'mail/booking.html', {"user": user})
        email_from = settings.EMAIL_HOST_USER
        recpipient_list = [user.user.email]
        send_mail(subject=subject, message=message,
                    from_email=email_from, recipient_list=recpipient_list)
        request.session['room_id'] = room_id
        request.session['from_date'] = from_date
        request.session['to_date'] = to_date
        return redirect('booking_success')

def payment_success(request):
    pay = request.session.get('payid')
    price = request.session.get('price')
    orglocation = request.session.get('orglocation')
    orgtime = request.session.get('orgtime')
    dsttime = request.session.get('dsttime')
    dstlocation = request.session.get('dstlocation')
    time = request.session.get('time')
    adult = request.session.get('adult')
    token = request.session.get('token')
    url3 = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/execute"
    # url3 = "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/execute"
    payload3 = {"paymentID": pay}
    headers3 = {
        "accept": "application/json",
        "Authorization": token,
        "X-APP-Key": app,
        "content-type": "application/json",
    }
    response3 = requests.post(url3, json=payload3, headers=headers3)
    status = response3.json()["statusMessage"]
    url5 = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/payment/status"
    # url5 = "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/payment/status"
    payload5 = {"paymentID": pay}
    headers5 = {
        "accept": "application/json",
        "Authorization": token,
        "X-APP-Key": app,
        "content-type": "application/json",
    }
    response4 = requests.post(url5, json=payload5, headers=headers5)
    payment_status2 = response4.json()["transactionStatus"]
    if response4.status_code == 200:
        if status == "Successful":
            payment_status = response4.json()["transactionStatus"]
            if payment_status == 'Completed':
                flgit = FlightBooking()
                flgit.origin = orglocation
                flgit.destination = dstlocation
                flgit.takeof = orgtime
                flgit.land = dsttime
                flgit.price = price
                flgit.cabin = "Economy"
                flgit.adult = adult
                flgit.time = time
                # flgit.customer_id = user.pk
                flgit.payment = False
                flgit.save()
                subject = "Thank Your For Flight Booking"
                # message = render_to_string(
                #     'mail/booking.html', {"user": user})
                # email_from = settings.EMAIL_HOST_USER
                # recpipient_list = [user.email]
                # send_mail(subject=subject, message=message,
                #             from_email=email_from, recipient_list=recpipient_list)
                return redirect('user_dashboard')
    return render(request, 'home/payment-success.html')



@customer_required
def booking_success(request):
    room_id = request.session.get('room_id')
    from_date = request.session.get('from_date')
    to_date = request.session.get('to_date')
    room = Rooms.objects.get(id=room_id)
    data = {
        'from_date': from_date,
        'to_date': to_date,
        'room': room
    }
    return render(request, 'home/payment-success.html', data)