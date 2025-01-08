from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django_htmx.http import HttpResponseClientRedirect

from . import services
from .forms import EmailForm

# Global email address used for verification
EMAIL_ADDRESS = settings.EMAIL_ADDRESS

# View to handle logout functionality
def logout_btn_hx_view(request):
    """
    Handles logout for HTMX requests.
    Deletes the 'email_id' from the session and redirects to the home page.
    """
    if not request.htmx:  # Ensure the request is an HTMX request
        return redirect('/')  # Redirect to home for non-HTMX requests

    if request.method == "POST":  # Check if the request is a POST request
        try:
            del request.session['email_id']  # Attempt to delete 'email_id' from session
        except:
            pass  # Silently handle errors if 'email_id' is not in session

        # If 'email_id' is no longer in session, redirect to the home page
        email_id_in_session = request.session.get('email_id')
        if not email_id_in_session:
            return HttpResponseClientRedirect('/')  # HTMX-specific redirect

    # Render a template for the logout button
    return render(request, "emails/hx/logout-btn.html", {})

# View to handle email token login
def email_token_login_view(request):
    """
    Handles email token login via HTMX.
    Renders an email login form and initiates the email verification process.
    """
    if not request.htmx:
        return redirect('/')

    email_id_in_session = request.session.get('email_id')  # Check if user is already logged in
    template_name = "emails/hx/form.html"  # Template for rendering the form
    form = EmailForm(request.POST or None)  # Instantiate the email form with POST data
    context = {
        "form": form,
        "message": "",
        "show_form": not email_id_in_session,  # Show form only if user is not logged in
    }

    if form.is_valid():  # Check if the form submission is valid
        email_val = form.cleaned_data.get('email')  # Extract the email address
        obj = services.start_verification_event(email_val)  # Start the verification process
        context['form'] = EmailForm()  # Reset the form
        context['message'] = f"Success! Check your email for verification from {EMAIL_ADDRESS}"
        # return HttpResponseClientRedirect('/check-your-email')
        return render(request, template_name, context)  # Render the form with a success message
    else:
        print(form.errors)

    return render(request, template_name, context)

# View to verify email tokens
def verify_email_token_view(request, token, *args, **kwargs):
    """
    Verifies the email token and logs the user in if the token is valid.
    If verification fails, redirects to the login page with an error message.
    """
    did_verify, msg, email_obj = services.verify_token(token)  # Verify the token
    if not did_verify:  # Handle failed verification
        try:
            del request.session['email_id']  # Remove 'email_id' from session if present
        except:
            pass  # Silently handle errors
        messages.error(request, msg)  # Display an error message
        return redirect("/login/")  # Redirect to the login page

    # If verification is successful
    messages.success(request, msg)  # Display a success message
    request.session['email_id'] = f"{email_obj.id}"  # Store the user's email ID in the session

    # Redirect to the next URL or home page if 'next_url' is not defined
    next_url = request.session.get('next_url') or "/"
    if not next_url.startswith("/"):  # Ensure the next URL is a valid path
        next_url = "/"
    return redirect(next_url)  # Redirect to the next page
