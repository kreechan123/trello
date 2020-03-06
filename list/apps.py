from django.apps import AppConfig


class ListConfig(AppConfig):
    name = 'list'

    def ready(self):
    	import list.signals
