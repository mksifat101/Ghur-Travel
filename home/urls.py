from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact-us', views.contact, name='contact'),
    path('about-us', views.about, name='about'),
    path('hotels', views.hotels, name='hotels'),
    path('hotel/<slug>', views.hotel_single, name='hotel_single'),
    path('room/<slug>', views.single_room, name='single_room'),
    path('room/<id>/booking', views.room_booking, name='room_booking'),
    path('room-booking', views.user_room_booking, name='user_room_booking'),
    path('booking-success', views.booking_success, name='booking_success'),
    path('room-booking-with-bKash', views.user_room_booking_bkash, name='user_room_booking_bkash'),
    path('room-booking-with-cod', views.user_room_booking_cod, name='user_room_booking_cod'),
    path('room-booking-bkash-success', views.room_book_payment_success, name='room_book_payment_success'),

    # Hotel Search
    path('search', views.hotel_search, name='hotel_search'),
    path('search-by-facilits', views.fac_by_hotel, name='fac_by_hotel'),
    path('room-search/<slug>', views.user_room_search, name='user_room_search'),

    # Flight Search
    path('flight-search', views.flight_search, name='flight_search'),
    path('flight-booking', views.flight_booking, name='flight_booking'),
    path('user-flight-booking-bkash', views.user_flight_booking_bkash, name='user_flight_booking_bkash'),
    path('user-flight-booking-cod', views.user_flight_booking_cod, name='user_flight_booking_cod'),

    # Top Dst
    path('top-destination/<slug>', views.top_destination_view,
         name='top_destination_view'),
    # Enquriy
    path('hotel-enquiry/<slug>', views.hotel_enquiry, name='hotel_enquiry'),
    # Blog
    path('news', views.news, name='news'),
    path('news/<slug>', views.news_single, name='news_single'),
]
