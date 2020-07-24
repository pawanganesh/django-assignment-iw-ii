from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import TemplateView

from account.forms import UserRegisterForm, UserLoginForm
from account.models import User


class LoginView(View):
    form_class = UserLoginForm

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect('blog:index')
        context = {
            'form': self.form_class
        }
        return render(request, 'account/login.html', context=context)

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('home')
        else:
            form = self.form_class
        context = {
            'form': form
        }
        return render(request, 'account/login.html', context=context)


class RegisterView(View):
    form_class = UserRegisterForm

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class
        }
        return render(request, 'account/register.html', context=context)

    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('account/account_activation_mail.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect('account:login')
        else:
            return redirect('account:register')
        #     form = UserRegisterForm
        #     context = {
        #         'form': form
        #     }
        # return render(request, 'account/register.html', context=context)


class ConfirmRegistrationView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            # print(uid)
            user = User.objects.get(pk=uid)
            # print(user)
        except (TypeError, ValueError, OverflowError, user.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse("Thank you for your email confimation. Now you can login your account.")
        else:
            return HttpResponse('Activation link is invalid!')


class Logout(LogoutView):
    template_name = 'blog/index.html'

