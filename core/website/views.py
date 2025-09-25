from django.views.generic import TemplateView, FormView, View
from django.core.management import call_command
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import send_mail
import logging
import os
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _

from .forms import NewsLetterForm, ContactForm
from shop.models import ProductModel


# from django.contrib.auth import get_user_model
# User = get_user_model()

# def create_superuser(request):
#     email = "admin@example.com"
#     password = "admin11"

#     if not User.objects.filter(email=email).exists():
#         User.objects.create_superuser(email=email, password=password)
#         return HttpResponse(f"Superuser with email {email} created successfully.")
#     else:
#         return HttpResponse(f"Superuser with email {email} already exists.")

    
# ping
logger = logging.getLogger(__name__)

PING_TOKEN = os.getenv("SECRET_PING_TOKEN", "")

def ping_view(request):
    token = request.GET.get("token")
    if not token or token != PING_TOKEN:
        logger.warning(f"❌ Ping attempt with invalid or missing token: {token}")
        return HttpResponse("Unauthorized", status=401)

    logger.info("✅ Ping from UptimeRobot or cron-job.org")
    return HttpResponse("pong")


# migrate
class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
    

@method_decorator(csrf_exempt, name='dispatch')
class MigrateView(View):
    def get(self, request, *args, **kwargs):
        try:
            call_command('migrate', interactive=False)
            return HttpResponse("✅ Migrations completed successfully!")
        except Exception as e:
            return HttpResponse(f"❌ Error during migration: {e}")
        

class IndexView(TemplateView):
    template_name = "website/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = ProductModel.objects.all()[:4]        
        return context


class AboutView(TemplateView):
    template_name = "website/about.html"


class ContactView(FormView):
    template_name = "website/contact.html"
    form_class = ContactForm
    success_url = "/contact/"

    def form_valid(self, form):
        send_mail(
            subject=_("Contact Request from") + f" {form.cleaned_data['first_name']} {form.cleaned_data['last_name']}",
            message=_("Email") + f": {form.cleaned_data['email']}\n" +
                    _("Phone") + f": {form.cleaned_data['phone_number']}\n" +
                    _("Message") + f": {form.cleaned_data['details']}",
            from_email=form.cleaned_data['email'],
            recipient_list=["rezaei.marjann@gmail.com"],
        )
        form.save()
        messages.success(self.request, _("Your message was sent successfully!"))
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, _("Please enter valid information."))
        return self.render_to_response(self.get_context_data(form=form))
    

class NewsletterView(FormView):
    form_class = NewsLetterForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("Your email has been registered successfully."))
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, _("Please enter a valid email address."))
        return redirect(self.success_url)
