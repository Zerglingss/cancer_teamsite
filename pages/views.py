from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

from .forms import ContactForm
from .models import ContactMessage

from ratelimit.decorators import ratelimit
# from django.http import HttpResponseTooManyRequests
from django.http import HttpResponse

import random

def home(request):
    if 'rand_int' not in request.session:
        request.session['rand_int'] = random.randint(1, 100)
    return render(request, 'pages/home.html', {'rand_int': request.session['rand_int']})

def test(request):
    return render(request, 'pages/react.html')

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    return render(request, 'pages/contact.html')

def contacts(request):
    if not request.session.get('form_submitted'):
        return redirect('contact')  # or 404 if you prefer
    del request.session['form_submitted']
    return render(request, 'pages/contact_success.html')

@ratelimit(key='ip', rate='3/h', method='POST', block=True)
def contact_view(request):
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        return HttpResponse("Too many requests", status=429)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            request.session['form_submitted'] = True
            return redirect(reverse('contact_success'))
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})