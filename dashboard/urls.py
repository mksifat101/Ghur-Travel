from django.urls import path
from dashboard import views
from dashboard import get_views

urlpatterns = [
    #     Get
    path('get_booking_customer', get_views.get_booking_customer, name='get_booking_customer'),
    path('get_top_dst', get_views.get_top_dst, name='get_top_dst'),
    path('get_hotel_partner', get_views.get_hotel_partner, name='get_hotel_partner'),
    path('get_partner_by_hotel', get_views.get_partner_by_hotel, name='get_partner_by_hotel'),
    path('autocomplete', get_views.autocomplete, name='autocomplete'),
    path('get-flight-adult', get_views.get_flight_adult, name='get_flight_adult'),
    path('get-hotel-filter-fec', get_views.get_hotel_search_by_fec, name='get_hotel_search_by_fec'),
    path('get_room_booking_total', get_views.get_room_booking_total, name='get_room_booking_total'),
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    # Top Destination
    path('top-destination', views.topdestination, name='topdestination'),
    path('add-top-destination', views.add_top_destination, name='add_top_destination'),
    path('edit-top-destination/<id>', views.top_destination_edit, name='top_destination_edit'),
    path('delete-top-destination/<id>', views.top_destination_delete, name='top_destination_delete'),
    # Destination
    path('destination', views.destination, name='destination'),
    path('add-destination', views.add_destination, name='add_destination'),
    path('edit-destination/<id>', views.destination_edit, name='destination_edit'),
    path('delete-destination/<id>', views.destination_delete,
         name='destination_delete'),
    # Partner
    path('partners', views.partner, name='partner'),
    path('partner/<username>', views.single_partner, name='single_partner'),
    path('add-partner', views.add_partner, name='add_partner'),
    path('edit-partner/<id>', views.edit_partner, name='edit_partner'),
    path('delete-partner/<id>', views.delete_partner, name='delete_partner'),
#     
    path('hotels', views.dashboard_hotel_list, name='dashboard_hotel_list'),
    path('hotel/<slug>', views.dashboard_hotel_single, name='dashboard_hotel_single'),
    path('hotel/edit/<id>', views.dashboard_hotel_edit, name='dashboard_hotel_edit'),
    path('hotel/delete/<id>', views.dashboard_hotel_delete, name='dashboard_hotel_delete'),
    path('hotel/feciliti/', views.dashboard_hotel_fecilitis, name='dashboard_hotel_fecilitis'),
    path('hotel/fecilitis/add', views.dashboard_hotel_fecilitis_add, name='dashboard_hotel_fecilitis_add'),
    path('hotel/fecilitis/update/<id>', views.dashboard_hotel_fecilitis_update, name='dashboard_hotel_fecilitis_update'),
     #     
    path('room/fecilitis', views.dashboard_room_fecilitis, name='dashboard_room_fecilitis'),
    path('room/fecilitis/add', views.dashboard_room_fecilitis_add, name='dashboard_room_fecilitis_add'),
    path('room/fecilitis/<id>', views.dashboard_room_fecilitis_update, name='dashboard_room_fecilitis_update'),
    path('room/add', views.dashboard_room_add, name='dashboard_room_add'),
    path('room/<slug>', views.dashboard_room_single, name='dashboard_room_single'),
     #     
    path('hotels/add', views.dashboard_hotel_add, name='dashboard_hotel_add'),
#     
    path('category-add', views.dashboard_news_categories_add, name='dashboard_news_categories_add'),
    path('categories', views.dashboard_news_categories, name='dashboard_news_categories'),
    path('categories-updated/<slug>', views.pertner_hotel_news_update, name='pertner_hotel_news_update'),
     #     
    path('customer', views.dashboard_customer, name='dashboard_customer'),
#     
    path('rooms', views.dashboard_room, name='dashboard_room'),
    path('room/edit/<id>', views.dashboard_room_edit, name='dashboard_room_edit'),
    path('room/delete/<id>', views.dashboard_room_delete, name='dashboard_room_delete'),
     #     
    path('booking', views.dashboard_booking, name='dashboard_booking'),
    path('flight-booking', views.dashboard_flight_booking, name='dashboard_flight_booking'),
    path('book/add-booking', views.dashboard_booking_add, name='dashboard_booking_add'),
    path('enquiry', views.dashboard_enquiry, name='dashboard_enquiry'),
     #
    path('news', views.dashboard_news, name='dashboard_news'),
    path('add-news', views.dashboard_news_add, name='dashboard_news_add'),
    # Team
    path('team', views.dashboard_team, name='dashboard_team'),
    path('team/add', views.dashboard_team_add, name='dashboard_team_add'),
    path('team/edit/<id>', views.dashboard_team_edit, name='dashboard_team_edit'),
    path('team/delete/<id>', views.dashboard_team_delete, name='dashboard_team_delete'),
]
