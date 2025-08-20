from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

from .models import ReviewModel
from .forms import SubmitReviewForm


class SubmitReviewView(LoginRequiredMixin, CreateView):
    http_method_names = ['post']
    model = ReviewModel
    form_class = SubmitReviewForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        product = form.cleaned_data['product']
        messages.success(
            self.request,
            'دیدگاه شما با موفقیت ثبت شد و پس از بررسی نمایش داده خواهد شد'
        )
        return redirect(reverse_lazy('shop:product-detail', kwargs={"slug": product.slug}))

    def form_invalid(self, form):
        product = form.cleaned_data.get('product')
        messages.error(self.request, 'خطایی در ثبت دیدگاه اتفاق افتاد')
        if product:
            return redirect(reverse_lazy('shop:product-detail', kwargs={"slug": product.slug}))
        return redirect(self.request.META.get('HTTP_REFERER', '/'))

    def get_queryset(self):
        return ReviewModel.objects.filter(user=self.request.user)
