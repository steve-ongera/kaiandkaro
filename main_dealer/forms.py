from django import forms
from django.core.validators import RegexValidator
from .models import Inquiry, TestDrive, Customer, Car


class InquiryForm(forms.ModelForm):
    """Form for customer inquiries about cars"""
    
    # Customer fields (if not logged in)
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = forms.CharField(
        validators=[phone_regex],
        max_length=17,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+254700000000'
        })
    )

    class Meta:
        model = Inquiry
        fields = ['inquiry_type', 'message', 'preferred_contact_method']
        widgets = {
            'inquiry_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about your interest in this car, any specific questions, or requirements you might have...'
            }),
            'preferred_contact_method': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'inquiry_type': 'What are you interested in?',
            'message': 'Your Message',
            'preferred_contact_method': 'How would you like us to contact you?'
        }

    def __init__(self, *args, **kwargs):
        self.car = kwargs.pop('car', None)
        super().__init__(*args, **kwargs)
        
        # Add Bootstrap classes and styling
        for field_name, field in self.fields.items():
            if field_name not in ['inquiry_type', 'preferred_contact_method']:
                field.widget.attrs.update({'class': 'form-control'})
            
            # Add required attribute for HTML5 validation
            if field.required:
                field.widget.attrs.update({'required': 'required'})

    def save(self, commit=True):
        inquiry = super().save(commit=False)
        
        if self.car:
            inquiry.car = self.car
            
        if commit:
            # Create or get customer
            customer, created = Customer.objects.get_or_create(
                email=self.cleaned_data['email'],
                defaults={
                    'first_name': self.cleaned_data['first_name'],
                    'last_name': self.cleaned_data['last_name'],
                    'phone': self.cleaned_data['phone'],
                }
            )
            inquiry.customer = customer
            inquiry.save()
            
        return inquiry


class TestDriveForm(forms.ModelForm):
    """Form for test drive requests"""
    
    # Customer fields
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = forms.CharField(
        validators=[phone_regex],
        max_length=17,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+254700000000'
        })
    )
    
    driving_license_number = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your driving license number'
        }),
        help_text="Required for test drives"
    )

    class Meta:
        model = TestDrive
        fields = ['scheduled_date', 'duration_minutes', 'pickup_location', 'notes']
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'duration_minutes': forms.Select(
                choices=[(15, '15 minutes'), (30, '30 minutes'), (45, '45 minutes'), (60, '1 hour')],
                attrs={'class': 'form-select'}
            ),
            'pickup_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kai and Karo Showroom or specify preferred location'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special requests or additional information...'
            }),
        }
        labels = {
            'scheduled_date': 'Preferred Date & Time',
            'duration_minutes': 'Test Drive Duration',
            'pickup_location': 'Pickup Location',
            'notes': 'Additional Notes (Optional)'
        }

    def __init__(self, *args, **kwargs):
        self.car = kwargs.pop('car', None)
        super().__init__(*args, **kwargs)
        
        # Add Bootstrap validation classes
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs.update({'required': 'required'})

    def save(self, commit=True):
        test_drive = super().save(commit=False)
        
        if self.car:
            test_drive.car = self.car
            
        if commit:
            # Create or get customer
            customer, created = Customer.objects.get_or_create(
                email=self.cleaned_data['email'],
                defaults={
                    'first_name': self.cleaned_data['first_name'],
                    'last_name': self.cleaned_data['last_name'],
                    'phone': self.cleaned_data['phone'],
                    'driving_license_number': self.cleaned_data['driving_license_number'],
                }
            )
            
            # Update driving license if customer exists but doesn't have it
            if not customer.driving_license_number:
                customer.driving_license_number = self.cleaned_data['driving_license_number']
                customer.save()
                
            test_drive.customer = customer
            test_drive.save()
            
        return test_drive


class ContactForm(forms.Form):
    """General contact form"""
    
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('sales', 'Sales Question'),
        ('service', 'Service & Maintenance'),
        ('rental', 'Car Rental'),
        ('financing', 'Financing Options'),
        ('trade_in', 'Trade-in Valuation'),
        ('complaint', 'Complaint'),
        ('suggestion', 'Suggestion'),
    ]
    
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    
    phone = forms.CharField(
        max_length=17,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+254700000000 (Optional)'
        })
    )
    
    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='What is this regarding?'
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Please provide details about your inquiry or message...'
        }),
        label='Your Message'
    )
    
    # Optional car selection
    interested_car = forms.ModelChoiceField(
        queryset=Car.objects.filter(status='available'),
        required=False,
        empty_label="Not about a specific car",
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Specific Car (Optional)'
    )
    
    # Consent checkbox
    consent = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='I agree to be contacted regarding my inquiry'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add Bootstrap validation
        for field_name, field in self.fields.items():
            if field.required and field_name != 'consent':
                field.widget.attrs.update({'required': 'required'})

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Basic phone validation
            import re
            if not re.match(r'^\+?1?\d{9,15}$', phone):
                raise forms.ValidationError("Please enter a valid phone number.")
        return phone


class CarSearchForm(forms.Form):
    """Form for searching/filtering cars"""
    
    brand = forms.ModelChoiceField(
        queryset=None,  # Will be set in __init__
        required=False,
        empty_label="Any Brand",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    car_type = forms.ChoiceField(
        choices=[('', 'Any Type')] + Car.CAR_TYPES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Price (KES)'
        })
    )
    
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Price (KES)'
        })
    )
    
    min_year = forms.IntegerField(
        required=False,
        min_value=1990,
        max_value=2030,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Year'
        })
    )
    
    max_year = forms.IntegerField(
        required=False,
        min_value=1990,
        max_value=2030,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Year'
        })
    )
    
    transmission = forms.ChoiceField(
        choices=[('', 'Any Transmission')] + Car.TRANSMISSION_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    fuel_type = forms.ChoiceField(
        choices=[('', 'Any Fuel Type')] + Car.FUEL_TYPES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    is_for_rent = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Available for Rent'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set brand queryset
        from .models import Brand
        self.fields['brand'].queryset = Brand.objects.filter(is_active=True).order_by('name')


class NewsletterForm(forms.Form):
    """Newsletter subscription form"""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        }),
        label='Email Address'
    )
    
    consent = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='I agree to receive newsletters and promotional emails'
    )