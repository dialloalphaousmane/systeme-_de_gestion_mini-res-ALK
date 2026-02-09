from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Allows access only to admin users or for read-only requests.
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and request.user.is_staff
        )

class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to only allow owners of an object or admin users to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # For the CustomUser model, the object is the user.
        # So we check if the object being accessed is the same as the request user.
        return obj == request.user or request.user.is_staff

# Note: IsAdminUser is already available in rest_framework.permissions, so we don't need to redefine it.
# We just need to make sure it's imported correctly where it's used.