# 🚀 FortiFun WebSocket Server - Free Deployment Guide

## 🎯 **Best Free WebSocket Hosting Options**

### **1. Railway (Recommended) - $5/month credit (effectively free)**

#### **Setup Steps:**
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login to Railway
railway login

# 3. Initialize project
railway init

# 4. Deploy
railway up
```

#### **Environment Variables:**
- `SECRET_KEY`: Auto-generated
- `DEBUG`: False
- `ALLOWED_HOSTS`: `*.railway.app,*.up.railway.app`
- `DATABASE_URL`: Auto-provided by Railway
- `REDIS_URL`: Auto-provided by Railway

#### **WebSocket URL:**
```
wss://your-app.railway.app/ws/chat/?token={jwt_token}
```

---

### **2. Render (750 hours/month free)**

#### **Setup Steps:**
1. Connect GitHub repo to Render
2. Set build command: `pip install -r requirements.txt && python manage.py migrate`
3. Set start command: `python manage.py runserver 0.0.0.0:$PORT`

#### **Environment Variables:**
- `SECRET_KEY`: Generate new key
- `DEBUG`: False
- `ALLOWED_HOSTS`: `*.onrender.com`
- `DATABASE_URL`: Auto-provided by Render

#### **WebSocket URL:**
```
wss://your-app.onrender.com/ws/chat/?token={jwt_token}
```

---

### **3. Heroku (550-1000 hours/month free)**

#### **Setup Steps:**
```bash
# 1. Install Heroku CLI
# 2. Login to Heroku
heroku login

# 3. Create app
heroku create your-fortifun-app

# 4. Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# 5. Deploy
git push heroku main
```

#### **WebSocket URL:**
```
wss://your-app.herokuapp.com/ws/chat/?token={jwt_token}
```

---

### **4. Fly.io (3 shared-cpu VMs free)**

#### **Setup Steps:**
```bash
# 1. Install Fly CLI
# 2. Login
fly auth login

# 3. Launch app
fly launch

# 4. Deploy
fly deploy
```

#### **WebSocket URL:**
```
wss://your-app.fly.dev/ws/chat/?token={jwt_token}
```

---

## 🔧 **Flutter App Configuration**

### **Update WebSocket URLs in Flutter:**

#### **1. Update DjangoService:**
```dart
// lib/app/core/services/django_service.dart
class DjangoService {
  // Production URLs
  static const String baseUrl = 'https://your-app.railway.app';
  static const String wsUrl = 'wss://your-app.railway.app/ws/chat/';
  
  // For other platforms, replace with:
  // Render: 'https://your-app.onrender.com'
  // Heroku: 'https://your-app.herokuapp.com'
  // Fly.io: 'https://your-app.fly.dev'
}
```

#### **2. Update UnifiedWebSocketService:**
```dart
// lib/app/core/services/unified_websocket_service.dart
class UnifiedWebSocketService {
  String _getWebSocketUrl() {
    return 'wss://your-app.railway.app/ws/chat/?token=${_authController.accessToken}';
  }
}
```

---

## 📱 **Testing WebSocket Connection**

### **1. Test with Flutter App:**
```dart
// In your Flutter app, test the connection:
final websocketService = Get.find<UnifiedWebSocketService>();
await websocketService.connect();
```

### **2. Test with Browser:**
```javascript
// Open browser console and test:
const ws = new WebSocket('wss://your-app.railway.app/ws/chat/?token=YOUR_JWT_TOKEN');
ws.onopen = () => console.log('Connected!');
ws.onmessage = (event) => console.log('Message:', event.data);
```

---

## 🎯 **Recommended Deployment Strategy**

### **For Development:**
- Use **Railway** (easiest setup, good free tier)

### **For Production:**
- Use **Render** (reliable, good performance)
- Or **Fly.io** (fast, global CDN)

### **For Testing:**
- Use **Heroku** (familiar, easy to debug)

---

## 🔧 **Quick Start Commands**

### **Railway (Recommended):**
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login and deploy
railway login
railway init
railway up

# 3. Get your URL
railway domain
```

### **Render:**
1. Connect GitHub repo to Render
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `python manage.py runserver 0.0.0.0:$PORT`
4. Deploy automatically

---

## 📊 **WebSocket Endpoints Ready:**

- **Main Chat**: `wss://your-app.railway.app/ws/chat/?token={token}`
- **Conversations**: `wss://your-app.railway.app/ws/conversations/{id}/?token={token}`
- **Anonymous Chat**: `wss://your-app.railway.app/ws/anonymous_chat/{room_id}/`

---

## 🚀 **Next Steps:**

1. **Choose a platform** (Railway recommended)
2. **Deploy your Django app**
3. **Update Flutter app** with new WebSocket URLs
4. **Test the connection** with your Flutter app
5. **Monitor performance** and scale as needed

Your WebSocket system is fully implemented and ready for production! 🎉




