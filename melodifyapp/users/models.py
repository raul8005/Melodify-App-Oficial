from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Encriptar la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Si 'age' no se proporciona, asignar un valor predeterminado
        extra_fields.setdefault('age', 0)
        
        if extra_fields.get('phone_number') is None:
            raise ValueError("Superusers must have a 'phone_number' field set")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    TYPE_CHOICES = [
        ('O', 'Oyente'),
        ('M', 'Músico'),
        ('P', 'Productor'),
    ]
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, default='Desconocido')  # Campo obligatorio
    last_name = models.CharField(max_length=30, default='Desconocido')   # Campo obligatorio
    gender_choices = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    gender = models.CharField(max_length=1, choices=gender_choices)
    age = models.PositiveIntegerField(default=0)  # Ahora es obligatorio
    user_type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='O')
    phone_number = models.CharField(max_length=10, default='0000000000')  # obligatorio
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'age', 'phone_number']  # Añadir age y phone_number

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Follow(models.Model):
    follower = models.ForeignKey('User', related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey('User', related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} sigue a {self.following}"