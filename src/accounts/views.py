from django.conf import settings
from django.contrib.auth import get_user_model,login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage

from .forms import RegistrationForm , ProfileEditForm
from .tokens import account_activation_token

User = get_user_model()


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.email = user_form.cleaned_data['email']
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()
            #send one time activation email
            current_site = get_current_site(request)
            subject = 'Activate Account'
            sender = 'mail@achiengcindy.com'
            message = render_to_string('accounts/account_activation_email.html', {
                'user':  new_user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes( new_user.pk)).decode(),
                'token':account_activation_token.make_token( new_user),
            })
            # https://stackoverflow.com/questions/40655802/how-to-implement-email-user-method-in-custom-user-model
            email = EmailMessage(subject, message,sender, [new_user.email])
            email.send()
            return redirect('account_activation_sent')

    else:
        user_form = RegistrationForm()
    return render(request, 'accounts/register.html',{'user_form': user_form})

def account_activation_sent(request):
    return render(request, 'accounts/account_activation_sent.html')

def activate(request, uidb64, token, backend='accounts.authentication.EmailAuthBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError,User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, 'accounts.authentication.EmailAuthBackend')
        return redirect('login')
    else:
        return render(request, 'accounts/account_activation_invalid.html')

@login_required
def edit(request):
    if request.method == 'POST':
        profile_form = ProfileEditForm(instance=request.user,data=request.POST,files=request.FILES)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        profile_form = ProfileEditForm(instance=request.user)
    return render(request, 'accounts/edit.html', {'profile_form': profile_form})
   


