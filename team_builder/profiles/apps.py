from django.apps import apps, AppConfig


class ProfilesConfig(AppConfig):
    name = 'profiles'


# https://stackoverflow.com/questions/43847173/cannot-import-models-from-another-app-in-django
Project = apps.get_model('projects', 'Project')
Position = apps.get_model('projects', 'Position')
