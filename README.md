# Kai and Karo Car Dealership

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2%2B-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive car dealership management system built with Django, designed for modern automotive businesses in Kenya and beyond.

## 🚗 About Kai and Karo

Kai and Karo is a full-featured car dealership platform that handles everything from inventory management to customer relationships. Whether you're selling new cars, foreign used vehicles, or local used cars, this system provides all the tools you need to run a successful dealership.

## ✨ Features

### 🏪 **Inventory Management**
- Complete car catalog with detailed specifications
- Multiple car types: New, Foreign Used, Local Used
- Brand and model management
- Feature tracking (Interior, Safety, Technical, Extra)
- Image gallery with main image selection
- Stock number and VIN tracking

### 💰 **Sales & Pricing**
- Flexible pricing with MSRP and selling prices
- Dealer discounts and final price calculations
- Multiple payment methods (Cash, Bank Transfer, Financing, Trade-in)
- Complete sales pipeline tracking

### 🚙 **Rental Services**
- Daily, weekly, and monthly rental rates
- Rental booking management
- Security deposits and pricing calculations
- Pickup and return location tracking

### 👥 **Customer Management**
- Comprehensive customer profiles
- Inquiry tracking and management
- Test drive scheduling
- Communication preferences (Email, Phone, WhatsApp)

### 📊 **Business Operations**
- Sales reporting and analytics
- Rental booking management
- Test drive scheduling
- Customer inquiry tracking
- Blog management for marketing

### 🔧 **Technical Features**
- SEO-friendly URLs with slugs
- Meta descriptions for better search ranking
- Responsive admin interface
- UUID-based primary keys for security
- Comprehensive data validation

## 🛠️ Technology Stack

- **Backend**: Django 4.2+
- **Database**: PostgreSQL (recommended) / SQLite for development
- **Frontend**: Django Templates + Bootstrap (customizable)
- **File Storage**: Django file handling for images
- **Admin Interface**: Django Admin with custom configurations

## 📋 Requirements

- Python 3.8 or higher
- Django 4.2 or higher
- Pillow (for image handling)
- PostgreSQL (for production)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/kai-and-karo.git
cd kai-and-karo
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
MEDIA_ROOT=media/
STATIC_ROOT=staticfiles/
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Load Sample Data (Optional)
```bash
python manage.py loaddata fixtures/sample_data.json
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/admin/` to access the admin interface.

## 📊 Models Overview

### Core Models
- **Car**: Main vehicle inventory with all specifications
- **Brand**: Car manufacturers (BMW, Toyota, etc.)
- **CarModel**: Specific models (Camry, X5, etc.)
- **Category**: Vehicle categories (Sedan, SUV, Hatchback)
- **Feature**: Car features and amenities

### Business Models
- **Customer**: Client information and profiles
- **Sale**: Sales transactions and records
- **Rental**: Vehicle rental bookings
- **Inquiry**: Customer inquiries and leads
- **TestDrive**: Test drive appointments

### Content Models
- **BlogPost**: Marketing and informational content
- **CarImage**: Vehicle photo management

## 🏗️ Project Structure

```
kai-and-karo/
├── kai_karo/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── dealership/
│   ├── models.py
│   ├── admin.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
├── static/
├── media/
├── requirements.txt
└── manage.py
```

## 💼 Business Use Cases

### For Car Dealers
- Track inventory across multiple locations
- Manage customer relationships and inquiries
- Process sales from inquiry to delivery
- Handle rental operations efficiently

### For Customers
- Browse available vehicles with detailed specs
- Submit inquiries for purchase or rental
- Schedule test drives
- View transparent pricing

### For Management
- Monitor sales performance
- Track inventory turnover
- Analyze customer behavior
- Generate business reports

## 🔧 Configuration

### Settings
Key settings in `settings.py`:
```python
# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kai_karo_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Admin Customization
The admin interface is highly customized with:
- Image previews
- Inline editing for related models
- Custom list displays and filters
- Organized fieldsets for better UX

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure proper database (PostgreSQL)
- [ ] Set up media file serving (AWS S3, Cloudinary)
- [ ] Configure email backend
- [ ] Set up SSL certificates
- [ ] Configure caching (Redis)
- [ ] Set up monitoring and logging

### Environment Variables
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost/kai_karo_db
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🤝 Contributing

We welcome contributions to Kai and Karo! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation as needed
- Use meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Development Team**: Kai and Karo Tech Team
- **Location**: Nairobi, Kenya
- **Contact**: info@kaiandkaro.com

## 🆘 Support

### Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Python Documentation](https://docs.python.org/)

### Getting Help
- Create an issue on GitHub
- Email: support@kaiandkaro.com
- Phone: +254 XXX XXX XXX

## 🚗 About the Business

Kai and Karo is a trusted name in the Kenyan automotive industry, specializing in:
- New car sales from major manufacturers
- Quality foreign used vehicles
- Reliable local used cars
- Flexible rental services
- Professional automotive services

**Location**: Nairobi, Kenya  
**Established**: 2020  
**Mission**: To provide quality vehicles and exceptional service to our customers across Kenya and East Africa.

---

**Made with Steve Ongera  in Nairobi, Kenya**