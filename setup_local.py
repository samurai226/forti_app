#!/usr/bin/env python3
"""
Django Backend Local Setup Script
Automates the setup process for local development
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def run_command(command, description, check=True):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(f"✅ {description} completed")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported. Please use Python 3.8+")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def setup_virtual_environment():
    """Set up virtual environment"""
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    print("📦 Creating virtual environment...")
    return run_command("python -m venv venv", "Creating virtual environment")

def activate_venv_and_install():
    """Activate virtual environment and install dependencies"""
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # Install dependencies
    install_cmd = f"{pip_cmd} install -r requirements.txt"
    return run_command(install_cmd, "Installing Python dependencies")

def setup_database():
    """Set up database and run migrations"""
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/Mac
        python_cmd = "venv/bin/python"
    
    # Run migrations
    migrate_cmd = f"{python_cmd} manage.py migrate"
    if not run_command(migrate_cmd, "Running database migrations"):
        return False
    
    # Create superuser (optional)
    print("👤 Creating superuser (optional)...")
    create_superuser_cmd = f"{python_cmd} manage.py createsuperuser --noinput --username admin --email admin@example.com"
    run_command(create_superuser_cmd, "Creating superuser", check=False)
    
    return True

def check_redis():
    """Check if Redis is available"""
    print("🔍 Checking Redis availability...")
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
        print("✅ Redis is running and accessible")
        return True
    except ImportError:
        print("⚠️ Redis package not installed, will use in-memory channel layer")
        return False
    except Exception as e:
        print(f"⚠️ Redis not available: {e}")
        print("   Will use in-memory channel layer (limited functionality)")
        return False

def create_test_data():
    """Create test data for development"""
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/Mac
        python_cmd = "venv/bin/python"
    
    # Create test users and conversations
    print("📊 Creating test data...")
    test_data_script = """
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from conversations.models import Conversation, Message
from matching.models import UserPreference, UserInterest, Interest

User = get_user_model()

# Create test users
try:
    user1, created = User.objects.get_or_create(
        username='testuser1',
        defaults={
            'email': 'testuser1@example.com',
            'first_name': 'Test',
            'last_name': 'User1',
            'bio': 'Test user 1 for development'
        }
    )
    if created:
        user1.set_password('password123')
        user1.save()
        print('✅ Created test user 1')
    
    user2, created = User.objects.get_or_create(
        username='testuser2',
        defaults={
            'email': 'testuser2@example.com',
            'first_name': 'Test',
            'last_name': 'User2',
            'bio': 'Test user 2 for development'
        }
    )
    if created:
        user2.set_password('password123')
        user2.save()
        print('✅ Created test user 2')
    
    # Create test conversation
    conversation, created = Conversation.objects.get_or_create(
        id=1,
        defaults={'is_active': True}
    )
    if created:
        conversation.participants.add(user1, user2)
        print('✅ Created test conversation')
    
    # Create test message
    if not Message.objects.filter(conversation=conversation).exists():
        Message.objects.create(
            conversation=conversation,
            sender=user1,
            content='Hello! This is a test message.'
        )
        print('✅ Created test message')
    
    print('✅ Test data setup completed')
    
except Exception as e:
    print(f'❌ Error creating test data: {e}')
"""
    
    # Write and run the test data script
    with open('create_test_data.py', 'w') as f:
        f.write(test_data_script)
    
    run_command(f"{python_cmd} create_test_data.py", "Creating test data")
    
    # Clean up
    os.remove('create_test_data.py')

def print_startup_instructions():
    """Print instructions for starting the server"""
    print("\n" + "="*60)
    print("🚀 SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\n📋 Next Steps:")
    print("\n1. Start the Django server with WebSocket support:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\daphne -b 127.0.0.1 -p 8000 chat_api.asgi:application")
    else:  # Unix/Linux/Mac
        print("   venv/bin/daphne -b 127.0.0.1 -p 8000 chat_api.asgi:application")
    
    print("\n2. Test WebSocket connections:")
    print("   - Open websocket_test_client.html in your browser")
    print("   - Or run: python test_websocket_client.py")
    
    print("\n3. API Endpoints:")
    print("   - REST API: http://127.0.0.1:8000/")
    print("   - WebSocket: ws://127.0.0.1:8000/ws/")
    print("   - Admin: http://127.0.0.1:8000/admin/")
    print("     Username: admin, Password: (check console output)")
    
    print("\n4. Test Users (for authentication):")
    print("   - Username: testuser1, Password: password123")
    print("   - Username: testuser2, Password: password123")
    
    print("\n🔧 Troubleshooting:")
    print("   - If Redis is not available, the app will use in-memory channel layer")
    print("   - Check logs for any errors")
    print("   - Make sure port 8000 is not in use")
    
    print("\n" + "="*60)

def main():
    """Main setup function"""
    print("🔧 Django Backend Local Setup")
    print("="*50)
    
    # Check if we're in the right directory
    if not Path("manage.py").exists():
        print("❌ manage.py not found. Please run this script from the Django project root.")
        return False
    
    # Step 1: Check Python version
    if not check_python_version():
        return False
    
    # Step 2: Setup virtual environment
    if not setup_virtual_environment():
        return False
    
    # Step 3: Install dependencies
    if not activate_venv_and_install():
        return False
    
    # Step 4: Setup database
    if not setup_database():
        return False
    
    # Step 5: Check Redis
    check_redis()
    
    # Step 6: Create test data
    create_test_data()
    
    # Step 7: Print instructions
    print_startup_instructions()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 Setup completed successfully!")
        else:
            print("\n❌ Setup failed. Please check the errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)






