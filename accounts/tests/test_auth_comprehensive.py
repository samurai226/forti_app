# accounts/tests/test_auth_comprehensive.py

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
import json

User = get_user_model()

class AuthComprehensiveTestCase(APITestCase):
    """Comprehensive authentication tests"""
    
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test User'
        }
        self.login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
    
    def test_user_registration(self):
        """Test user registration endpoint"""
        url = reverse('auth-register')
        response = self.client.post(url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        
        # Verify user was created
        user = User.objects.get(email=self.user_data['email'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
    
    def test_user_login(self):
        """Test user login endpoint"""
        # Create user first
        user = User.objects.create_user(
            username='testuser',
            email=self.user_data['email'],
            password=self.user_data['password'],
            first_name='Test',
            last_name='User'
        )
        
        url = reverse('auth-login')
        response = self.client.post(url, self.login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
    
    def test_user_profile_get(self):
        """Test getting user profile"""
        user = User.objects.create_user(
            username='testuser',
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        
        # Get JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        # Test authenticated request
        url = reverse('users-me')
        response = self.client.get(
            url, 
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], user.email)
    
    def test_user_profile_update(self):
        """Test updating user profile"""
        user = User.objects.create_user(
            username='testuser',
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        
        # Get JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        # Update profile
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'bio': 'Updated bio'
        }
        
        url = reverse('users-me')
        response = self.client.put(
            url, 
            data=json.dumps(update_data),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify update
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Updated')
        self.assertEqual(user.last_name, 'Name')
    
    def test_token_refresh(self):
        """Test token refresh endpoint"""
        user = User.objects.create_user(
            username='testuser',
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        
        # Get refresh token
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        
        url = reverse('auth-refresh')
        response = self.client.post(
            url, 
            data={'refresh': refresh_token},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('user', response.data)
    
    def test_logout(self):
        """Test logout endpoint"""
        user = User.objects.create_user(
            username='testuser',
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        
        # Get JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        url = reverse('auth-logout')
        response = self.client.post(
            url,
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Logout successful', response.data['detail'])
    
    def test_invalid_credentials(self):
        """Test login with invalid credentials"""
        url = reverse('auth-login')
        invalid_data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('invalid credentials', response.data['detail'])
    
    def test_duplicate_registration(self):
        """Test registration with existing email"""
        # Create user first
        User.objects.create_user(
            username='testuser',
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        
        url = reverse('auth-register')
        response = self.client.post(url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email already registered', response.data['detail'])
    
    def test_missing_required_fields(self):
        """Test registration with missing fields"""
        url = reverse('auth-register')
        incomplete_data = {
            'email': 'test@example.com'
            # Missing password and name
        }
        
        response = self.client.post(url, incomplete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email and password required', response.data['detail'])
    
    def test_unauthorized_access(self):
        """Test accessing protected endpoint without token"""
        url = reverse('users-me')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_invalid_token(self):
        """Test accessing protected endpoint with invalid token"""
        url = reverse('users-me')
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION='Bearer invalid_token'
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)





