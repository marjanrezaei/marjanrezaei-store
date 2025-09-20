from django.views.generic import ListView, TemplateView
import json
from dashboard.permissions import AdminRequiredMixin
from shop.models import ProductCategoryModel

# ------------------ Category List ------------------
class AdminCategoryListView(AdminRequiredMixin, ListView):
    model = ProductCategoryModel
    template_name = "dashboard/admin/categories/category-list.html"
    context_object_name = "categories"
    paginate_by = 20

    def get_queryset(self):
        qs = ProductCategoryModel.objects.prefetch_related("translations")
        for cat in qs:
            cat.fa_title = cat.safe_translation_getter("title", language_code="fa", any_language=True)
            cat.en_title = cat.safe_translation_getter("title", language_code="en", any_language=True)
            cat.ar_title = cat.safe_translation_getter("title", language_code="ar", any_language=True)
        return qs

# ------------------ Category Form (Create/Edit) ------------------
class AdminCategoryFormView(AdminRequiredMixin, TemplateView):
    template_name = "dashboard/admin/categories/category-form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = ['fa', 'en', 'ar']
        # produce a JSON-safe string for embedding in JS
        context['languages_json'] = json.dumps(context['languages'])
        context['object_id'] = self.kwargs.get('pk')
        return context

class AdminCategoryEditView(TemplateView):
    template_name = "dashboard/admin/categories/category-form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = ['fa', 'en', 'ar']
        context['languages_json'] = json.dumps(context['languages']) 
        context['object_id'] = self.kwargs.get('pk')
        return context

