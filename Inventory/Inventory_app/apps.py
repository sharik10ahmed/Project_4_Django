from django.apps import AppConfig


class InventoryAppConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'

    name = 'Inventory_app'

    def ready(self):

        import Inventory_app.signals