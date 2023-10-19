from django.shortcuts import render, redirect
from django.contrib import messages
from authentication.models import User
from dashboard.models import *
from customer.models import *
from decimal import Decimal
from django.http import JsonResponse


def get_booking_customer(request):
    client = request.GET.get('customer')
    filter = request.GET.get('filter')
    if filter == "id":
        clint = Customer.objects.get(id=client)
    elif filter == "phone":
        user = User.objects.get(phone=client)
        clint = Customer.objects.get(user=user)
    elif filter == "email":
        user = User.objects.get(email=client)
        clint = Customer.objects.get(user=user)
    elif filter == "username":
        user = User.objects.get(username=client)
        clint = Customer.objects.get(user=user)
    data = {
        'customer': clint
    }
    return render(request, 'get/get_booking_customer.html', data)


def get_top_dst(request):
    tpid = request.GET.get('topdst')
    tpdst = TopDestination.objects.get(id=tpid)
    dst = Destination.objects.filter(top=tpdst)
    data = {
        'dst': dst
    }
    return render(request, 'get/get_top_dst.html', data)


def get_hotel_partner(request):
    partner = request.GET.get('partner')
    filter = request.GET.get('filter')
    if filter == "id":
        clint = Partnar.objects.get(id=partner)
    elif filter == "phone":
        user = User.objects.get(phone=partner)
        clint = Partnar.objects.get(user=user)
    elif filter == "email":
        user = User.objects.get(email=partner)
        clint = Partnar.objects.get(user=user)
    elif filter == "username":
        user = User.objects.get(username=partner)
        clint = Partnar.objects.get(user=user)
    data = {
        'customer': clint
    }
    return render(request, 'get/get_hotel_partner.html', data)


def get_partner_by_hotel(request):
    partner = request.GET.get('partner')
    filter = request.GET.get('filter')
    if filter == "id":
        clint = Partnar.objects.get(id=partner)
        hotel = Hotel.objects.filter(partner=clint)
    elif filter == "phone":
        user = User.objects.get(phone=partner)
        clint = Partnar.objects.get(user=user)
        hotel = Hotel.objects.filter(partner=clint)
    elif filter == "email":
        user = User.objects.get(email=partner)
        clint = Partnar.objects.get(user=user)
        hotel = Hotel.objects.filter(partner=clint)
    elif filter == "username":
        user = User.objects.get(username=partner)
        clint = Partnar.objects.get(user=user)
        hotel = Hotel.objects.filter(partner=clint)
    data = {
        'customer': clint,
        'hotel': hotel
    }
    return render(request, 'get/get_partner_by_hotel.html', data)


def autocomplete(request):
    query = request.GET.get('term', '')
    items = Destination.objects.filter(name__icontains=query)
    results = [item.name for item in items]
    return JsonResponse(results, safe=False)


def get_flight_adult(request):
    adult = request.GET.get('adult')
    price = request.GET.get('price')
    totalam = Decimal(price) * int(adult)
    data = {
        'totalam': totalam
    }
    return render(request, 'get/get_flight_adult.html', data)


def get_hotel_search_by_fec(request):
    fec = request.GET.get('fec')
    fc = Hotel_Facilities.objects.filter(feciliti=fec)
    # hotel = Hotel.objects.all()
    data = {
        'hotel': fc
    }
    return render(request, 'get/get_hotel_search_by_fec.html', data)


def get_room_booking_total(request):
    adult = request.GET.get('adult')
    child = request.GET.get('child')
    room_id = request.GET.get('room_id')
    inroom = request.GET.get('inroom')
    rom = Rooms.objects.get(id=room_id)
    print(inroom)
    # totalam += Decimal(rom.price) * int(adult + child)
    # totalam += Decimal(rom.price) * int(inroom)
    # data = {
    #     'totalam': totalam
    # }
    # return JsonResponse(data)
    return render(request, 'get/get_hotel_search_by_fec.html')