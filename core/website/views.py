from django.views.generic.edit import FormView
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.mail import send_mail
from .forms import ContactForm
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect
import random

# Create your views here.

class IndexView(TemplateView):
    template_name = "website/index.html"
    
    
class AboutView(TemplateView):
    template_name = "website/about.html"
    

class ContactView(FormView):
    template_name = "website/contact.html"
    form_class = ContactForm
    success_url = "/contact/"

    def form_valid(self, form):
        send_mail(
            subject=f"Contact Request from {form.cleaned_data['first_name']} {form.cleaned_data['last_name']}",
            message=f"Email: {form.cleaned_data['email']}\nPhone: {form.cleaned_data['phone_number']}\nMessage: {form.cleaned_data['details']}",
            from_email=form.cleaned_data['email'],
            recipient_list=["your_email@example.com"],
        )

        messages.success(self.request, "پیام شما با موفقیت ارسال شد!")
        # Redirect user back to contact page
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "لطفاً اطلاعات را به درستی وارد کنید.")
        return self.render_to_response(self.get_context_data(form=form))
