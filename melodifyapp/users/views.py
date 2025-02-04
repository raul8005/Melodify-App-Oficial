from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from musico.models import Song
from .forms import UserCreationForm, UserUpdateForm
from .models import User
from .decorators import user_type_required

# Vista de inicio
def inicio(request):
    """Página de inicio."""
    return render(request, 'home.html')

# Vista de registro de usuario
def register_view(request):
    """Registra a un nuevo usuario."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Crea el usuario
            messages.success(request, "¡Registro exitoso! Ahora puedes iniciar sesión.")
            return redirect('users:login')  # Redirigir al login después del registro
        else:
            messages.error(request, "Hubo un error en el formulario. Por favor verifica tus datos.")
    else:
        form = UserCreationForm()  # Crear una instancia vacía del formulario
    return render(request, 'register.html', {'form': form})

# Vista de inicio de sesión
def login_view(request):
    """Autentica al usuario y redirige al dashboard correspondiente."""
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return redirect('users:redirect_dashboard')
        else:
            messages.error(request, "Credenciales incorrectas. Inténtalo nuevamente.")
    return render(request, 'login.html')


# Vista para cerrar sesión
def logout_view(request):
    """Cierra sesión y redirige al login."""
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('users:login')


@login_required
def redirect_dashboard(request):
    """Redirige al dashboard según el tipo de usuario."""
    role_dashboard = {
        'M': 'users:musico_dashboard',
        'O': 'users:oyente_dashboard',
        'P': 'users:productor_dashboard',
    }
    user_role = request.user.user_type
    dashboard_url = role_dashboard.get(user_role)
    if dashboard_url:
        return redirect(dashboard_url)
    else:
        messages.error(request, "Tu rol no está definido correctamente.")
        return redirect('users:login')  

# Dashboard de músico
@login_required
@user_type_required('M')
def musico_dashboard(request):
    """Dashboard para músicos."""
    return render(request, 'musico_dashboard.html')

# Dashboard de oyente
@login_required
@user_type_required('O')  
def oyente_dashboard(request):
    """Dashboard para oyentes."""
    return render(request, 'oyente_dashboard.html')

# Dashboard de productor
@login_required
@user_type_required('P')  
def productor_dashboard(request):
    """Dashboard para productores."""
    return render(request, 'productor_dashboard.html')

# Vista de listar canciones productor
@login_required
def buscar_artista(request):
    """Vista para listar las canciones."""
    songs = Song.objects.all()  
    return render(request, 'oyente/buscar_artista.html', {'songs': songs})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def delete_account(request):
    """Vista para eliminar la cuenta del usuario."""
    if request.method == 'POST':
        user = request.user
        logout(request)  # Cerrar sesión antes de eliminar
        user.delete()
        messages.success(request, "Tu cuenta ha sido eliminada exitosamente.")
        return redirect('users:inicio')
    return render(request, 'confirm_delete.html')