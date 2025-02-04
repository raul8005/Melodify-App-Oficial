
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

# Decorador para restringir el acceso según el tipo de usuario
def user_type_required(user_type):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.user_type != user_type:
                return redirect('users:dashboard')  # Redirige al dashboard si el tipo de usuario no coincide
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
