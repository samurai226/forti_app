#!/bin/bash
# FortiFun WebSocket Server - Render Deployment Script

echo "🚀 Deploying FortiFun WebSocket Server to Render..."
echo "=================================================="

# 1. Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Are you in the correct directory?"
    exit 1
fi

# 2. Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# 3. Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# 4. Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# 5. Create superuser (optional)
echo "👤 Creating superuser (optional)..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@fortifun.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

# 6. Test the server
echo "🧪 Testing server startup..."
timeout 10s python manage.py runserver 0.0.0.0:8000 &
SERVER_PID=$!
sleep 5
kill $SERVER_PID 2>/dev/null

echo "✅ Render deployment preparation complete!"
echo ""
echo "🎯 Next Steps:"
echo "1. Push your code to GitHub"
echo "2. Connect your repo to Render"
echo "3. Use these settings in Render:"
echo "   - Build Command: pip install -r requirements.txt && python manage.py migrate"
echo "   - Start Command: python manage.py runserver 0.0.0.0:\$PORT"
echo "4. Add environment variables:"
echo "   - SECRET_KEY: [Generate new key]"
echo "   - DEBUG: False"
echo "   - ALLOWED_HOSTS: *.onrender.com"
echo "5. Add PostgreSQL database"
echo "6. Deploy!"
echo ""
echo "🌐 Your WebSocket URL will be:"
echo "   wss://your-app.onrender.com/ws/chat/?token={jwt_token}"




