# accounts/device_token_views.py

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import DeviceToken
from .serializers import DeviceTokenSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_device_token(request):
    """Register a new device token for push notifications"""
    try:
        device_token = request.data.get('device_token')
        device_type = request.data.get('device_type', 'unknown')
        app_version = request.data.get('app_version', '1.0.0')
        
        if not device_token:
            return Response(
                {'error': 'device_token is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if token already exists
        existing_token = DeviceToken.objects.filter(
            device_token=device_token,
            user=request.user
        ).first()
        
        if existing_token:
            # Update existing token
            existing_token.device_type = device_type
            existing_token.app_version = app_version
            existing_token.is_active = True
            existing_token.updated_at = timezone.now()
            existing_token.save()
            
            return Response({
                'message': 'Device token updated successfully',
                'token_id': existing_token.id
            })
        else:
            # Create new token
            new_token = DeviceToken.objects.create(
                user=request.user,
                device_token=device_token,
                device_type=device_type,
                app_version=app_version,
                is_active=True
            )
            
            return Response({
                'message': 'Device token registered successfully',
                'token_id': new_token.id
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_device_token(request):
    """Update an existing device token"""
    try:
        device_token = request.data.get('device_token')
        device_type = request.data.get('device_type')
        app_version = request.data.get('app_version')
        
        if not device_token:
            return Response(
                {'error': 'device_token is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find the token
        token_obj = DeviceToken.objects.filter(
            device_token=device_token,
            user=request.user
        ).first()
        
        if not token_obj:
            return Response(
                {'error': 'Device token not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Update fields
        if device_type:
            token_obj.device_type = device_type
        if app_version:
            token_obj.app_version = app_version
        
        token_obj.updated_at = timezone.now()
        token_obj.save()
        
        return Response({
            'message': 'Device token updated successfully',
            'token_id': token_obj.id
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unregister_device_token(request):
    """Unregister a device token"""
    try:
        device_token = request.data.get('device_token')
        
        if not device_token:
            return Response(
                {'error': 'device_token is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find and deactivate the token
        token_obj = DeviceToken.objects.filter(
            device_token=device_token,
            user=request.user
        ).first()
        
        if token_obj:
            token_obj.is_active = False
            token_obj.save()
            return Response({'message': 'Device token unregistered successfully'})
        else:
            return Response(
                {'error': 'Device token not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_device_tokens(request):
    """Get all device tokens for the current user"""
    try:
        tokens = DeviceToken.objects.filter(
            user=request.user,
            is_active=True
        ).order_by('-created_at')
        
        serializer = DeviceTokenSerializer(tokens, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )






