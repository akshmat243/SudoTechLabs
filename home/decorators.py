from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def superuser_required(view_func):
    """
    Allows access only to superusers.
    """
    @login_required(login_url='login')
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def admin_required(view_func):
    """
    Allows access only to staff users (admin users).
    """
    @login_required(login_url='login')
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_admin:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def teamleader_required(view_func):
    """
    Allows access only to staff users (admin users).
    """
    @login_required(login_url='login')
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_team_leader:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def staff_required(view_func):
    """
    Allows access only to staff users (admin users).
    """
    @login_required(login_url='login')
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff_new:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view