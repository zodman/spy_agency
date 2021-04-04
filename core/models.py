from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .signals import registered_user


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
    type = models.CharField(max_length=10, choices=CHOICES, default="hitman")
    manages = models.ManyToManyField(User, related_name="manager")
    status = models.CharField(max_length=10, choices=STATUS, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type}"
    @property
    def is_leader(self):
        if self.type == 'leader':
            return True

    @property
    def is_boss(self):
        if self.type == "boss":
            return True

    @property
    def is_hitman(self):
        if self.type == 'hitman':
            return True
        

class Hit(models.Model):
    STATUS_COLOR = {
        'new': 'primary',
        'assigned': 'warning',
        'failed': 'danger',
        'completed': 'success',
    }
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
    status = models.CharField(max_length=10, choices = CHOICES, default='new')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hits_created")
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        ordering = ("-status",)

    @classmethod
    def next_status(cls, state):
        choices = []
        if state in cls.STATES:
            states = cls.STATES.get(state)
            choices = [(i, dict(cls.CHOICES)[i]) for i in states]
        return choices

    def get_status(self):
        return dict(self.CHOICES).get(self.status)

    @property
    def is_new(self):
        return self.status == 'new'

    @property
    def status_color(self):
        return dict(self.STATUS_COLOR).get(self.status, "aaa")

    def get_absolute_url(self):
        return reverse_lazy("hit_view", kwargs=dict(pk=self.id))

    def __str__(self):
        return f"{self.id}"
