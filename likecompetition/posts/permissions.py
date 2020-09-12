from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		return request.method in permissions.SAFE_METHODS or obj.user == request.user
