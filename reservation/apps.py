from django.apps import AppConfig


class ReservationConfig(AppConfig):
    """
    Configuration for the 'reservation' app.

    This class defines the configuration for the 'reservation' app, including its name
    and the default auto-generated primary key field type.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservation'
