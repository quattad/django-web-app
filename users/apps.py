from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):  # must be created in order to execute signals
        import users.signals