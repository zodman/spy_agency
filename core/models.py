from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    CHOICES = (
        ('hitman', 'Hitman'),
        ('boss', 'Boss'),
        ('leader', 'Big Boss'),
    )
    STATUS = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=CHOICES)
    status = models.CharField(max_length=10, choices=STATUS, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type}"


class Hit(models.Model):
    CHOICES = (
        ('new', 'New'),
        ('assigned', 'Assigned'),
        ('failed', 'Failed'),
        ('completed', 'Completed'),
    )
    STATES = {
        'new': ['assigned',],
        'assigned': ['failed','completed']
    }
    assigned = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hits")
    description = models.TextField()
    target = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices = CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hits_created")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.id}"
