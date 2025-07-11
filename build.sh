#!/usr/bin/env bash
# Build script for Render.com deployment
set -o errexit

echo "🚀 Starting New Revolution Backend Build..."

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
mkdir -p staticfiles
mkdir -p logs

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "👤 Setting up admin user..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        email='admin@newrevolution.com',
        username='admin',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print('✅ Superuser created: admin@newrevolution.com / admin123')
else:
    print('✅ Superuser already exists')
"

echo "🎉 Build completed successfully!"