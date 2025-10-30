from rest_framework import permissions

class IsOrganizerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: only the event organizer can edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = GET, HEAD, OPTIONS (read-only)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only the organizer can modify/delete
        return obj.organizer == request.user


class IsInvitedOrPublicEvent(permissions.BasePermission):
    """
    Custom permission: private events are only accessible to invited users.
    """

    def has_object_permission(self, request, view, obj):
        # Public events are accessible to everyone
        if obj.is_public:
            return True
        
        # Organizer always has access
        if obj.organizer == request.user:
            return True

        # Check if user is in invited list
        return obj.rsvp_set.filter(user=request.user).exists()
