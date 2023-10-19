from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from authentication.models import User
from customer.models import Customer
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('dashboard')
        elif request.user.is_admin:
            return redirect('dashboard')
        elif request.user.is_staff:
            return redirect('staff_dashboard')
        elif request.user.is_customer:
            return redirect('user_dashboard')
        elif request.user.is_partner:
            return redirect('partner_dashboard')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            if user.is_customer:
                messages.success(request, 'Logged in Successfully')
                # if 'next' in request.POST:
                #     return redirect(request.POST.get('next'))
                # else:
                return redirect('user_dashboard')
            elif user.is_superuser:
                messages.success(request, 'Admin Logged in Successfully')
                return redirect('dashboard')
            elif user.is_partner:
                messages.success(request, 'Partnar Logged in Successfully')
                return redirect('partner_dashboard')
            # elif user.is_manager:
            #     messages.success(request, 'Admin Logged in Successfully')
            #     return redirect('dashboard')
            url = request.META.get('HTTP_REFERER')
        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect('login')
    return render(request, 'authentication/login.html')


def logout(request):
    auth.logout(request)
    messages.warning(request, 'Log Out Successfully')
    return redirect('login')


def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username Already Exists")
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Exists")
            return redirect('register')
        elif User.objects.filter(phone=phone).exists():
            messages.error(request, "Contact Number Already Exists")
            return redirect('register')
        else:
            user = User()
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.phone = phone
            user.set_password(password)
            user.is_customer = True
            user.is_active = True
            user.save()
            cst = Customer(user=user)
            cst.save()
            subject = "Thank Your For Registration"
            message = render_to_string(
                'mail/registration.html', {"user": cst})
            email_from = settings.EMAIL_HOST_USER
            recpipient_list = [email]
            send_mail(subject=subject, message=message, from_email=email_from, recipient_list=recpipient_list)
            messages.success(request, "User Profile Created Successfully")
            return redirect('login')
    return render(request, 'authentication/register.html')
