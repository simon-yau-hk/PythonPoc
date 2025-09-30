from django.db import models
from django.utils import timezone

class Member(models.Model):
    """
    Member model - represents users in the system
    """
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    password_hash = models.CharField(max_length=128)  # Store hashed password
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'members'
        ordering = ['username']
    
    def __str__(self):
        return self.username

class Task(models.Model):
    """
    Task model - belongs to a member
    """
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Foreign Key relationship - Task belongs to Member
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='tasks')
    
    class Meta:
        db_table = 'tasks'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.member.username}"

class TaskItem(models.Model):
    """
    TaskItem model - subtasks/checklist items for a task
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    order = models.IntegerField(default=0)  # For ordering items
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Foreign Key relationship - TaskItem belongs to Task
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_items')
    
    class Meta:
        db_table = 'task_items'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.title} - {self.task.title}"
    
    def save(self, *args, **kwargs):
        """Override save to set completed_at timestamp"""
        if self.is_completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.is_completed:
            self.completed_at = None
        super().save(*args, **kwargs)