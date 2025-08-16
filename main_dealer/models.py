from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
import uuid


class Category(models.Model):
    """Car categories like Hatchback, Sedan, SUV, etc."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    """Car brands like BMW, Toyota, etc."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    logo = models.ImageField(upload_to='brand_logos/', blank=True, null=True)
    country_of_origin = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CarModel(models.Model):
    """Car models like Camry, Q8, etc."""
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='car_models')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['brand', 'name']
        ordering = ['brand__name', 'name']

    def __str__(self):
        return f"{self.brand.name} {self.name}"


class Feature(models.Model):
    """Car features like Bluetooth, Navigation, etc."""
    FEATURE_CATEGORIES = [
        ('interior', 'Interior Design'),
        ('safety', 'Safety Design'),
        ('extra', 'Extra Design'),
        ('technical', 'Technical'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=FEATURE_CATEGORIES)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class Car(models.Model):
    """Main car model"""
    CAR_TYPES = [
        ('new', 'New Car'),
        ('foreign', 'Foreign Used'),
        ('local', 'Local Used'),
    ]
    
    AVAILABILITY_STATUS = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Under Maintenance'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
        ('cvt', 'CVT'),
        ('hybrid', 'Hybrid'),
    ]
    
    FUEL_TYPES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hybrid'),
        ('electric', 'Electric'),
        ('lpg', 'LPG'),
    ]
    
    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('very_good', 'Very Good'),
        ('good', 'Good'),
        ('fair', 'Fair'),
    ]

    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stock_number = models.CharField(max_length=20, unique=True)
    vin_number = models.CharField(max_length=17, unique=True, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2030)]
    )
    car_type = models.CharField(max_length=10, choices=CAR_TYPES)
    
    # Physical Details
    color = models.CharField(max_length=50)
    mileage = models.PositiveIntegerField(help_text="Mileage in kilometers")
    engine_size = models.DecimalField(max_digits=3, decimal_places=1, help_text="Engine size in liters")
    horsepower = models.PositiveIntegerField()
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES)
    doors = models.PositiveIntegerField(default=4)
    seats = models.PositiveIntegerField(default=5)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    
    # Pricing
    msrp_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    dealer_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Availability
    status = models.CharField(max_length=20, choices=AVAILABILITY_STATUS, default='available')
    is_featured = models.BooleanField(default=False)
    is_for_rent = models.BooleanField(default=False)
    is_for_sale = models.BooleanField(default=True)
    
    # SEO and Content
    title = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Features
    features = models.ManyToManyField(Feature, blank=True)
    
    # Location
    location = models.CharField(max_length=100, default="Nairobi, Kenya")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['brand', 'car_model']),
            models.Index(fields=['year', 'car_type']),
            models.Index(fields=['selling_price']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.year} {self.brand.name} {self.car_model.name}"
    
    def get_absolute_url(self):
        return reverse('car_detail', kwargs={'slug': self.slug})
    
    @property
    def final_price(self):
        """Calculate final price after dealer discount"""
        return self.selling_price - self.dealer_discount
    
    @property
    def monthly_rent_estimate(self):
        """Estimate monthly rental price (rough calculation)"""
        if self.is_for_rent:
            return round(self.final_price * 0.03, 2)  # 3% of car value per month
        return None
    
    @property
    def main_image(self):
        """Get the main image for the car"""
        first_image = self.images.filter(is_main=True).first()
        if first_image:
            return first_image
        return self.images.first()
    
    @property
    def is_new(self):
        return self.car_type == 'new'
    
    @property
    def is_foreign_used(self):
        return self.car_type == 'foreign'
    
    @property
    def is_local_used(self):
        return self.car_type == 'local'

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"{self.year} {self.brand.name} {self.car_model.name}"
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(f"{self.title}-{self.stock_number}")
        super().save(*args, **kwargs)


class CarImage(models.Model):
    """Car images"""
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='car_images/')
    alt_text = models.CharField(max_length=100, blank=True)
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.car} - Image {self.order}"
    
    def save(self, *args, **kwargs):
        if self.is_main:
            # Ensure only one main image per car
            CarImage.objects.filter(car=self.car, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)


class RentalRate(models.Model):
    """Rental pricing for cars"""
    RATE_TYPES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rental_rates')
    rate_type = models.CharField(max_length=10, choices=RATE_TYPES)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['car', 'rate_type']

    def __str__(self):
        return f"{self.car} - {self.rate_type}: ${self.rate}"


class Customer(models.Model):
    """Customer information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, default="Kenya")
    date_of_birth = models.DateField(null=True, blank=True)
    driving_license_number = models.CharField(max_length=50, blank=True)
    id_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Inquiry(models.Model):
    """Customer inquiries about cars"""
    INQUIRY_TYPES = [
        ('purchase', 'Purchase Inquiry'),
        ('rental', 'Rental Inquiry'),
        ('test_drive', 'Test Drive Request'),
        ('general', 'General Question'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('in_progress', 'In Progress'),
        ('converted', 'Converted'),
        ('closed', 'Closed'),
    ]
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='inquiries')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES)
    message = models.TextField()
    preferred_contact_method = models.CharField(
        max_length=20, 
        choices=[('email', 'Email'), ('phone', 'Phone'), ('whatsapp', 'WhatsApp')],
        default='email'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer.full_name} - {self.car} - {self.inquiry_type}"


class Rental(models.Model):
    """Car rental bookings"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rentals')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    pickup_location = models.CharField(max_length=200)
    return_location = models.CharField(max_length=200)
    
    # Pricing
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    total_days = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Status and Notes
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Rental #{self.id} - {self.car} - {self.customer.full_name}"


class Sale(models.Model):
    """Car sales records"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('deposit_paid', 'Deposit Paid'),
        ('financing_approved', 'Financing Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('financing', 'Financing'),
        ('trade_in', 'Trade-in'),
        ('mixed', 'Mixed Payment'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    car = models.OneToOneField(Car, on_delete=models.CASCADE, related_name='sale')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    # Pricing
    agreed_price = models.DecimalField(max_digits=12, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    trade_in_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    financing_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Details
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    sale_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Sale #{self.id} - {self.car} - {self.customer.full_name}"


class TestDrive(models.Model):
    """Test drive bookings"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='test_drives')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    scheduled_date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=30)
    pickup_location = models.CharField(max_length=200, default="Kai and Karo Showroom")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['scheduled_date']

    def __str__(self):
        return f"Test Drive - {self.car} - {self.customer.full_name} - {self.scheduled_date}"


class BlogPost(models.Model):
    """Blog posts for the website"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True)
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date', '-created_at']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})