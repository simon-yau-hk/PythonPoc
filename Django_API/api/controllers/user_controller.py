from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from ..services.user_service import UserService
from ..serializers.user_serializer import (
    UserSerializer, 
    UserCreateSerializer, 
    UserUpdateSerializer
)

class UserController:
    """
    Controller layer - handles HTTP requests and responses
    Delegates business logic to service layer
    """
    
    def __init__(self):
        self.user_service = UserService()

# Create controller instance
user_controller = UserController()

@api_view(['GET', 'POST'])
def user_list(request):
    """
    GET /api/users/ - List all users
    POST /api/users/ - Create new user
    """
    try:
        if request.method == 'GET':
            users = user_controller.user_service.get_all_users()
            serializer = UserSerializer(users, many=True)
            
            return Response({
                'status': 'success',
                'data': serializer.data,
                'count': len(serializer.data)
            }, status=status.HTTP_200_OK)
        
        elif request.method == 'POST':
            serializer = UserCreateSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response({
                    'status': 'error',
                    'message': 'Validation failed',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = user_controller.user_service.create_user(**serializer.validated_data)
            response_serializer = UserSerializer(user)
            
            return Response({
                'status': 'success',
                'message': 'User created successfully',
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
    
    except ValidationError as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'status': 'error',
            'message': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, user_id):
    """
    GET /api/users/{id}/ - Get user by ID
    PUT /api/users/{id}/ - Update user
    DELETE /api/users/{id}/ - Delete user
    """
    try:
        if request.method == 'GET':
            user = user_controller.user_service.get_user_by_id(user_id)
            
            if not user:
                return Response({
                    'status': 'error',
                    'message': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = UserSerializer(user)
            return Response({
                'status': 'success',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            serializer = UserUpdateSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response({
                    'status': 'error',
                    'message': 'Validation failed',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = user_controller.user_service.update_user(user_id, **serializer.validated_data)
            
            if not user:
                return Response({
                    'status': 'error',
                    'message': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            response_serializer = UserSerializer(user)
            return Response({
                'status': 'success',
                'message': 'User updated successfully',
                'data': response_serializer.data
            }, status=status.HTTP_200_OK)
        
        elif request.method == 'DELETE':
            deleted = user_controller.user_service.delete_user(user_id)
            
            if not deleted:
                return Response({
                    'status': 'error',
                    'message': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            return Response({
                'status': 'success',
                'message': 'User deleted successfully'
            }, status=status.HTTP_200_OK)
    
    except ValidationError as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'status': 'error',
            'message': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def active_users(request):
    """
    GET /api/users/active/ - Get only active users
    """
    try:
        users = user_controller.user_service.get_active_users()
        serializer = UserSerializer(users, many=True)
        
        return Response({
            'status': 'success',
            'data': serializer.data,
            'count': len(serializer.data)
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'status': 'error',
            'message': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def user_stats(request):
    """
    GET /api/users/stats/ - Get user statistics
    """
    try:
        stats = user_controller.user_service.get_user_stats()
        
        return Response({
            'status': 'success',
            'data': stats
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'status': 'error',
            'message': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
