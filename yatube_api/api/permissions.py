from rest_framework import permissions


class CanViewGroup(permissions.BasePermission):

    def has_permission(self, request, view):
        return True


class CanManagePost(permissions.BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
