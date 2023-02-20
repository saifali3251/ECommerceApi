from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = 'base'

    # This is how we are connecting the signal to this app(make sure in setting.py the app is imported as base.apps.BaseConfig)
    def ready(self):
        import base.signals
