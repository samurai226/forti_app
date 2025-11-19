#!/usr/bin/env python
"""
Railway Deployment Script for FortiFun WebSocket Server
Automates deployment to Railway platform
"""
import os
import subprocess
import json
from pathlib import Path

def create_railway_config():
    """Create Railway configuration files"""
    
    # 1. Create railway.json
    railway_config = {
        "build": {
            "builder": "NIXPACKS"
        },
        "deploy": {
            "startCommand": "python manage.py runserver 0.0.0.0:$PORT",
            "healthcheckPath": "/api/v1/accounts/auth/login",
            "healthcheckTimeout": 300,
            "restartPolicyType": "ON_FAILURE",
            "restartPolicyMaxRetries": 10
        }
    }
    
    with open('railway.json', 'w') as f:
        json.dump(railway_config, f, indent=2)
    
    print("✅ Created railway.json")
    
    # 2. Create Procfile for Heroku compatibility
    with open('Procfile', 'w') as f:
        f.write('web: python manage.py runserver 0.0.0.0:$PORT\n')
    
    print("✅ Created Procfile")
    
    # 3. Create .env.example
    env_example = """# Railway Environment Variables
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=*.railway.app,*.up.railway.app

# Database (Railway provides this automatically)
DATABASE_URL=postgresql://user:pass@host:port/db

# Redis (for WebSocket channels)
REDIS_URL=redis://user:pass@host:port

# CORS Settings
CORS_ALLOWED_ORIGINS=https://*.railway.app,https://*.up.railway.app

# WebSocket Settings
CHANNEL_LAYERS=redis
WEBSOCKET_URL=wss://your-app.railway.app/ws/chat/
"""
    
    with open('.env.example', 'w') as f:
        f.write(env_example)
    
    print("✅ Created .env.example")

def create_deployment_script():
    """Create deployment script"""
    
    deploy_script = """#!/bin/bash
# Railway Deployment Script for FortiFun

echo "🚀 Deploying FortiFun WebSocket Server to Railway..."

# 1. Install Railway CLI
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# 2. Login to Railway
echo "🔐 Logging into Railway..."
railway login

# 3. Initialize project
echo "🏗️ Initializing Railway project..."
railway init

# 4. Set environment variables
echo "⚙️ Setting environment variables..."
railway variables set SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
railway variables set DEBUG=False
railway variables set ALLOWED_HOSTS="*.railway.app,*.up.railway.app"

# 5. Deploy
echo "🚀 Deploying to Railway..."
railway up

# 6. Get deployment URL
echo "🌐 Getting deployment URL..."
railway domain

echo "✅ Deployment complete!"
echo "🔗 WebSocket URL: wss://your-app.railway.app/ws/chat/"
echo "📱 Update Flutter app with new WebSocket URL"
"""
    
    with open('deploy_railway.sh', 'w') as f:
        f.write(deploy_script)
    
    # Make executable
    os.chmod('deploy_railway.sh', 0o755)
    
    print("✅ Created deploy_railway.sh")

def create_render_config():
    """Create Render configuration"""
    
    render_yaml = """services:
  - type: web
    name: fortifun-websocket
    env: python
    buildCommand: pip install -r requirements.txt && python manage.py migrate
    startCommand: python manage.py runserver 0.0.0.0:$PORT
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
      - key: ALLOWED_HOSTS
        value: "*.onrender.com"
      - key: CORS_ALLOWED_ORIGINS
        value: "https://*.onrender.com"
    healthCheckPath: /api/v1/accounts/auth/login

databases:
  - name: fortifun-db
    plan: free
    databaseName: fortifun
    user: fortifun_user
"""
    
    with open('render.yaml', 'w') as f:
        f.write(render_yaml)
    
    print("✅ Created render.yaml")

def main():
    """Main deployment setup"""
    print("🚀 Setting up FortiFun WebSocket Server for Production Deployment")
    print("=" * 70)
    
    # Create all configuration files
    create_railway_config()
    create_deployment_script()
    create_render_config()
    
    print("\n🎯 Deployment Options Ready:")
    print("1. Railway: Run 'bash deploy_railway.sh'")
    print("2. Render: Connect GitHub repo to Render")
    print("3. Heroku: Run 'git push heroku main'")
    print("4. Fly.io: Run 'fly deploy'")
    
    print("\n📱 After deployment, update Flutter app with:")
    print("   - Railway: wss://your-app.railway.app/ws/chat/")
    print("   - Render: wss://your-app.onrender.com/ws/chat/")
    print("   - Heroku: wss://your-app.herokuapp.com/ws/chat/")
    print("   - Fly.io: wss://your-app.fly.dev/ws/chat/")

if __name__ == '__main__':
    main()




