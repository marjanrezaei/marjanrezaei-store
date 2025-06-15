from django.views.generic import TemplateView, FormView
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from .forms import NewsLetterForm, ContactForm


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
        form.save()
        messages.success(self.request, "پیام شما با موفقیت ارسال شد!")
        # Redirect user back to contact page
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "لطفاً اطلاعات را به درستی وارد کنید.")
        return self.render_to_response(self.get_context_data(form=form))


class NewsletterView(FormView):
    form_class = NewsLetterForm
    success_url = '/'  # Redirect after successful form submission

    def form_valid(self, form):
        form.save()  # Save the form data
        messages.success(self.request, "ایمیل شما با موفقعیت ثبت شد.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "لطفا یک ایمیل معتبر وارد نمایید.")
        return HttpResponseRedirect(self.success_url)  # Redirect on invalid form