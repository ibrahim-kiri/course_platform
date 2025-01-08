from django.conf import settings
from django.shortcuts import render

from emails import services as emails_services
from emails.models import Email, EmailVerificationEvent
from emails.forms import EmailForm

# View for rendering the login/logout page
def login_logout_template_view(request):
    return render(request, "auth/login-logout.html", {})

# Email address used in verification messages
EMAIL_ADDRESS = settings.EMAIL_ADDRESS

# Home page view
def home_view(request, *args, **kwargs):
    template_name = "home.html"
    form = EmailForm(request.POST or None)  # Initialize form with POST data if available
    context = {
        "form": form,
        "message": ""
    }
    
    if form.is_valid():  # Process form submission
        email_val = form.cleaned_data.get('email')  # Extract the email value
        obj = emails_services.start_verification_event(email_val)  # Start verification
        print(obj)  # Log the verification object
        context['form'] = EmailForm()  # Reset the form
        context['message'] = f"Success! Check your email for verification from {EMAIL_ADDRESS}"
    else:
        print(form.errors)  # Log any form errors
    
    # Log the email ID stored in the session (if any)
    print('email_id', request.session.get('email_id'))
    
    return render(request, template_name, context)  # Render the home page with the context
