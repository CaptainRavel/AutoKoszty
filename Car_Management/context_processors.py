from .models import UserCars

def user_has_cars(request):
    if request.user.is_authenticated:
        cars_count = UserCars.objects.filter(user=request.user).count()
        has_cars = cars_count > 0
    else:
        has_cars = False
        cars_count = 0

    return {'user_has_cars': has_cars, 'cars_count': cars_count}