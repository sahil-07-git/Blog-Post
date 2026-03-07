from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_fields = "django.db.models.BigAutoField"
    name = 'blog'

    def ready(self):
        import blog.signals # noqa
