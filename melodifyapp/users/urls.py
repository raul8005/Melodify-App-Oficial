from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
  #  path('intermediate_dashboard/', views.intermediate_dashboard, name='intermediate_dashboard'),
    path('redirect_dashboard/', views.redirect_dashboard, name='redirect_dashboard'),
    path('musico/', views.musico_dashboard, name='musico_dashboard'),
    path('oyente/', views.oyente_dashboard, name='oyente_dashboard'),
    path('productor/', views.productor_dashboard, name='productor_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('songs/', views.buscar_artista, name='song_list'),
    path('update/', views.update_profile, name='update_profile'),
    path('profile/', views.profile, name='profile'),
    path('delete_account/', views.delete_account, name='delete_account'),  
]
