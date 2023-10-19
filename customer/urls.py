from django.urls import path
from customer import views

urlpatterns = [
    path('dashboard', views.user_dashboard, name='user_dashboard'),
    path('booking', views.user_booking_list, name='user_booking_list'),
    path('profile', views.user_profile, name='user_profile'),
    path('edit-profile', views.edit_user_profile, name='edit_user_profile'),
]
