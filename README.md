# 🚀 New Revolution Backend

Robust Django REST API backend for the New Revolution marketplace platform.

## 🏗️ Tech Stack

- **Django 4.2** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Database (Supabase)
- **Redis** - Caching and real-time features
- **Celery** - Background tasks
- **Channels** - WebSocket support
- **JWT** - Authentication
- **Cloudinary** - File storage
- **Resend** - Email service
- **Stripe** - Payment processing

## 🚀 Quick Start

### Local Development

1. **Clone and setup**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Environment setup**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Database setup**:
```bash
python manage.py migrate
python manage.py createsuperuser
```

4. **Run development server**:
```bash
python manage.py runserver
```

### Render.com Deployment

1. **Connect your GitHub repository to Render**
2. **Create a new Web Service**
3. **Configure settings**:
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn newrevolution.wsgi:application`
   - **Environment**: Python 3.11

4. **Add environment variables**:
```env
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://postgres.sbykzpirrgeceecxvpvc:password@aws-0-us-west-1.pooler.supabase.com:6543/postgres
RESEND_API_KEY=re_Gca9oy8H_CCEZJoVtjEAtqh3WK68YDnRY
FRONTEND_DOMAIN=https://newrevolution.netlify.app
DEBUG=False
```

## 📊 API Endpoints

### Authentication
- `POST /api/v1/auth/register/` - User registration
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/logout/` - User logout
- `POST /api/v1/auth/token/refresh/` - Refresh JWT token
- `GET /api/v1/auth/profile/` - Get user profile
- `PUT /api/v1/auth/profile/` - Update user profile

### Products
- `GET /api/v1/products/` - List products
- `POST /api/v1/products/` - Create product
- `GET /api/v1/products/{id}/` - Get product details
- `PUT /api/v1/products/{id}/` - Update product
- `DELETE /api/v1/products/{id}/` - Delete product
- `GET /api/v1/products/my-products/` - Get user's products
- `GET /api/v1/products/featured/` - Get featured products

### Categories
- `GET /api/v1/categories/` - List categories
- `GET /api/v1/categories/tree/` - Get category tree

### Reviews
- `GET /api/v1/reviews/` - List reviews
- `POST /api/v1/reviews/` - Create review

### Chat
- `GET /api/v1/chat/conversations/` - List conversations
- `POST /api/v1/chat/conversations/` - Create conversation
- `GET /api/v1/chat/conversations/{id}/messages/` - Get messages

### Payments
- `POST /api/v1/payments/create-intent/` - Create payment intent
- `GET /api/v1/payments/boost-packages/` - Get boost packages

### Notifications
- `GET /api/v1/notifications/` - List notifications
- `POST /api/v1/notifications/{id}/mark-read/` - Mark as read

## 🔧 Configuration

### Required Environment Variables

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,.onrender.com

# Database (Supabase)
DATABASE_URL=postgresql://postgres.sbykzpirrgeceecxvpvc:password@aws-0-us-west-1.pooler.supabase.com:6543/postgres

# Email (Resend)
RESEND_API_KEY=re_Gca9oy8H_CCEZJoVtjEAtqh3WK68YDnRY
DEFAULT_FROM_EMAIL=noreply@newrevolution.com

# File Storage (Cloudinary)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Frontend
FRONTEND_DOMAIN=https://newrevolution.netlify.app
```

## 🏗️ Architecture

### Apps Structure
```
apps/
├── accounts/          # User management
├── products/          # Product listings
├── categories/        # Product categories
├── reviews/           # Review system
├── chat/              # Real-time messaging
├── payments/          # Payment processing
├── notifications/     # Notification system
└── core/              # Shared utilities
```

### Models Overview

**User Model**:
- Custom user with email authentication
- Profile information and preferences
- Seller status and ratings
- Verification and ban system

**Product Model**:
- Comprehensive product information
- Image handling with Cloudinary
- Category and tagging system
- Boost and featured listings

**Chat System**:
- Real-time messaging with WebSockets
- Conversation management
- Message history and status

## 🔒 Security Features

- **JWT Authentication** - Secure token-based auth
- **Rate Limiting** - API abuse prevention
- **Input Validation** - Comprehensive data validation
- **CORS Protection** - Proper cross-origin configuration
- **SQL Injection Protection** - Django ORM safety
- **XSS Protection** - Input sanitization
- **HTTPS Enforcement** - Secure communications

## 📈 Performance

- **Database Optimization** - Indexed queries and select_related
- **Caching** - Redis-powered caching layer
- **Image Optimization** - Cloudinary processing
- **Background Tasks** - Celery for heavy operations
- **Connection Pooling** - Efficient database connections

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 📝 Logging

Comprehensive logging configuration:
- **Console logging** for development
- **File logging** for production
- **Sentry integration** for error tracking
- **Activity logging** for user actions

## 🔧 Management Commands

```bash
# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run migrations
python manage.py migrate

# Clear cache
python manage.py shell -c "from django.core.cache import cache; cache.clear()"
```

## 📊 Monitoring

- **Health Check**: `/health/` endpoint
- **Admin Interface**: `/admin/`
- **API Root**: `/api/v1/`
- **Sentry Error Tracking** (optional)

## 🚀 Production Deployment

### Render.com Setup

1. **Create Web Service** from GitHub repository
2. **Set root directory** to `backend`
3. **Configure build command**: `./build.sh`
4. **Configure start command**: `gunicorn newrevolution.wsgi:application`
5. **Add environment variables** from `.env.example`

### Database Setup (Supabase)

1. **Create Supabase project**
2. **Get connection string**
3. **Add to DATABASE_URL environment variable**
4. **Run migrations** via build script

### File Storage (Cloudinary)

1. **Create Cloudinary account**
2. **Get API credentials**
3. **Add to environment variables**
4. **Configure upload settings**

## 📞 Support

- **Health Check**: `GET /health/`
- **API Documentation**: `GET /api/v1/`
- **Admin Panel**: `/admin/`

---

**Built with ❤️ for New Revolution**