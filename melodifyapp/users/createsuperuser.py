from django.contrib.auth.management.commands.createsuperuser import Command as BaseCreateSuperUserCommand
from django.core.management import CommandError

class Command(BaseCreateSuperUserCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--age',
            type=int,
            help='Especifica la edad del superusuario.',
        )
        parser.add_argument(
            '--phone_number',
            type=str,
            help='Especifica el número de celular del superusuario.',
        )

    def handle(self, *args, **options):
        age = options.get('age')
        if age is None:
            raise CommandError('Debes proporcionar la edad del superusuario usando --age.')

        phone_number = options.get('phone_number')
        if phone_number is None:
            raise CommandError('Debes proporcionar el número de celular del superusuario usando --phone_number.')

        options['age'] = age
        options['phone_number'] = phone_number

        # Aseguramos que el superusuario tenga privilegios de administrador
        options['is_staff'] = True
        options['is_superuser'] = True
        
        super().handle(*args, **options)
