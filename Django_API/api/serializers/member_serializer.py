from rest_framework import serializers
from ..entities.entity import Member, Task, TaskItem

class TaskItemSerializer(serializers.ModelSerializer):
    """Serializer for TaskItem model"""
    
    class Meta:
        model = TaskItem
        fields = ['id', 'title', 'description', 'is_completed', 'order', 
                 'created_at', 'updated_at', 'completed_at']

class TaskWithItemsSerializer(serializers.ModelSerializer):
    """Serializer for Task model with nested task items"""
    task_items = TaskItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'status', 'due_date', 
                 'created_at', 'updated_at', 'task_items']

class MemberWithTasksSerializer(serializers.ModelSerializer):
    """Serializer for Member model with nested tasks and task items"""
    tasks = TaskWithItemsSerializer(many=True, read_only=True)
    task_count = serializers.SerializerMethodField()
    completed_tasks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Member
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 
                 'created_at', 'updated_at', 'tasks', 'task_count', 'completed_tasks_count']
    
    def get_task_count(self, obj):
        """Get total number of tasks for this member"""
        return obj.tasks.count()
    
    def get_completed_tasks_count(self, obj):
        """Get number of completed tasks for this member"""
        return obj.tasks.filter(status='completed').count()

class MemberSerializer(serializers.ModelSerializer):
    """Serializer for Member model"""
    
    class Meta:
        model = Member
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class MemberCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating members"""
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = Member
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model"""
    member = MemberSerializer(read_only=True)
    member_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'status', 'due_date', 
                 'created_at', 'updated_at', 'member', 'member_id']
        read_only_fields = ['id', 'created_at', 'updated_at']

class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tasks"""
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status', 'due_date', 'member_id']

        
class TaskItemSerializer(serializers.ModelSerializer):
    """Serializer for TaskItem model"""
    task = TaskSerializer(read_only=True)
    task_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = TaskItem
        fields = ['id', 'title', 'description', 'is_completed', 'order', 
                 'created_at', 'updated_at', 'completed_at', 'task', 'task_id']
        read_only_fields = ['id', 'created_at', 'updated_at', 'completed_at']

class TaskItemCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating task items"""
    
    class Meta:
        model = TaskItem
        fields = ['title', 'description', 'order', 'task_id']