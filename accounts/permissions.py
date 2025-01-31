from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == "Admin"

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == "Student"
