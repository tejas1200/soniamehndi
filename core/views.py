from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render, redirect
from .models import Gallery, Category, Booking
from .utils.imagekit import upload_to_imagekit

def home(request):
    images = Gallery.objects.all()[:6]
    return render(request, 'core/index.html', {'images': images})


def gallery(request):
    images = Gallery.objects.all()
    return render(request, 'core/gallery.html', {'images': images})



def about(request):
    return render(request, 'core/about.html')


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def admin_login(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('/admin/')
    return render(request, 'core/admin/login.html')


def admin_logout(request):
    logout(request)
    return redirect('/admin-login/')


from .models import Gallery, Booking, Category

@login_required
def dashboard(request):
    images = Gallery.objects.all().order_by('-created_at')
    bookings = Booking.objects.all().order_by('-created_at')[:5]
    categories = Category.objects.all()

    context = {
        'images': images[:8],  # only show few
        'recent_bookings': bookings,
        'categories': categories,

        'total_images': images.count(),
        'total_bookings': Booking.objects.count(),
        'total_categories': Category.objects.count(),
    }

    return render(request, 'core/admin/dashboard.html', context)

from .utils.imagekit import upload_to_imagekit
@login_required
def add_image(request):
    images = Gallery.objects.all().order_by('-created_at')

    if request.method == "POST":
        file = request.FILES['image']
        category_id = request.POST['category']

        category = Category.objects.get(id=category_id)

        image_url = upload_to_imagekit(file)

        Gallery.objects.create(
            image=image_url,
            category=category
        )

        return redirect('/admin/')

    categories = Category.objects.all()

    return render(request, 'core/admin/add_image.html', {
        'categories': categories,
        'images': images
    })

    
@login_required
def edit_image(request, id):
    image = Gallery.objects.get(id=id)

    if request.method == "POST":
        category_id = request.POST['category']
        image.category = Category.objects.get(id=category_id)
        image.save()
        return redirect('/admin/')

    categories = Category.objects.all()

    return render(request, 'core/admin/edit_image.html', {
        'image': image,
        'categories': categories
    })

@login_required
def delete_image(request, id):
    image = Gallery.objects.get(id=id)
    image.delete()
    return redirect('/admin/')

@login_required
# CLIENT SIDE
def booking(request):
    if request.method == "POST":
        Booking.objects.create(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            date=request.POST.get('date'),
            event_type=request.POST.get('event_type'),
            message=request.POST.get('message')
        )
        return redirect('/booking/?success=1')

    return render(request, 'core/booking_form.html')


# ADMIN SIDE
from django.contrib.auth.decorators import login_required

@login_required
def booking_list(request):
    bookings = Booking.objects.all().order_by('-created_at')

    return render(request, 'core/admin/booking_list.html', {
        'bookings': bookings
    })


from django.shortcuts import render, redirect
from .models import Category
from django.contrib.auth.decorators import login_required


@login_required
def categories(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)

    categories = Category.objects.all().order_by('-id')

    return render(request, 'core/admin/categories.html', {
        'categories': categories
    })


@login_required
def delete_category(request, id):
    Category.objects.get(id=id).delete()
    return redirect('/admin/categories/')

def gallery(request):
    images = Gallery.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    return render(request, 'core/admin/gallery.html', {
        'images': images,
        'categories': categories
    })