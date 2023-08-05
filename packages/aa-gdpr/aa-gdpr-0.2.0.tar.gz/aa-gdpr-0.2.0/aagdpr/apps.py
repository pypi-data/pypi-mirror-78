from django.apps import AppConfig
from . import __version__

class AagdprConfig(AppConfig):
    name = 'aagdpr'
    label = 'aagdpr'
    verbose_name = 'AA GDPR v{}'.format(__version__)