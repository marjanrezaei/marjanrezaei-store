class SwaggerSafeMixin:
    """
    General mixin for ViewSet and APIView
    - Prevents errors caused by AnonymousUser during Swagger schema generation
    """

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            if hasattr(self, 'queryset') and self.queryset is not None:
                return self.queryset.none()
            return []
        return super().get_queryset()

    def get_object(self, queryset=None):
        if getattr(self, 'swagger_fake_view', False):
            if hasattr(self, 'model') and self.model is not None:
                return self.model()
            return None
        return super().get_object(queryset)
