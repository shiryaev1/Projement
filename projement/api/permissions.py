from rest_framework import permissions


class IsReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method == 'GET':
            return True
