from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from ..services.member_service import MemberService
from ..serializers.member_serializer import (
    MemberSerializer, 
    MemberCreateSerializer,
    MemberWithTasksSerializer
)

class MemberController:
    """
    Controller layer for Member - handles HTTP requests and responses
    Delegates business logic to service layer
    """
    
    def __init__(self):
        self.member_service = MemberService()

# Create controller instance
member_controller = MemberController()

@api_view(['GET', 'POST'])
def member_list(request):
    """
    GET /api/members/ - List all members
    POST /api/members/ - Create new member
    """
    try:
        if request.method == 'GET':
            members = member_controller.member_service.get_all_members()
            serializer = MemberSerializer(members, many=True)
            
            return Response({
                'status': 'success',
                'data': serializer.data,
                'count': len(serializer.data)
            }, status=status.HTTP_200_OK)
        
        elif request.method == 'POST':
            serializer = MemberCreateSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response({
                    'status': 'error',
                    'message': 'Validation failed',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            member = member_controller.member_service.create_member(**serializer.validated_data)
            response_serializer = MemberSerializer(member)
            
            return Response({
                'status': 'success',
                'message': 'Member created successfully',
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
def member_detail(request, member_id):
    """
    GET /api/members/{id}/ - Get member by ID
    PUT /api/members/{id}/ - Update member
    DELETE /api/members/{id}/ - Delete member
    """
    try:
        if request.method == 'GET':
            member = member_controller.member_service.get_member_by_id(member_id)
            
            if not member:
                return Response({
                    'status': 'error',
                    'message': 'Member not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = MemberSerializer(member)
            return Response({
                'status': 'success',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            # Use partial update serializer
            member = member_controller.member_service.get_member_by_id(member_id)
            if not member:
                return Response({
                    'status': 'error',
                    'message': 'Member not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = MemberCreateSerializer(data=request.data, partial=True)
            
            if not serializer.is_valid():
                return Response({
                    'status': 'error',
                    'message': 'Validation failed',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            updated_member = member_controller.member_service.update_member(member_id, **serializer.validated_data)
            
            if not updated_member:
                return Response({
                    'status': 'error',
                    'message': 'Member not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            response_serializer = MemberSerializer(updated_member)
            return Response({
                'status': 'success',
                'message': 'Member updated successfully',
                'data': response_serializer.data
            }, status=status.HTTP_200_OK)
        
        elif request.method == 'DELETE':
            deleted = member_controller.member_service.delete_member(member_id)
            
            if not deleted:
                return Response({
                    'status': 'error',
                    'message': 'Member not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            return Response({
                'status': 'success',
                'message': 'Member deleted successfully'
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
def active_members(request):
    """
    GET /api/members/active/ - Get only active members
    """
    try:
        members = member_controller.member_service.get_active_members()
        serializer = MemberSerializer(members, many=True)
        
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

@api_view(['POST'])
def deactivate_member(request, member_id):
    """
    POST /api/members/{id}/deactivate/ - Deactivate member
    """
    try:
        member = member_controller.member_service.deactivate_member(member_id)
        
        if not member:
            return Response({
                'status': 'error',
                'message': 'Member not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MemberSerializer(member)
        return Response({
            'status': 'success',
            'message': 'Member deactivated successfully',
            'data': serializer.data
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

@api_view(['POST'])
def activate_member(request, member_id):
    """
    POST /api/members/{id}/activate/ - Activate member
    """
    try:
        member = member_controller.member_service.activate_member(member_id)
        
        if not member:
            return Response({
                'status': 'error',
                'message': 'Member not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MemberSerializer(member)
        return Response({
            'status': 'success',
            'message': 'Member activated successfully',
            'data': serializer.data
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
def member_stats(request):
    """
    GET /api/members/stats/ - Get member statistics
    """
    try:
        stats = member_controller.member_service.get_member_stats()
        
        return Response({
            'status': 'success',
            'data': stats
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'status': 'error',
            'message': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    summary="Get all members with their tasks and task items",
    description="Retrieve all members with nested tasks and task items data",
    responses={200: MemberWithTasksSerializer(many=True)},
    tags=['Members', 'Tasks']
)
@api_view(['GET'])
def members_with_tasks(request):
    """
    GET /api/members/with-tasks/ - Get all members with tasks and task items
    """
    try:
        members = member_controller.member_service.get_all_members_with_tasks()
        serializer = MemberWithTasksSerializer(members, many=True)
        
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

@extend_schema(
    summary="Get member with tasks and task items by ID",
    description="Retrieve a specific member with nested tasks and task items data",
    parameters=[
        OpenApiParameter(
            name='member_id',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='Unique identifier for the member'
        ),
    ],
    responses={200: MemberWithTasksSerializer},
    tags=['Members', 'Tasks']
)
@api_view(['GET'])
def member_with_tasks_detail(request, member_id):
    """
    GET /api/members/{id}/with-tasks/ - Get member with tasks and task items by ID
    """
    try:
        member = member_controller.member_service.get_member_with_tasks_by_id(member_id)
        
        if not member:
            return Response({
                'status': 'error',
                'message': 'Member not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MemberWithTasksSerializer(member)
        return Response({
            'status': 'success',
            'data': serializer.data
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

@extend_schema(
    summary="Get active members with tasks and task items",
    description="Retrieve only active members with nested tasks and task items data",
    responses={200: MemberWithTasksSerializer(many=True)},
    tags=['Members', 'Tasks']
)
@api_view(['GET'])
def active_members_with_tasks(request):
    """
    GET /api/members/active/with-tasks/ - Get active members with tasks and task items
    """
    try:
        members = member_controller.member_service.get_active_members_with_tasks()
        serializer = MemberWithTasksSerializer(members, many=True)
        
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
