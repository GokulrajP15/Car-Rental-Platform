from django.urls import path
from django.contrib.auth import views as av
from car_rental_app import views


urlpatterns = [
    path('',views.fun,name='home'),
    path('register/', views.register, name='register'),
    path('login/', av.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', av.LogoutView.as_view(next_page='home'), name='logout'),

    path('cars/', views.car_list, name='car_list'),
    path('book/<int:car_id>/', views.book_car, name='book_car'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('return/<int:booking_id>/', views.return_car, name='return_car'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-car/', views.add_car, name='add_car'),

    # path('car_list',views.car_list),
    # path('booking_list',views.booking_list),
    # path('admin_dashboard',views.admin_dashboard),
]