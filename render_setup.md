# 🚀 FortiFun WebSocket Server - Render Deployment

## 📋 **Render Setup Steps**

### **1. Create Render Account**
- Go to [render.com](https://render.com)
- Sign up with GitHub
- Connect your repository

### **2. Deploy Web Service**
- Click "New +" → "Web Service"
- Connect your GitHub repo: `forti_app`
- Use these settings:

#### **Build Settings:**
```
Build Command: pip install -r requirements.txt && python manage.py migrate
Start Command: python manage.py runserver 0.0.0.0:$PORT
```

#### **Environment Variables:**
```
SECRET_KEY = [Generate new secret key]
DEBUG = False
ALLOWED_HOSTS = *.onrender.com
CORS_ALLOWED_ORIGINS = https://*.onrender.com
DATABASE_URL = [Auto-provided by Render]
REDIS_URL = [Auto-provided by Render]
```

### **3. Add PostgreSQL Database**
- Click "New +" → "PostgreSQL"
- Name: `fortifun-db`
- Plan: `Free`
- Connect to your web service

### **4. Deploy**
- Click "Deploy Web Service"
- Wait for build to complete
- Get your URL: `https://your-app.onrender.com`

## 🔧 **WebSocket URLs After Deployment:**

```
Main Chat: wss://your-app.onrender.com/ws/chat/?token={jwt_token}
Conversations: wss://your-app.onrender.com/ws/conversations/{id}/?token={jwt_token}
Anonymous Chat: wss://your-app.onrender.com/ws/anonymous_chat/{room_id}/
```

## 📱 **Flutter App Updates:**

### **Update DjangoService:**
```dart
// lib/app/core/services/django_service.dart
class DjangoService {
  static const String baseUrl = 'https://your-app.onrender.com';
  static const String wsUrl = 'wss://your-app.onrender.com/ws/chat/';
}
```

### **Update UnifiedWebSocketService:**
```dart
// lib/app/core/services/unified_websocket_service.dart
String _getWebSocketUrl() {
  return 'wss://your-app.onrender.com/ws/chat/?token=${_authController.accessToken}';
}
```

## 🧪 **Test WebSocket Connection:**

### **1. Browser Test:**
```javascript
// Open browser console and test:
const ws = new WebSocket('wss://your-app.onrender.com/ws/chat/?token=YOUR_JWT_TOKEN');
ws.onopen = () => console.log('✅ Connected to Render WebSocket!');
ws.onmessage = (event) => console.log('📥 Message:', event.data);
```

### **2. Flutter Test:**
```dart
// In your Flutter app:
final websocketService = Get.find<UnifiedWebSocketService>();
await websocketService.connect();
```

## 🎯 **Render Advantages:**

✅ **Free Tier**: 750 hours/month  
✅ **WebSocket Support**: Full support  
✅ **Auto-Deploy**: Git-based deployments  
✅ **PostgreSQL**: Free database included  
✅ **SSL**: Automatic HTTPS/WSS  
✅ **Global CDN**: Fast worldwide  

## 🚀 **Deployment Checklist:**

- [ ] Create Render account
- [ ] Connect GitHub repository
- [ ] Deploy web service
- [ ] Add PostgreSQL database
- [ ] Update Flutter app URLs
- [ ] Test WebSocket connection
- [ ] Deploy Flutter app

## 📊 **Expected Performance:**

- **Build Time**: 2-5 minutes
- **Cold Start**: 10-30 seconds
- **WebSocket Latency**: <100ms
- **Uptime**: 99.9%

Your FortiFun WebSocket server will be live on Render! 🎉




