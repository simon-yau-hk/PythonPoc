from django.urls import path
from . import views
from .controllers.user_controller import user_list, user_detail, active_users, user_stats
from .controllers.member_controller import (
    member_list, member_detail, active_members, 
    deactivate_member, activate_member, member_stats,
    members_with_tasks, member_with_tasks_detail, active_members_with_tasks  # Add these
)

urlpatterns = [
    # Original test endpoint
    path('test/', views.hello_world, name='hello_world'),
    
    # User management endpoints (Controller-Service-Repository pattern)
    path('users/', user_list, name='user_list'),
    path('users/<int:user_id>/', user_detail, name='user_detail'),
    path('users/active/', active_users, name='active_users'),
    path('users/stats/', user_stats, name='user_stats'),
    
  # Member management endpoints
    path('members/', member_list, name='member_list'),
    path('members/<int:member_id>/', member_detail, name='member_detail'),
    path('members/active/', active_members, name='active_members'),
    path('members/<int:member_id>/deactivate/', deactivate_member, name='deactivate_member'),
    path('members/<int:member_id>/activate/', activate_member, name='activate_member'),
    path('members/stats/', member_stats, name='member_stats'),
    
    # New nested endpoints
    path('members/with-tasks/', members_with_tasks, name='members_with_tasks'),
    path('members/<int:member_id>/with-tasks/', member_with_tasks_detail, name='member_with_tasks_detail'),
    path('members/active/with-tasks/', active_members_with_tasks, name='active_members_with_tasks'),
]
