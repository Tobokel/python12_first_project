from rest_framework.permissions import BasePermission


class IsAuthorOrIsAdmin(BasePermission):
    # create, list
    # def has_permission(self, request, view):

    # update, partial, destroy, retrieve
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user == obj.author



