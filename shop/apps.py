from django.apps import AppConfig

# Configuración de la aplicación 'shop'
class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Define el tipo de campo automático por defecto
    name = 'shop'  # Nombre de la aplicación

    def ready(self):
        import shop.signals  # Importa las señales de la aplicación al iniciar

