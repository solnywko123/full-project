from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission


class IsOwnerOrAuthor(BasePermission):
    def has_permission(self, request, view, obj):
        user = request.user
        return user == obj.author or user == obj.owner
