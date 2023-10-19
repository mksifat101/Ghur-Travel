from django.shortcuts import render, redirect
from customer.models import Customer
from dashboard.models import *
from home.models import *
from authentication.decorators import customer_required


@customer_required
def user_dashboard(request):
    customer = Customer.objects.get(user_id=request.user.id)
    book = Booking.objects.filter(user=customer)
    room_book = Booking.objects.filter(user=customer).count()
    flight_book = FlightBooking.objects.filter(customer=customer).count()
    room_p = Booking.objects.filter(user=customer, payment=False).count()
    flight_p = FlightBooking.objects.filter(customer=customer, payment=False).count()
    total = room_book + flight_book
    totalp = room_p + flight_p
    data = {
        'cst': customer,
        'book': book,
        'total': total,
        'totalp': totalp
    }
    return render(request, 'customer/user_dashboard.html', data)


@customer_required
def user_booking_list(request):
    customer = Customer.objects.get(user_id=request.user.id)
    book = Booking.objects.filter(user=customer)
    data = {
        'cst': customer,
        'book': book
    }
    return render(request, 'customer/user_booking_list.html', data)


@customer_required
def user_profile(request):
    customer = Customer.objects.get(user_id=request.user.id)
    data = {
        'cst': customer,
    }
    return render(request, 'customer/profile.html', data)


def edit_user_profile(request):
    customer = Customer.objects.get(user_id=request.user.id)
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        dob = request.POST['dob']
        address = request.POST['address']
        nid = request.POST['nid']
        nationality = request.POST['nationality']
        passport = request.POST['passport']
        father = request.POST['father']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        zip = request.POST['zip']
        user = User.objects.get(id=customer.user.pk)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone = phone
        user.save()
        customer.dob = dob
        customer.address = address
        customer.nid = nid
        customer.nationality = nationality
        customer.passport = passport
        customer.father = father
        customer.city = city
        customer.state = state
        customer.country = country
        customer.zip = zip
        customer.save()
        return redirect('user_profile')
    data = {
        'cst': customer,
    }
    return render(request, 'customer/edit_profile.html', data)