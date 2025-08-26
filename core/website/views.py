from django.views.generic import TemplateView, FormView, View
from django.core.management import call_command
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin

from .forms import NewsLetterForm, ContactForm
from django.core.mail import send_mail
import logging
import os


from django.db import connection


from django.http import JsonResponse
from django.conf import settings

def test_email(request):
    try:
        send_mail(
            subject="Test Email from Render",
            message="If you see this, Gmail SMTP works!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["rezaei.marjann@gmail.com"],
            fail_silently=False,
        )
        return JsonResponse({"status": "ok", "msg": "email sent"})
    except Exception as e:
        return JsonResponse({"status": "error", "msg": str(e)})
    

logger = logging.getLogger(__name__)

PING_TOKEN = os.getenv("SECRET_PING_TOKEN", "")

def ping_view(request):
    token = request.GET.get("token")
    if not token or token != PING_TOKEN:
        logger.warning(f"❌ Ping attempt with invalid or missing token: {token}")
        return HttpResponse("Unauthorized", status=401)

    logger.info("✅ Ping from UptimeRobot or cron-job.org")
    return HttpResponse("pong")


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


def test_db(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT NOW();")
            row = cursor.fetchone()
        return HttpResponse(f"DB OK - Time: {row[0]}")
    except Exception as e:
        return HttpResponse(f"DB ERROR: {e}")
    

class MigrateView(View):
    def get(self, request, *args, **kwargs):
        try:
            call_command('migrate', interactive=False)
            return HttpResponse("Migrations completed successfully!")
        except Exception as e:
            return HttpResponse(f"Error during migration: {e}")
        

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
            message=(
                f"Email: {form.cleaned_data['email']}\n"
                f"Phone: {form.cleaned_data['phone_number']}\n"
                f"Message: {form.cleaned_data['details']}"
            ),
            from_email=form.cleaned_data['email'],
            recipient_list=["your_email@example.com"],
        )
        form.save()
        messages.success(self.request, "پیام شما با موفقیت ارسال شد!")
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "لطفاً اطلاعات را به درستی وارد کنید.")
        return self.render_to_response(self.get_context_data(form=form))


class NewsletterView(FormView):
    form_class = NewsLetterForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "ایمیل شما با موفقعیت ثبت شد.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "لطفا یک ایمیل معتبر وارد نمایید.")
        return redirect(self.success_url)
