from email import message
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User # in order to create a user using User.object.save()
from validate_email import validate_email
from django.contrib import messages, auth
from django.core.mail import EmailMessage

from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from userpreferences.models import UserPreference
from .utils import token_generator

from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading

# Create your views here.

class FirstnameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        fieldvalue = data['fieldvalue']
        if str(fieldvalue) == "":
            return JsonResponse({'msg_error': "First name is required."}, status=400)
        if not str(fieldvalue).isalpha():
            return JsonResponse({'msg_error': "First name should only be alphabetical characters only."}, status=400)
        return JsonResponse({'msg_valid': True})

class LastnameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        fieldvalue = data['fieldvalue']
        if str(fieldvalue) == "":
            return JsonResponse({'msg_error': "Last name is required."}, status=400)
        if not str(fieldvalue).isalpha():
            return JsonResponse({'msg_error': "Last name should only be alphabetical characters only."}, status=400)
        return JsonResponse({'msg_valid': True}, status=200)

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        fieldvalue = data['fieldvalue']
        if not str(fieldvalue).isalnum():
            return JsonResponse({'msg_error': "User name should only be alphanumeric characters only."}, status=400)
        if User.objects.filter(username = fieldvalue).exists():
            return JsonResponse({'msg_error': "User name already exist. Please try again."}, status=400)
        return JsonResponse({'msg_valid': True})

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        fieldvalue = data['fieldvalue']
        if not validate_email(fieldvalue):
            return JsonResponse({'msg_error': "Invalid Email. Please try again."}, status=400)
        if User.objects.filter(email = fieldvalue).exists():
            return JsonResponse({'msg_error': "Email is already in use. Please try again."}, status=400)
        return JsonResponse({'msg_valid': True})

# Renders the html page
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    def post(self, request):
        mydata = request.POST
        print(mydata)
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Retains the value of certain fields when submission fails.
        # Check register.html for that selected fields
        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 8:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)                
            
                # Get registration values and create user then save it
                user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname, last_name=lastname)
                user.is_active = False # so the user cannot login before verifying the email
                user.save()

                # Email Verification with link using token generations
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
                activate_url = 'http://' + domain + link

                # Email container for the verification
                email_subject = 'Activate your account'
                email_body = 'Hello! ' + user.username + '\nPlease click the link to verify your account\n' + activate_url

                email = EmailMessage(email_subject, email_body, 'noreply@sample.com', [email])
                # email.send(fail_silently=False)
                EmailThread(email).start()

                messages.success(request, "Registration Successful! Please check your email to activate your account")
                return redirect('login')


        return render(request, 'authentication/register.html')

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully. You can now login.')
            
        except Exception as ex:
            pass
        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, "Welcome, " + user.username + " you are now logged in")
                    return redirect('dashboard:home')
                
                messages.error(request, "Account is not activated. Please check your email for the activation link.")
                return render(request, 'authentication/login.html')
            
            messages.error(request, 'Invalid credentials. Please try again.')
            return render(request, 'authentication/login.html')
        
        messages.error(request, 'Please fill out all the fields')
        return render(request, 'authentication/login.html')

class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        messages.success(request, 'Successfully logged out')
        return redirect('login')

class EmailPasswordResetView(View):
    def get(self, request):
        return render(request, 'authentication/reset_password.html')
    def post(self, request):
        email = request.POST['email']

        if not validate_email(email):
            message.error(request, 'Please enter a valid email')
        
        current_site = get_current_site(request)
        user = User.objects.filter(email=email)
        username = user[0].username

        if user.exists():
            email_contents = {
                'user': user[0],
                'username': username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]),
            }

            link = reverse('set-newpassword', kwargs={'uidb64': email_contents['uid'], 'token': email_contents['token']})
            reset_url = 'http://' + current_site.domain + link
            email_subject = 'Password Reset Link'
            email_body = "You're receiving this email because you requested a password reset for your user account at: " + current_site.domain + "\n\nPlease click the link below to reset your password\n" + reset_url + '\nIn case you forgot your username: ' + username

            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@email.com',
                [email],
            )
            
            EmailThread(email).start()
            return render(request, 'authentication/reset_password_done.html')

        messages.error(request, 'Email not registered')
        return render(request, 'authentication/reset_password.html')

class CompletePasswordResetView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info('Reset link is invalid. Please try again.')
                return render('authentication/reset_password.html')

        except Exception as identifier:
            pass

        return render(request, 'authentication/set_newpassword.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }

        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password != password2:
            messages.error(request, 'Password does not match')
            return render(request, 'authentication/set_newpassword.html', context)

        if len(password) < 8:
            messages.error(request, 'Password too short')
            return render(request, 'authentication/set_newpassword.html', context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()

            messages.success(request,'Password reset successfully. You can now login with your new password')
            return redirect('login')

        except Exception as identifier:
            messages.info(request, 'Something went wrong. Please try again')
            return render(request, 'authentication/set_newpassword.html', context)

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)

        
        
