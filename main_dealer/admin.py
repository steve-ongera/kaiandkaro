from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Category, Brand, CarModel, Feature, Car, CarImage, RentalRate,
    Customer, Inquiry, Rental, Sale, TestDrive, BlogPost
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_filter = ['created_at']
    ordering = ['name']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country_of_origin', 'is_active', 'logo_preview', 'created_at']
    list_filter = ['is_active', 'country_of_origin', 'created_at']
    search_fields = ['name', 'country_of_origin']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['logo_preview']
    ordering = ['name']

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.logo.url)
        return "No Logo"
    logo_preview.short_description = "Logo Preview"


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'is_active', 'created_at']
    list_filter = ['brand', 'category', 'is_active', 'created_at']
    search_fields = ['name', 'brand__name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['brand__name', 'name']


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'icon', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name']
    ordering = ['category', 'name']


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    readonly_fields = ['image_preview']
    fields = ['image', 'image_preview', 'alt_text', 'is_main', 'order']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="75" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Preview"


class RentalRateInline(admin.TabularInline):
    model = RentalRate
    extra = 0
    fields = ['rate_type', 'rate', 'security_deposit', 'is_active']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = [
        'stock_number', 'car_info', 'year', 'car_type', 'color', 
        'selling_price', 'final_price', 'status', 'is_featured', 'main_image_preview'
    ]
    list_filter = [
        'status', 'car_type', 'is_featured', 'is_for_sale', 'is_for_rent',
        'brand', 'transmission', 'fuel_type', 'condition', 'year'
    ]
    search_fields = ['stock_number', 'vin_number', 'brand__name', 'car_model__name', 'color']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['id', 'final_price', 'monthly_rent_estimate', 'main_image_preview', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'stock_number', 'vin_number', 'brand', 'car_model', 'year', 'car_type')
        }),
        ('Physical Details', {
            'fields': ('color', 'mileage', 'engine_size', 'horsepower', 'transmission', 
                      'fuel_type', 'doors', 'seats', 'condition')
        }),
        ('Pricing', {
            'fields': ('msrp_price', 'selling_price', 'dealer_discount', 'final_price')
        }),
        ('Availability', {
            'fields': ('status', 'is_featured', 'is_for_rent', 'is_for_sale')
        }),
        ('SEO & Content', {
            'fields': ('title', 'slug', 'description', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Features & Location', {
            'fields': ('features', 'location')
        }),
        ('Rental Info', {
            'fields': ('monthly_rent_estimate',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [CarImageInline, RentalRateInline]
    filter_horizontal = ['features']
    
    def car_info(self, obj):
        return f"{obj.brand.name} {obj.car_model.name}"
    car_info.short_description = "Car"
    
    def main_image_preview(self, obj):
        main_img = obj.main_image
        if main_img:
            return format_html('<img src="{}" width="80" height="60" style="object-fit: cover;" />', main_img.image.url)
        return "No Image"
    main_image_preview.short_description = "Image"


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'city', 'country', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'id_number']
    list_filter = ['city', 'country', 'created_at']
    readonly_fields = ['full_name', 'created_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'first_name', 'last_name', 'full_name', 'email', 'phone', 'date_of_birth')
        }),
        ('Address', {
            'fields': ('address', 'city', 'country')
        }),
        ('Documents', {
            'fields': ('driving_license_number', 'id_number')
        }),
        ('System', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['customer', 'car_info', 'inquiry_type', 'status', 'created_at', 'car_link']
    list_filter = ['inquiry_type', 'status', 'preferred_contact_method', 'created_at']
    search_fields = ['customer__first_name', 'customer__last_name', 'car__stock_number', 'message']
    readonly_fields = ['created_at', 'updated_at', 'car_link']
    
    fieldsets = (
        ('Inquiry Details', {
            'fields': ('car', 'car_link', 'customer', 'inquiry_type', 'message')
        }),
        ('Contact & Status', {
            'fields': ('preferred_contact_method', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def car_info(self, obj):
        return f"{obj.car.brand.name} {obj.car.car_model.name}"
    car_info.short_description = "Car"
    
    def car_link(self, obj):
        if obj.car:
            url = reverse('admin:your_app_car_change', args=[obj.car.pk])  # Replace 'your_app' with actual app name
            return format_html('<a href="{}" target="_blank">View Car Details</a>', url)
        return "No Car"
    car_link.short_description = "Car Details"


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'car_info', 'start_date', 'end_date', 'total_amount', 'status']
    list_filter = ['status', 'start_date', 'created_at']
    search_fields = ['customer__first_name', 'customer__last_name', 'car__stock_number']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Rental Details', {
            'fields': ('id', 'car', 'customer', 'start_date', 'end_date')
        }),
        ('Location', {
            'fields': ('pickup_location', 'return_location')
        }),
        ('Pricing', {
            'fields': ('daily_rate', 'total_days', 'subtotal', 'security_deposit', 'total_amount')
        }),
        ('Status & Notes', {
            'fields': ('status', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def car_info(self, obj):
        return f"{obj.car.brand.name} {obj.car.car_model.name}"
    car_info.short_description = "Car"


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'car_info', 'agreed_price', 'final_amount', 'payment_method', 'status', 'sale_date']
    list_filter = ['status', 'payment_method', 'sale_date', 'created_at']
    search_fields = ['customer__first_name', 'customer__last_name', 'car__stock_number']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'sale_date'
    
    fieldsets = (
        ('Sale Details', {
            'fields': ('id', 'car', 'customer', 'payment_method', 'status')
        }),
        ('Pricing', {
            'fields': ('agreed_price', 'deposit_amount', 'trade_in_value', 'financing_amount', 'final_amount')
        }),
        ('Dates', {
            'fields': ('sale_date', 'delivery_date')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def car_info(self, obj):
        return f"{obj.car.brand.name} {obj.car.car_model.name}"
    car_info.short_description = "Car"


@admin.register(TestDrive)
class TestDriveAdmin(admin.ModelAdmin):
    list_display = ['customer', 'car_info', 'scheduled_date', 'duration_minutes', 'status']
    list_filter = ['status', 'scheduled_date', 'created_at']
    search_fields = ['customer__first_name', 'customer__last_name', 'car__stock_number']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'scheduled_date'
    
    fieldsets = (
        ('Test Drive Details', {
            'fields': ('car', 'customer', 'scheduled_date', 'duration_minutes', 'pickup_location')
        }),
        ('Status & Feedback', {
            'fields': ('status', 'notes', 'feedback')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def car_info(self, obj):
        return f"{obj.car.brand.name} {obj.car.car_model.name}"
    car_info.short_description = "Car"


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'published_date', 'created_at']
    list_filter = ['is_published', 'published_date', 'author', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'published_date'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'excerpt', 'content', 'featured_image')
        }),
        ('Publishing', {
            'fields': ('is_published', 'published_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


# Optional: Customize the admin site header and title
admin.site.site_header = "Kai and Karo Car Dealership Admin"
admin.site.site_title = "Kai and Karo Admin"
admin.site.index_title = "Welcome to Kai and Karo Administration"