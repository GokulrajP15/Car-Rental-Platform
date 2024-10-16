from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
# from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Car, Booking

# Create your views here.
def fun(request):
    return render(request,'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  # Redirect to the login page after successful registration
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

# @login_required
def car_list(request):
    cars = Car.objects.filter(is_available=True)
    return render(request, 'car_list.html', {'cars': cars})


# @login_required
def book_car(request, car_id):
    car = Car.objects.get(id=car_id)
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        booking = Booking.objects.create(
            user=request.user,
            car=car,
            start_date=start_date,
            end_date=end_date
        )
        car.is_available = False
        car.save()
        return redirect('booking_list')
    return render(request, 'book_car.html', {'car': car})


# @login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking_list.html', {'bookings': bookings})

# @login_required
def return_car(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.is_active = False
    booking.save()
    booking.car.is_available = True
    booking.car.save()
    return redirect('booking_list')


def is_staff_user(user):
    return user.is_staff

# @user_passes_test(is_staff_user)
def admin_dashboard(request):
    cars = Car.objects.all()
    bookings = Booking.objects.filter(is_active=True)
    return render(request, 'admin_dashboard.html', {'cars': cars, 'bookings': bookings})


def is_staff_user(user):
    return user.is_staff

# @user_passes_test(is_staff_user)
def add_car(request):
    if request.method == 'POST':
        name = request.POST['name']
        model = request.POST['model']
        year = request.POST['year']
        daily_rate = request.POST['daily_rate']
        Car.objects.create(name=name, model=model, year=year, daily_rate=daily_rate)
        return redirect('admin_dashboard')
    return render(request, 'add_car.html')

# @login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        booking = Booking.objects.create(
            user=request.user,
            car=car,
            start_date=start_date,
            end_date=end_date
        )
        car.is_available = False
        car.save()
        return redirect('booking_list')
    return render(request, 'book_car.html', {'car': car})