from rest_framework import permissions


class IsLoggedInAndOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        kwargs = request.parser_context['kwargs']
        user_id = str(kwargs['user_id']) if 'user_id' in kwargs \
            else str(kwargs['id'])

        return 'user_id' in request.user and user_id == request.user['user_id']


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return 'is_admin' in request.user and bool(request.user['is_admin'])


class IsAdminOrLoggedInAndOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'is_admin' in request.user and bool(request.user['is_admin']):
            return True

        kwargs = request.parser_context['kwargs']
        user_id = str(kwargs['user_id']) if 'user_id' in kwargs \
            else str(kwargs['id'])
        return 'user_id' in request.user and user_id == request.user['user_id']
