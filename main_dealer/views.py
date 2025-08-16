# views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count, Min, Max
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic import ListView, DetailView
from .models import (
    Car, Brand, CarModel, Category, Feature, 
    Customer, Inquiry, BlogPost, RentalRate
)
from .forms import InquiryForm, TestDriveForm, ContactForm


def home_view(request):
    """Home page view with featured cars and services"""
    
    # Get featured cars for the hero section
    featured_cars = Car.objects.filter(
        is_featured=True, 
        status='available'
    ).select_related('brand', 'car_model').prefetch_related('images')[:8]
    
    # Get latest cars
    latest_cars = Car.objects.filter(
        status='available'
    ).select_related('brand', 'car_model').prefetch_related('images').order_by('-created_at')[:8]
    
    # Get cars for sale
    cars_for_sale = Car.objects.filter(
        is_for_sale=True,
        status='available'
    ).select_related('brand', 'car_model').prefetch_related('images')[:4]
    
    # Get cars for rent
    cars_for_rent = Car.objects.filter(
        is_for_rent=True,
        status='available'
    ).select_related('brand', 'car_model').prefetch_related('images')[:4]
    
    # Get latest blog posts
    blog_posts = BlogPost.objects.filter(is_published=True)[:3]
    
    # Get brands for the filter
    brands = Brand.objects.filter(is_active=True).order_by('name')
    
    # Get year range for filter
    year_range = Car.objects.aggregate(
        min_year=Min('year'),
        max_year=Max('year')
    )
    
    context = {
        'featured_cars': featured_cars,
        'latest_cars': latest_cars,
        'cars_for_sale': cars_for_sale,
        'cars_for_rent': cars_for_rent,
        'blog_posts': blog_posts,
        'brands': brands,
        'year_range': year_range,
        'page_title': 'Find Your Dream Car - Kai and Karo',
        'meta_description': 'Browse our extensive collection of new and used cars. Foreign imports, local vehicles, and rental options available.',
    }
    
    return render(request, 'home.html', context)


def car_list_view(request):
    """Car listing page with filters and pagination"""
    
    # Base queryset
    cars = Car.objects.filter(status='available').select_related(
        'brand', 'car_model', 'car_model__category'
    ).prefetch_related('images', 'rental_rates')
    
    # Apply filters
    brand_id = request.GET.get('brand')
    if brand_id:
        cars = cars.filter(brand_id=brand_id)
    
    model_id = request.GET.get('model')
    if model_id:
        cars = cars.filter(car_model_id=model_id)
    
    year = request.GET.get('year')
    if year:
        cars = cars.filter(year=year)
    
    car_type = request.GET.get('car_type')
    if car_type:
        cars = cars.filter(car_type=car_type)
    
    condition = request.GET.get('condition')
    if condition:
        cars = cars.filter(condition=condition)
    
    transmission = request.GET.get('transmission')
    if transmission:
        cars = cars.filter(transmission=transmission)
    
    fuel_type = request.GET.get('fuel_type')
    if fuel_type:
        cars = cars.filter(fuel_type=fuel_type)
    
    color = request.GET.get('color')
    if color:
        cars = cars.filter(color__icontains=color)
    
    # Price range filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        cars = cars.filter(selling_price__gte=min_price)
    if max_price:
        cars = cars.filter(selling_price__lte=max_price)
    
    # Mileage filter
    mileage = request.GET.get('mileage')
    if mileage:
        mileage_map = {
            '10': 10000,
            '15': 15000,
            '20': 20000,
            '25': 25000,
            '27': 27000,
        }
        if mileage in mileage_map:
            cars = cars.filter(mileage__lte=mileage_map[mileage])
    
    # Availability filter
    availability = request.GET.get('availability', 'all')
    if availability == 'sale':
        cars = cars.filter(is_for_sale=True)
    elif availability == 'rent':
        cars = cars.filter(is_for_rent=True)
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        cars = cars.filter(
            Q(brand__name__icontains=search) |
            Q(car_model__name__icontains=search) |
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = [
        'selling_price', '-selling_price',
        'year', '-year',
        'mileage', '-mileage',
        'created_at', '-created_at'
    ]
    if sort_by in valid_sorts:
        cars = cars.order_by(sort_by)
    
    # Pagination
    per_page = request.GET.get('per_page', 9)
    try:
        per_page = int(per_page)
        if per_page not in [9, 15, 20]:
            per_page = 9
    except (ValueError, TypeError):
        per_page = 9
    
    paginator = Paginator(cars, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    brands = Brand.objects.filter(is_active=True).order_by('name')
    models = CarModel.objects.filter(is_active=True).select_related('brand').order_by('brand__name', 'name')
    categories = Category.objects.all().order_by('name')
    
    # Get available years, colors, etc.
    years = Car.objects.values_list('year', flat=True).distinct().order_by('-year')
    colors = Car.objects.values_list('color', flat=True).distinct().order_by('color')
    
    # Price range
    price_range = Car.objects.aggregate(
        min_price=Min('selling_price'),
        max_price=Max('selling_price')
    )
    
    context = {
        'page_obj': page_obj,
        'cars': page_obj,
        'brands': brands,
        'models': models,
        'categories': categories,
        'years': years,
        'colors': colors,
        'price_range': price_range,
        'current_filters': request.GET,
        'total_cars': paginator.count,
        'page_title': 'Car Listing - Kai and Karo',
        'meta_description': 'Browse our complete inventory of cars for sale and rent.',
    }
    
    return render(request, 'cars/car_list.html', context)


def car_detail_view(request, slug):
    """Car detail page"""
    
    car = get_object_or_404(
        Car.objects.select_related('brand', 'car_model', 'car_model__category')
        .prefetch_related('images', 'features', 'rental_rates'),
        slug=slug
    )
    
    # Get related cars (same brand or model)
    related_cars = Car.objects.filter(
        Q(brand=car.brand) | Q(car_model=car.car_model),
        status='available'
    ).exclude(id=car.id).select_related('brand', 'car_model').prefetch_related('images')[:4]
    
    # Handle inquiry form
    inquiry_form = InquiryForm()
    test_drive_form = TestDriveForm()
    
    if request.method == 'POST':
        if 'inquiry_submit' in request.POST:
            inquiry_form = InquiryForm(request.POST)
            if inquiry_form.is_valid():
                inquiry = inquiry_form.save(commit=False)
                inquiry.car = car
                inquiry.save()
                messages.success(request, 'Your inquiry has been submitted successfully!')
                return redirect('car_detail', slug=car.slug)
        
        elif 'test_drive_submit' in request.POST:
            test_drive_form = TestDriveForm(request.POST)
            if test_drive_form.is_valid():
                test_drive = test_drive_form.save(commit=False)
                test_drive.car = car
                test_drive.save()
                messages.success(request, 'Your test drive has been scheduled!')
                return redirect('car_detail', slug=car.slug)
    
    # Get features by category
    features_by_category = {}
    for feature in car.features.all():
        if feature.category not in features_by_category:
            features_by_category[feature.category] = []
        features_by_category[feature.category].append(feature)
    
    context = {
        'car': car,
        'related_cars': related_cars,
        'inquiry_form': inquiry_form,
        'test_drive_form': test_drive_form,
        'features_by_category': features_by_category,
        'page_title': f"{car.title} - Kai and Karo",
        'meta_description': car.meta_description or car.description[:160],
    }
    
    return render(request, 'cars/car_detail.html', context)


def get_models_by_brand(request):
    """AJAX view to get models by brand"""
    brand_id = request.GET.get('brand_id')
    models = []
    
    if brand_id:
        models = list(
            CarModel.objects.filter(brand_id=brand_id, is_active=True)
            .values('id', 'name')
            .order_by('name')
        )
    
    return JsonResponse({'models': models})


def contact_view(request):
    """Contact page view"""
    form = ContactForm()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Handle contact form submission
            # You can save to database or send email
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    
    context = {
        'form': form,
        'page_title': 'Contact Us - Kai and Karo',
        'meta_description': 'Get in touch with Kai and Karo for all your car needs.',
    }
    
    return render(request, 'cars/contact.html', context)


def about_view(request):
    """About page view"""
    context = {
        'page_title': 'About Us - Kai and Karo',
        'meta_description': 'Learn about Kai and Karo, your trusted car dealer in Kenya.',
    }
    
    return render(request, 'cars/about.html', context)


# Class-based views (alternative approach)
class CarListView(ListView):
    """Class-based view for car listing"""
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'
    paginate_by = 9
    
    def get_queryset(self):
        return Car.objects.filter(status='available').select_related(
            'brand', 'car_model'
        ).prefetch_related('images')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.filter(is_active=True)
        context['page_title'] = 'Car Listing - Kai and Karo'
        return context


class CarDetailView(DetailView):
    """Class-based view for car detail"""
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'
    slug_field = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.object
        
        context['related_cars'] = Car.objects.filter(
            brand=car.brand,
            status='available'
        ).exclude(id=car.id)[:4]
        
        context['page_title'] = f"{car.title} - Kai and Karo"
        return context